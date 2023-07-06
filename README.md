# cs262_proj
CS262 Final Project: Distributed Web Crawler
## Usage

### config.json

Update your master and slave server's ips and ports in this file
### GRPC

Recompile the `chat.proto` inside `src` folder (when you change the file):

    python3 -m grpc_tools.protoc -Iprotos --python_out=. --pyi_out=. --grpc_python_out=. protos/crawl.proto

### Master server

Run the master server:

    python3 src/server.py

### Slave server

Run the slave server:

    python3 src/slave_server.py

### Worker

You can add workers to the system at anytime during the web crawling job. They can also be disconnected without interfering the job. 

Run the worker:

    python3 src/worker.py