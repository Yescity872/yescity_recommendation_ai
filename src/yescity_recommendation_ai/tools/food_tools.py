from typing import Optional,Dict,Any,List
from pydantic import Field,BaseModel,ConfigDict
from crewai.tools import BaseTool
from .base_tool import MongoDBQueryTool
from ..database.schemas import FoodSearchParams
from ..database.mongodb_client import mongodb_client

class FoodSearchInput(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )
    cityName:str=Field(...,description="City name to search for food places")
    category:Optional[str]=Field(None,description="Food category to filter by")
    minRating:Optional[float]=Field(None,description="Minimum average rating (0-5)")
    budget:Optional[str]=Field(None,description="Budget range: 'cheap', 'moderate', 'luxury'")
    vegOnly:Optional[bool]=Field(False,description="Filter for vegetarian places only")
    flagship:Optional[bool]=Field(None,description="Filter for flagship places")
    maxResults:int=Field(10,description="Maximum number of results to return")

class FoodSearchTool(BaseTool):
    name:str="search_food_places"
    description:str="""
    Search for food recommendations in a specific city using YesCity3 database.
    This tool queries the 'foods' collection which contains detailed information
    about restaurants, sweet shops, cafes, and other food places.
    """

    args_schema:type=FoodSearchInput

    def _run(
            self,
            cityName:str,
            category:Optional[str]=None,
            minRating:Optional[float]=None,
            budget:Optional[str]=None,
            vegOnly:Optional[bool]=False,
            flagship:Optional[bool]=None,
            maxResults:int=10
    )-> List[Dict[str,Any]]:
        query_filter={"cityName":{"$regex":f"^{cityName}$","$options":"i"}}

        if category:
            query_filter["category"]={"$regex":category,"$options":"i"}

        if flagship is not None:
            query_filter["flagship"]=flagship

        if vegOnly:
            query_filter["vegOrNonVeg"]={"$regex": "veg", "$options": "i"}

        if minRating is not None:
            # Since you have multiple rating fields, calculate average
            rating_fields = ["valueForMoney", "service", "taste", "hygiene"]
            query_filter["$or"] = []
            for field in rating_fields:
                query_filter["$or"].append({field: {"$gte": minRating}})

        print(f"🍕 Searching foods in {cityName} with filter: {query_filter}")

        base_tool=MongoDBQueryTool(collection_name="foods")
        results=base_tool._run(query_filter=query_filter,limit=maxResults)

        formatted_results=[]
        for result in results:
            ratings=[]
            for field in ["valueForMoney", "service", "taste", "hygiene"]:
                if field in result and result[field]:
                    ratings.append(result[field])

            avg_rating = sum(ratings) / len(ratings) if ratings else None

            formatted = {
                "_id": result.get("_id", ""),
                "foodPlace": result.get("foodPlace", "Unknown"),
                "category": result.get("category", "Unknown"),
                "cityName": result.get("cityName", ""),
                "address": result.get("address", "Address not available"),
                "description": result.get("description", "No description"),
                "valueForMoney": result.get("valueForMoney"),
                "taste": result.get("taste"),
                "service": result.get("service"),
                "hygiene": result.get("hygiene"),
                "avgRating": round(avg_rating, 1) if avg_rating else None,
                "flagship": result.get("flagship", False),
                "vegOrNonVeg": result.get("vegOrNonVeg", "Unknown"),
                "openTime": result.get("openTime", "Timings not available"),
                "phone": result.get("phone", "Not available"),
                "menuSpecial": result.get("menuSpecial"),
                "images": result.get("images", [])
            }

            formatted_results.append(formatted)

        print(f"✅ Found {len(formatted_results)} food places")
        return formatted_results

# Create an instance for easy import
food_search_tool = FoodSearchTool()
