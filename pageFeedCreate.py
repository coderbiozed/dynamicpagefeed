import csv
from urllib.parse import urljoin

def get_price_level(price):
    if price >= 1 and price <= 100:
        return 1
    elif price <= 500:
        return 2
    elif price <= 1000:
        return 3
    elif price <= 5000:
        return 4
    elif price <= 10000:
        return 5
    elif price <= 50000:
        return 6
    else:
        return 7

def calculate_score_level(review_score, review_score_base):
    # Avoid division by zero
    if review_score_base == 0:
        return 6

    # Calculate the result using review_score / review_score_base
    result = review_score_base / 5

    # Calculate the score using review_score_base / result
    score = review_score / result

    # Map the score to levels
    if score == 5:
        return 1
    elif score >= 4:
        return 2
    elif score >= 3:
        return 3
    elif score >= 2:
        return 4
    elif score >= 1:
        return 5
    else:
        return 6

def create_page_feed_from_slugs(slug_csv_file_path):
    # Read the slugs from the CSV file
    with open(slug_csv_file_path, 'r', newline='', encoding='utf-8') as slug_file:
        reader = csv.DictReader(slug_file)
        rows = list(reader)

    # Specify the CSV file path for the new page feed
    page_feed_csv_path = "data/daynamicPageFeed.csv"

    # Open CSV file for writing
    with open(page_feed_csv_path, 'w', newline='', encoding='utf-8') as page_feed_file:
        fieldnames = ["Page URL", "Country Code", "Property Type Categories", "Custom Label 1", "Custom Label 2", "Partner"]
        writer = csv.DictWriter(page_feed_file, fieldnames=fieldnames, delimiter=';')

        # Write header
        writer.writeheader()

        # Write data rows
        for row in rows:
            slug = row['Slug']
            price = float(row['USD_Price'])
            review_score = float(row['Review_Score'])

            review_score_base_str = row.get('Review_score_base', '')
            try:
                review_score_base = float(review_score_base_str)
            except ValueError:
                review_score_base = 5.0  # Default to 5.0 if the conversion fails

            country_code = row['Country_Code']
            property_type_categories = row['Property_Type_Categories'].replace("[", "").replace("]", "")

            # Assuming the URLs are constructed with a base URL
            page_url = f"https://travelarii.com/property/{slug}"
            price_level = get_price_level(price)

            # Use the modified calculate_score_level function
            review_score_level = calculate_score_level(review_score, review_score_base)

            # Use semicolons as delimiters
            writer.writerow({
                "Page URL": page_url,
                "Country Code": country_code.capitalize(),
                "Property Type Categories": property_type_categories.lower(),
                "Custom Label 1": f"price_{price_level}",
                "Custom Label 2": f"review_score_{review_score_level}",
                "Partner": row.get("Partner", "")
            })

    print(f"Page feed CSV created at: {page_feed_csv_path}")

# Main function
def main():
    # Specify the path to the slug CSV file
    slug_csv_file_path = "data/retrieved_data.csv"

    # Create page feed from slugs with reversed custom levels and save to CSV
    create_page_feed_from_slugs(slug_csv_file_path)

# Run the script
if __name__ == "__main__":
    main()


