import time
import grpc
import os
import json
import crawl_pb2
import crawl_pb2_grpc
import threading
import random
from server import serve
import shutil
from collections import defaultdict
import argparse

DEFAULT_TOP_COMMENT = 10


# The slave server for replication of the master server
class SlaveServer:
    def __init__(
        self, host, port, master_host, master_port, index, top_comments, master=False
    ) -> None:
        self.host = host
        self.port = port
        self.master_host = master_host
        self.master_port = master_port
        self.master = master
        self.index = index  # slave server index number
        self.users = {}
        self.user_status = defaultdict(list)
        self.on_save = True  # flag for saving the dicts to files
        self.channel = grpc.insecure_channel(master_host + ":" + master_port)
        self.stub = crawl_pb2_grpc.CrawlStub(self.channel)
        self.top_comments = top_comments

    # The heartbeat function to check if the master server is available
    def listen_heartbeat(self):
        msg = crawl_pb2.Worker()
        msg.number = -1
        while True:
            if not self.master:
                # sleep for a random time between 0 and 8 seconds to prevent all the slave servers from sending heartbeat at the same time
                if self.index == 1:
                    time.sleep(0.1)
                else:
                    time.sleep(10)
                try:
                    self.stub.SendHeartbeat(msg)
                except Exception as e:
                    try:
                        # force the slave server 2 to first try to connect to slave server 1
                        if self.index == 2:
                            self.channel = grpc.insecure_channel(self.host + ":7878")
                            self.stub = crawl_pb2_grpc.CrawlStub(self.channel)
                        self.stub.SendHeartbeat(msg)
                    except:
                        print(
                            f"Master is not available. Replacing master from port {self.port}..."
                        )
                        # start a new thread to serve the master server
                        threading.Thread(
                            target=serve,
                            args=(self.host, self.port, self.top_comments),
                            daemon=True,
                        ).start()
                        # set the master flag to True to indicate that this server is the master server
                        self.master = True


if __name__ == "__main__":
    # use argparse to parse command line arguments including host, port and master_host, master_port
    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--top-comments",
        type=int,
        default=DEFAULT_TOP_COMMENT,
        help="Value of the variable in the top comments (default: %(default)s)",
    )
    args = parser.parse_args()

    # Set the value of the variable based on the command-line argument
    top_comments = args.top_comments

    slave_idx = int(input("Enter slave index [1/2]: "))
    with open("config.json", "r") as f:
        config = json.load(f)
    if slave_idx == 1:
        host = config["slave1"]["host"]
        port = config["slave1"]["port"]
    elif slave_idx == 2:
        host = config["slave2"]["host"]
        port = config["slave2"]["port"]
    else:
        raise ValueError("Invalid slave index")
    master_host = config["master"]["host"]
    master_port = config["master"]["port"]
    print("Starting slave server...")
    server = SlaveServer(host, port, master_host, master_port, slave_idx, top_comments)
    # start a new thread to listen for heartbeat from the master server
    threading.Thread(target=server.listen_heartbeat, daemon=True).start()
    while True:
        pass
