# Use an existing image as a base
# FROM node:14
FROM python:3.11.3

# Set the working directory
WORKDIR /usr/src/app

# Copy the rest of the code
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8088
# set environment variables
ENV CLUSTER uat
ENV TENANT 10000
ENV BOT_ID 740
ENV NUM_DOCS 1

CMD ["python3", "./src/phrasegen.py", "uat", "10000", "740"]

# CMD ["python3", "/usr/src/app/src/phrasegen.py"]
# CMD /usr/src/app/test.sh ; sleep infinity
# Define the command to run the app
# CMD ["node", "index.js"]

# docker build -t testimage .
# docker images
# docker run -p 5000:5000 -d testimage:latest
# docker exec -it 161b /bin/bash