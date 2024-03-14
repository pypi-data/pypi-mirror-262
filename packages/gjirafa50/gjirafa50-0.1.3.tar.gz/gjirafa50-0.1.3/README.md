
---

# Gjirafa50 Python API Client

The Gjirafa50 Python API Client is a Python library that provides easy access to the Gjirafa50 API for scraping product data from the Gjirafa50 website.

## Installation

You can install the Gjirafa50 Python API Client using pip:

```
pip install gjirafa50
```

Alternatively, you can clone this repository and install it locally:

```
git clone https://github.com/slumbersage/gjirafa50-python-api-client.git
cd gjirafa50-python-api-client
pip install .
```

## Usage

Here's how you can use the Gjirafa50 Python API Client:

```python
from gjirafa50 import Gjirafa50APIClient

# Initialize the client
client = Gjirafa50APIClient(base_url="localhost:8000/api", valid_api_keys=["your_api_key"])

# Search for products
search_result = client.search_products(api_key="your_api_key", q="laptop", pagenumber=1)

# Get product details
product_url = "https://gjirafa50.com/product/details/12345"
product_details = client.get_product_details(api_key="your_api_key", product_url=product_url)

print(search_result)
print(product_details)
```

## Supported Parameters for Searching Products

- `api_key` (required): Your API key for accessing the Gjirafa50 API.
- `q` (optional): The search query. Defaults to "laptop".
- `pagenumber` (optional): The page number to search. Defaults to 1.
- `orderby` (optional): The order by parameter. Accepts values: "0" (Most relevant), "10" (Price: Low to High), "11" (Price: High to Low), "16" (Newest), "17" (Highest Discount). Defaults to "10".
- `advs` (optional): Advs parameter. Defaults to False.
- `hls` (optional): Hls parameter. Defaults to False.
- `is_param` (optional): Is parameter. Defaults to False.
- `startprice` (optional): Start price for filtering products.
- `maxprice` (optional): Max price for filtering products.
- `_` (optional): Underscore parameter. Defaults to the current timestamp in milliseconds.

### Examples:

Search for laptops priced between $500 and $1000:

```python
search_result = client.search_products(api_key="your_api_key", q="laptop", pagenumber=1, orderby="10", startprice=500, maxprice=1000)
```

Search for the newest products:

```python
search_result = client.search_products(api_key="your_api_key", q="laptop", pagenumber=1, orderby="16")
```

## Supported Parameters for Getting Product Details

- `api_key` (required): Your API key for accessing the Gjirafa50 API.
- `product_url` (required): The URL of the product for which you want to retrieve details.

### Example:

Get details of a product:

```python
product_url = "https://gjirafa50.com/product/details/12345"
product_details = client.get_product_details(product_url=product_url)
```

---

