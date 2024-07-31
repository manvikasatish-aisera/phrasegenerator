import os
import subprocess
from datetime import datetime
from dotenv import load_dotenv

# Returns the date of the results excel file, assuming they follow the naming convention
def returnDate(file_name): # Needs file_name to follow the naming format: <cluster>_tenant<tenant>_botid<botid>_excel_year_month_day_hour_minute.xlsx
    startIndex = file_name.rfind("excel") + 6
    endIndex = file_name.rfind(".")
    return file_name[startIndex : endIndex]

# Uploads the latest excel file into the AWS S3 bucket.
def uploadFile_to_S3(cluster, tenant, bot):
    # Finds latest file based on date
    latest_file = None
    for filename in os.listdir("../results"):
        if filename.endswith(".DS_Store"):
            continue
        file_path = os.path.join("../results", filename)
        if latest_file is None or datetime.strptime(returnDate(file_path), "%Y_%m_%d_%H_%M") > datetime.strptime(returnDate(latest_file), "%Y_%m_%d_%H_%M"):
            latest_file = file_path

    if latest_file is None:
        print("No file found to upload.")
        return

    bucket_name = f"aiseratenants-{cluster}"
    s3_folderPath = f"{tenant}/KBPhrases/botid{bot}/" + str(latest_file)

    # Construct the AWS CLI command
    command = [
        "aws", "s3", "cp", latest_file,
        f"s3://{bucket_name}/{s3_folderPath}"
    ]

    # Run the command
    result = subprocess.run(command, capture_output=True, text=True)

    print("Command:", " ".join(command))
    print("Return code:", result.returncode)
    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)

    if result.returncode == 0:
        print(f'File -{latest_file}- uploaded to S3 bucket: {bucket_name}.')
        print(f'S3 Path: s3://{bucket_name}/{s3_folderPath}')
    else:
        print(f'Failed to upload file. Error: {result.stderr}')