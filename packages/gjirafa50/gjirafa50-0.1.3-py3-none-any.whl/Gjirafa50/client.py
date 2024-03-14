import requests
from typing import List, Optional, Union
from .models import Product, ScrapeResult, Banner

class Gjirafa50APIClient:
    def __init__(self, base_url: str, api_key: str, accept: str = "application/json"):
        self.base_url = base_url
        self.api_key = api_key
        self.accept = accept

    def construct_url(self, endpoint: str) -> str:
        return f"{self.base_url}/api/{endpoint}"

    def make_get_request(self, endpoint: str, params: dict) -> dict:
        url = self.construct_url(endpoint)
        headers = {"accept": self.accept, "api-key": self.api_key}
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response.json()
    
    def search(self, pagenumber: int = 1, orderby: str = "10", q: str = "laptop",
            advs: bool = False, hls: bool = False, is_param: bool = False,
            startprice: Optional[int] = None, maxprice: Optional[int] = None,
            underscore: int = 1710025383220, formatted: bool = False) -> Union[None, ScrapeResult]:
        params = {
            "pagenumber": pagenumber,
            "orderby": orderby,
            "q": q,
            "advs": advs,
            "hls": hls,
            "is": is_param,
            "_": underscore
        }
        if startprice is not None and maxprice is not None:
            params["startprice"] = startprice
            params["maxprice"] = maxprice

        search_result = ScrapeResult(**self.make_get_request("search", params))
        if formatted:
            print("Search Result:")
            for i, product in enumerate(search_result.products, start=1):
                print(f"Product {i}:")
                print("Title:", product.title)
                print("Price:", product.price)
                if product.discount:
                    print("Discount:", product.discount)
                print("Link:", product.link)
                print("PriceNoDiscount:", product.price_no_discount)
                print("Image URL:", product.image_url)
                print()
        # Ensure data is not printed when formatted is False
        elif formatted is False:
            pass
        else:
            print(search_result)
        return search_result if not formatted else None

    def productdetails(self, product_url: str, formatted: bool = False) -> dict:
        params = {"product_url": product_url}
        product_details = self.make_get_request("product/details", params)
        if formatted:
            print("Product Details:")
            print("Name:", product_details["Name"])
            print("Price:", product_details["Price"])
            if product_details.get("PriceWithDiscount"):
                print("Price With Discount:", product_details["PriceWithDiscount"])
            print("In Stock:", product_details["InStock"])
            print("Stock Quantity:", product_details["StockQuantity"])
            print("Short Description:", product_details["ShortDescription"])
            print("Full Description:", product_details["FullDescription"])
            print("Delivery Times:")
            for location, delivery_time in product_details["DeliveryTimes"].items():
                print(f"  {location}: {delivery_time}")
            print("Product Specification Model:")
            for key, value in product_details["ProductSpecificationModel"].items():
                print(f"  {key}: {value}")
            print("Image Models:")
            print("  Default Picture Model:")
            print("    Id:", product_details["ImageModels"]["DefaultPictureModel"]["Id"])
            print("    Image URL:", product_details["ImageModels"]["DefaultPictureModel"]["ImageUrl"])
            print("  Picture Models:")
            for picture_model in product_details["ImageModels"]["PictureModels"]:
                print("    Id:", picture_model["Id"])
                print("    Image URL:", picture_model["ImageUrl"])
        # Ensure data is not printed when formatted is False
        elif not formatted:
            pass
        else:
            print(product_details)
        return product_details  # Explicitly return the product details


    def fetch_categories(self, q: Optional[str] = None, min_subcategories: Optional[int] = None,
                        max_subcategories: Optional[int] = None, include_empty_categories: bool = False,
                        formatted: bool = False) -> dict:
        params = {
            "q": q,
            "min_subcategories": min_subcategories,
            "max_subcategories": max_subcategories,
            "include_empty_categories": include_empty_categories
        }
        categories_data = self.make_get_request("categories", params)
        if formatted:
            print("Categories:")
            for category, subcategories in categories_data.items():
                print(f"- {category}")
                for subcategory in subcategories:
                    print(f"  - {subcategory['name']}")
        # Ensure data is not printed when formatted is False
        elif not formatted:
            return categories_data
        else:
            print(categories_data)
        return categories_data  # Explicitly return the data




    def banners(self, formatted: bool = False) -> List[dict]:
        response = self.make_get_request("banners", params={})
        banners_data = response
        
        if formatted:
            print("Banners:")
            for i, banner in enumerate(banners_data, start=1):
                print(f"Banner {i}:")
                print("Link:", banner["link"])
                print("Image URL:", banner["image_url"])
                print()
        return banners_data

    def happy_hours(self, formatted: bool = False) -> List[dict]:
        response = self.make_get_request("happy-hours", params={})
        happy_hours_data = response
        
        if formatted:
            print("Happy Hours Products:")
            for i, product in enumerate(happy_hours_data["products"], start=1):
                print(f"Product {i}:")
                print("Name:", product["Name"])
                print("Price:", product["Price"])
                print("Discount:", product["Discount"])
                print("In Stock:", product["InStock"])
                print("Stock Quantity:", product["StockQuantity"])
                print("SeName:", product["SeName"])
                print("Image URL:", product["ImageUrl"])
                print()
        return happy_hours_data
