FROM ubuntu:22.04

RUN apt-get update && apt-get install -y iputils-ping
RUN apt-get install -y python3.10 python3-pip

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the web code
COPY . /app/web

WORKDIR /app/web
# # Expose the Flask port
# EXPOSE 5000

# # Expose the gRPC port 
# EXPOSE 50051

# WORKDIR /app/web
# ENV FLASK_APP=app

# CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
