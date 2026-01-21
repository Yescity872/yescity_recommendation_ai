from yescity_recommendation_ai.tools.food_tools import food_search_tool

if __name__ == "__main__":
    results=food_search_tool.run(
        cityName='varanasi',
        category='Street Food',
        minRating=0.0,
        maxResults=5,
)
    
    for r in results:
        print(r["foodPlace"])
