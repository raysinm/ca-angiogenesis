FROM ubuntu:22.04

RUN apt-get update && apt-get install -y iputils-ping
RUN apt-get install -y python3.10 python3-pip

WORKDIR /opt

# Install dependencies
COPY ./requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the engine code
COPY . /opt/engine

# # Expose the gRPC server port
# EXPOSE 50051

# Start the gRPC server
# CMD [ "python3", "engine_server.py" ]
