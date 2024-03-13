import boto3
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def upload_csv_to_s3(file_path, bucket_name, s3_key):
    # Retrieve AWS credentials from environment variables
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    
    if not aws_access_key_id or not aws_secret_access_key:
        print("AWS credentials not found in environment variables. Make sure to set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY.")
        return

    # Create an S3 client
    s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    
    try:
        # Upload the CSV file to the specified S3 bucket and key
        s3.upload_file(file_path, bucket_name, s3_key)
        print(f"File uploaded successfully to S3://{bucket_name}/{s3_key}")
    except Exception as e:
        print(f"Error uploading file to S3: {e}")

# Replace 'your_file.csv', 'cdn.travelarii.com', and 'your_s3_key' with your file, bucket, and key information
upload_csv_to_s3('data/daynamicPageFeed.csv', 'cdn.travelarii.com', 'dynamicFeed')
