from typing import Optional,List,Dict,Any
from pydantic import BaseModel, Field,ConfigDict
from pydantic_core import core_schema
from bson import ObjectId
from datetime import datetime

# class PyObjectId(ObjectId):
#     @classmethod
#     def __get_pydantic_core_schema__(
#         cls,
#         _source_type: Any,
#         _handler: Any,
#     ) -> core_schema.CoreSchema:
#         return core_schema.union_schema([
#             # Check if it's an instance of ObjectId
#             core_schema.is_instance_schema(ObjectId),
#             # Validate from string
#             core_schema.str_schema(),
#             # Validate from bytes
#             core_schema.bytes_schema(),
#         ])

#     @classmethod
#     def __get_pydantic_json_schema__(
#         cls,
#         _core_schema: core_schema.CoreSchema,
#         _handler: Any,
#     ) -> Dict[str, Any]:
#         return {"type": "string"}

#     @classmethod
#     def validate(cls, v):
#         if isinstance(v, ObjectId):
#             return v
#         if isinstance(v, str):
#             try:
#                 return ObjectId(v)
#             except Exception:
#                 raise ValueError("Invalid ObjectId")
#         if isinstance(v, bytes):
#             try:
#                 return ObjectId(v.decode())
#             except Exception:
#                 raise ValueError("Invalid ObjectId")
#         raise TypeError(f"Expected ObjectId, str, or bytes, got {type(v)}")

class FoodSchema(BaseModel):
    # Use the new ConfigDict instead of inner Config class
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
        json_encoders={ObjectId: str},
    )
    id:Optional[ObjectId]=Field(None,alias="_id")
    cityId:Optional[str]=None
    cityName:str
    engagement:Optional[Dict[str,Any]]=None
    flagship:Optional[bool]=False
    reviews:List[Dict[str,Any]]=[]
    foodPlace:str
    lat:float
    lon:float
    address:str
    locationLink:Optional[str]=None
    category:str
    vegOrNonVeg: Optional[str] = None
    valueForMoney: Optional[float] = None
    service: Optional[float] = None
    taste: Optional[float] = None
    hygiene: Optional[float] = None
    menuSpecial: Optional[str] = None
    menulink: Optional[str] = None
    openDay: Optional[str] = None
    openTime: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None
    images: List[str] = []

class FoodSearchParams(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )
    """Parameters for food search."""
    cityName: Optional[str] = None
    category: Optional[str] = None
    minRating: Optional[float] = Field(None, ge=0, le=5)
    minValueForMoney: Optional[float] = Field(None, ge=0, le=5)
    minTaste: Optional[float] = Field(None, ge=0, le=5)
    vegOnly: Optional[str] = None
    flagship: Optional[bool] = None
    limit: int = Field(10, ge=1, le=50)   
