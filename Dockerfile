# Use an existing image as a base
# FROM node:14
FROM python:3.11.3

# Set the working directory
WORKDIR /usr/src/app

# EXPOSE 8088
# Copy the rest of the code
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# set environment variables
ENV CLUSTER uat
ENV TENANT 10000
ENV BOT_ID 740
ENV NUM_DOCS 1
ENV OPENAI_AZURE_ENDPOINT endpointvalue
ENV OPENAI_API_VERSION apiversion
ENV OPENAI_API_KEY dummy
ENV GITHUB_TOKEN githubtoken
ENV HOST_IP localhost
ENV aws_access_key_id awskey
ENV aws_secret_access_key awssecret
ENV region_name region

RUN mkdir -p /logs
RUN pwd
RUN ls /
WORKDIR src
CMD ["python3", "phrasegen.py"]

# CMD /usr/src/app/test.sh ; sleep infinity

# CMD ["python3", "/usr/src/app/src/phrasegen.py"]
# CMD /usr/src/app/test.sh ; sleep infinity
# Define the command to run the app
# CMD ["node", "index.js"]

# docker build -t testimage .
# docker images
# docker run -p 5000:5000 -d testimage:latest
# docker exec -it 161b /bin/bash