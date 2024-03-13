import csv

#❤❤👊 If i want to Find All url From My Site

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import csv

# Function to get all valid URLs from a given site
def get_valid_urls(base_url):
    valid_urls = set()

    # Make an initial request to the base URL
    response = requests.get(base_url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract all anchor tags (links) from the page
        for a_tag in soup.find_all('a', href=True):
            # Join the URL with the base URL to handle relative URLs
            url = urljoin(base_url, a_tag['href'])
            
            # Parse the URL to check its validity
            parsed_url = urlparse(url)

            # Add the valid URLs to the set
            if parsed_url.scheme and parsed_url.netloc:
                valid_urls.add(url)

    return valid_urls

# Function to save valid URLs in a CSV file
def save_to_csv(valid_urls, csv_file_path):
    # Open CSV file for writing
    with open(csv_file_path, 'w', newline='') as csvfile:
        fieldnames = ["Valid URL"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write header
        writer.writeheader()

        # Write data rows
        for url in valid_urls:
            writer.writerow({"Valid URL": url})

    print(f"Valid URLs saved in CSV file: {csv_file_path}")

# Main function
def main():
    base_url = "https://topasiafx.com/"

    # Get all valid URLs from the site
    valid_urls = get_valid_urls(base_url)

    # Specify the CSV file path
    csv_file_path = "topasiafx.csv"

    # Save valid URLs to CSV
    save_to_csv(valid_urls, csv_file_path)

# Run the script
if __name__ == "__main__":
    main()