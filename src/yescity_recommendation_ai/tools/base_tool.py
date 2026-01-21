from typing import Dict,List,Any,Optional
from pydantic import BaseModel,Field
from crewai.tools import BaseTool
from ..database.mongodb_client import mongodb_client
from bson import ObjectId

class MongoDBQueryTool(BaseTool):

    name: str = "mongodb_query_tool"
    description: str = "Base tool to query MongoDB collections with proper schema handling"
    collection_name: str=Field(..., description="Name of the MongoDB collection to query")

    def _run(self,query_filter: Dict[str,Any]=None,limit:int=10,**kwargs)->List[Dict]:
        """
        Run a query on the specified collection.
        
        Args:
            query_filter: MongoDB query filter
            limit: Maximum number of results to return
            **kwargs: Additional query parameters
            
        Returns:
            List of documents with _id converted to string
        """

        try:
            collection=mongodb_client.get_collection(self.collection_name)

            #Build query filter
            filter_dict=query_filter or {}
            if kwargs:
                filter_dict.update(kwargs)

            for key,value in filter_dict.items():
                if isinstance(value,str) and key in ['cityName','foodPlace','category']:
                    filter_dict[key]={'$regex':value,'$options':'i'}

            print(f"🔍 Querying {self.collection_name}: {filter_dict}")

            cursor=collection.find(filter_dict).limit(limit)
            results=list(cursor)

            processed_results=[]
            for doc in results:
                processed={}
                for key,value in doc.items():
                    if isinstance(value,ObjectId):
                        processed[key]=str(value)
                    else:
                        processed[key]=value
                processed_results.append(processed)
            
            print(f"Found {len(processed_results)} documents.")
            return processed_results
        
        except Exception as e:
            error_msg = f"Failed to query collection {self.collection_name}: {str(e)}"
            print(f"❌ {error_msg}")
            return [{"error": error_msg}]