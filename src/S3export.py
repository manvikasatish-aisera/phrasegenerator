import boto3
import os
from datetime import datetime
from dotenv import load_dotenv

#returns the date of the results excel file, assuming they follow the naming convention
def returnDate(file_name): #needs file_name to follow the naming format: <cluster>_tenant<tenant>_botid<botid>_excel_year_month_day_hour_minute.xlsx
    startIndex = file_name.rfind("excel") + 6
    endIndex = file_name.rfind(".")
    return file_name[startIndex : endIndex]

#uploads the latest excel file into the amazon s3 bucket
def uploadFile_to_S3(cluster, tenant, bot ):
    #finds latest file based on date
    latest_file = None
    for filename in os.listdir("../results"):
        if filename[filename.rfind("."):] != ".DS_Store":
            file_path = os.path.join("results", filename)
            if latest_file is None or datetime.strptime(returnDate(file_path),"%Y_%m_%d_%H_%M") > datetime.strptime(returnDate(latest_file),"%Y_%m_%d_%H_%M"):
                latest_file = file_path

    bucket_name = f"aiseratenants-{cluster}" 
    s3_folderPath = f"{tenant}/KBPhrases/botid{bot}/" + str(latest_file)
    #loads all the creds needed to access amazon s3
    load_dotenv()
    session = boto3.Session(
        aws_access_key_id = os.getenv("aws_access_key_id"),
        aws_secret_access_key = os.getenv("aws_secret_access_key"),
        region_name = os.getenv("region_name")
    )
    s3 = session.client("s3")

    #changes directory for naming purposes, before changing back
    os.chdir(os.getcwd()[:os.getcwd().rfind("/")])
    s3.upload_file(latest_file, bucket_name, s3_folderPath)
    os.chdir(os.getcwd()+"/src")
    
    print(f'File -{latest_file}- uploaded to S3 bucket: {bucket_name}.')
    print(f'S3 Path: {bucket_name}/{s3_folderPath}')