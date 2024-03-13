
from elasticsearch import Elasticsearch
from dotenv import load_dotenv
from opensearchpy import OpenSearch
import csv
from urllib.parse import urljoin
from elasticsearch.helpers import scan
import os

load_dotenv()

es_host = os.getenv("es_host")
es_port = os.getenv("es_port")
username = 'travelarii2023'
password = os.getenv("password")
es_scheme = os.getenv('scheme', 'https')
environment = os.getenv("environment")

print(f"ES Host: {es_host}")
print(f"ES Port: {es_port}")
print(f"Environment: {environment}")

if environment == "local":
    es = Elasticsearch(f"http://{es_host}:{es_port}")
else:
    es = OpenSearch(
        f"https://search-travelarii-l353a43pnq6vopkgrznuhvxifm.us-east-1.es.amazonaws.com/",
        http_auth=(username, password),
        verify_certs=False,  # Disable SSL/TLS verification (for testing only)
    )

INDEX_NAME = "properties"

    
# Define your query with filters
query = {
    "query": {
        "bool": {
            "must": [
                {
                    "exists": {
                        "field": "slug"
                    }
                }
            ]
        }
    }
}

# Execute the initial search query using scroll
response = es.search(index=INDEX_NAME, body=query, scroll="2m", size=1000)  # Adjust the size as needed

# Extract slugs and additional data from the response
data = [
    {
        "Slug": hit["_source"]["slug"],
        "Country_Code": hit["_source"]["country_code"],
        "Property_Type_Categories": hit["_source"]["property_type_categories"],
        "Review_score_base": hit["_source"].get("review_score_base", None),  # Use get method to avoid KeyError
        "Review_Score": hit["_source"]["review_score"],
        "USD_Price": hit["_source"]["usd_price"], 
        "Partner": hit["_source"]["partner"],
        "Published": hit["_source"]["published"],
         # Replace with the actual field name
    }
    for hit in response["hits"]["hits"]
]
# 🎨🎨🎨 Example:👉👉👉   US;House;price_2;review_score_2;booking.com
# Specify the CSV file path
csv_file_path = "retrieved_data.csv"
fieldnames = ["Slug", "Country_Code", "Property_Type_Categories", "Review_score_base", "Review_Score", "USD_Price", "Partner", "Published"]
# Write data to CSV file
# Write data to CSV file
with open(csv_file_path, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Write header
    writer.writeheader()

    # Write data rows
    writer.writerows(data)

# Use scroll to retrieve remaining data
while len(response["hits"]["hits"]) > 0:
    scroll_id = response["_scroll_id"]
    response = es.scroll(scroll_id=scroll_id, scroll="2m")
    
    # Extract additional data from the response
    additional_data = [
        {
            "Slug": hit["_source"]["slug"],
            "Country_Code": hit["_source"]["country_code"],
            "Property_Type_Categories": hit["_source"]["property_type_categories"],
            "Review_score_base": hit["_source"].get("review_score_base", None), 
            "Review_Score": hit["_source"]["review_score"],
            "USD_Price": hit["_source"]["usd_price"],  # Replace with the actual field name
            "Partner": hit["_source"]["partner"],
            "Published": hit["_source"]["published"],
             # Replace with the actual field name review_score_base
        }
        for hit in response["hits"]["hits"]
    ]

    # Append additional data to the CSV file
    with open(csv_file_path, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerows(additional_data)

print(f"Data saved in CSV file: {csv_file_path}")