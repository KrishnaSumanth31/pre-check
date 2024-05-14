import sys
from datetime import datetime, timedelta
import boto3

def delete_old_files(bucket_name):
    s3 = boto3.client('s3')
    
    # Get list of objects in the bucket
    objects = s3.list_objects_v2(Bucket=bucket_name)['Contents']
    
    # Calculate the date 30 days ago
    thirty_days_ago = datetime.now() - timedelta(days=30)
    
    # Iterate through objects and delete files older than 30 days
    for obj in objects:
        last_modified = obj['LastModified'].replace(tzinfo=None)
        if last_modified < thirty_days_ago:
            s3.delete_object(Bucket=bucket_name, Key=obj['Key'])
            print(f"Deleted file: {obj['Key']}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python glue_script.py <bucket_name>")
        sys.exit(1)
    
    bucket_name = sys.argv[1]
    delete_old_files(bucket_name)

if __name__ == "__main__":
    main()
