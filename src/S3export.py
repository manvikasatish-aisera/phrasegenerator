import os
import boto3
from datetime import datetime
from configparser import ConfigParser

def load_aws_credentials_from_above(profile='default'):
    # Determine the path to the credentials file located one directory above
    credentials_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.aws', 'credentials')

    # Read the credentials file
    config = ConfigParser()
    config.read(credentials_path)

    if profile in config:
        # Set environment variables
        os.environ['AWS_ACCESS_KEY_ID'] = config[profile]['aws_access_key_id']
        os.environ['AWS_SECRET_ACCESS_KEY'] = config[profile]['aws_secret_access_key']
        print(f"Loaded credentials for profile: {profile}")
    else:
        print(f"Profile {profile} not found in {credentials_path}")

# Returns the date of the results excel file, assuming they follow the naming convention
def returnDate(file_name): # Needs file_name to follow the naming format: <cluster>_tenant<tenant>_botid<botid>_excel_year_month_day_hour_minute.xlsx
    startIndex = file_name.rfind("excel") + 6
    endIndex = file_name.rfind(".")
    return file_name[startIndex : endIndex]

# Uploads the latest excel file into the AWS S3 bucket.
def uploadFile_to_S3(cluster, tenant, bot ):
    # Finds latest file based on date.
    latest_file = None
    for filename in os.listdir("../results"):
        if filename[filename.rfind("."):] != ".DS_Store":
            file_path = os.path.join("results", filename)
            if latest_file is None or datetime.strptime(returnDate(file_path),"%Y_%m_%d_%H_%M") > datetime.strptime(returnDate(latest_file),"%Y_%m_%d_%H_%M"):
                latest_file = file_path

    bucket_name = f"aiseratenants-{cluster}" 
    s3_folderPath = f"{tenant}/KBPhrases/botid{bot}/" + str(latest_file)
    os.environ['AWS_DEFAULT_REGION'] = 'us-west-2'

    # Loads all the creds needed to access AWS S3.
    session = boto3.Session(
        aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name = os.getenv("AWS_DEFAULT_REGION")
    )
    s3 = session.client("s3")

    # Changes directory for naming purposes, before changing back
    os.chdir(os.getcwd()[:os.getcwd().rfind("/")])
    s3.upload_file(latest_file, bucket_name, s3_folderPath)
    os.chdir(os.getcwd()+"/src")
    
    print(f'File -{latest_file}- uploaded to S3 bucket: {bucket_name}.')
    print(f'S3 Path: {bucket_name}/{s3_folderPath}')