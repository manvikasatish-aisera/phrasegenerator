FROM python:3.11.3

# Set the working directory
RUN cat ~/.aws/credentials 

WORKDIR /usr/src/app

# Copy the rest of the code
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# set environment variables
ENV CLUSTER uat
ENV TENANT 10000
ENV BOT_ID 740
ENV NUM_DOCS 1
ENV GITHUB_TOKEN githubtoken
ENV TODAY date
ENV VAULT_ADDR vaultaddr
ENV AWS_ACCESS_KEY_ID tempid
ENV AWS_SECRET_ACCESS_KEY tempkey

RUN mkdir -p /logs
RUN pwd
RUN ls /

WORKDIR src

CMD ["python3", "phrasegen.py"]