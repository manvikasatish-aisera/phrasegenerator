import boto3
import os
from datetime import datetime
from dotenv import load_dotenv

def returnDate(file_name): #needs file_name to follow the naming format
    return file_name[file_name[:file_name.rfind("_")-1].rfind("_")+1 : file_name.rfind(".")]

def uploadFile_to_S3():
    latest_file = None
    for filename in os.listdir("results"):
        if filename[filename.rfind("."):] != ".DS_Store":
            file_path = os.path.join("results", filename)
            if latest_file is None or datetime.strptime(returnDate(file_path),"%Y-%m-%d_%H:%M:%S") > datetime.strptime(returnDate(latest_file),"%Y-%m-%d_%H:%M:%S"):
                latest_file = file_path

    bucket_name = "aiseratenants-uat"
    s3_folderPath = "10000/KBPhrases/botid740/" + str(latest_file)

    load_dotenv()
    session = boto3.Session(
        aws_access_key_id = os.getenv("aws_access_key_id"),
        aws_secret_access_key = os.getenv("aws_secret_access_key"),
        region_name = os.getenv("region_name")
    )
    s3 = session.client("s3")

    s3.upload_file(latest_file, bucket_name, s3_folderPath)
    print(f'File -{latest_file}- uploaded to S3 bucket: {bucket_name}')