import threading
import grpc
import crawl_pb2
import crawl_pb2_grpc
import sys
import time
from datetime import datetime
import json
from youtube import get_comments_from_url


# The client class for the chat server
class CrawlWorker:
    def __init__(self, address, port, backup1, backup2) -> None:
        # connect to the server through the channel and create a stub
        self.channel = grpc.insecure_channel(address + ":" + port)
        self.stub = crawl_pb2_grpc.CrawlStub(self.channel)
        self.backup1 = backup1
        self.backup2 = backup2
        self.online = False
        self.create_user()

    def _listen_for_messages(self):
        """listen for message in the background"""
        print("Listening for tasks...")
        try:
            self.stream = self.stub.TaskStream(crawl_pb2.Worker(number=self.number))
            # print all the messages received from the server
            for msg in self.stream:
                print(f"\n>>Assigned Task URL: {msg.url}")
                # if the client is not online, cancel the stream
                self.process_url(msg.url, 10)
                if not self.online:
                    print("Crawl stream cancelled")
                    self.stream.cancel()
                    return
        except grpc.RpcError as e:
            try:
                self.channel = grpc.insecure_channel(
                    self.backup1[0] + ":" + self.backup1[1]
                )
                self.stub = crawl_pb2_grpc.CrawlStub(self.channel)
                self.create_user()
            except:
                self.channel = grpc.insecure_channel(
                    self.backup2[0] + ":" + self.backup2[1]
                )
                self.stub = crawl_pb2_grpc.CrawlStub(self.channel)
                self.create_user()

    def process_url(self, url, top_comments):
        # get the top popular comments from the url
        comments = get_comments_from_url(url, top_comments)
        try:
            # In case some videos turn their comments off, we just skip them
            if len(comments) < top_comments:
                print("Unable to fetch comments, skipping...")
                self.stub.ReceiveComment(crawl_pb2.Comment(url=url, isBad=1))
                return
            # Send the comments to the server by iterating through the list
            for i, comment in enumerate(comments):
                cmt = crawl_pb2.Comment(
                    url=url, content=comment, sequence=i, worker_id=self.number, isBad=0
                )
                self.stub.ReceiveComment(cmt)
        except grpc.RpcError as e:
            try:
                self.channel = grpc.insecure_channel(
                    self.backup1[0] + ":" + self.backup1[1]
                )
                self.stub = crawl_pb2_grpc.CrawlStub(self.channel)
                if len(comments) < top_comments:
                    print("Unable to fetch comments, skipping...")
                    self.stub.ReceiveComment(crawl_pb2.Comment(url=url, isBad=1))
                    return
                for i, comment in enumerate(comments):
                    cmt = crawl_pb2.Comment(
                        url=url,
                        content=comment,
                        sequence=i,
                        worker_id=self.number,
                        isBad=0,
                    )
                    self.stub.ReceiveComment(cmt)
            except:
                self.channel = grpc.insecure_channel(
                    self.backup2[0] + ":" + self.backup2[1]
                )
                self.stub = crawl_pb2_grpc.CrawlStub(self.channel)
                if len(comments) < 10:
                    print("Unable to fetch comments, skipping...")
                    self.stub.ReceiveComment(crawl_pb2.Comment(url=url, isBad=1))
                    return
                for i, comment in enumerate(comments):
                    cmt = crawl_pb2.Comment(
                        url=url,
                        content=comment,
                        sequence=i,
                        worker_id=self.number,
                        isBad=0,
                    )
                    self.stub.ReceiveComment(cmt)

        return

    def create_user(self):
        """Prompt to create or login user"""
        worker = crawl_pb2.Worker()
        try:
            res = self.stub.CreateWorker(worker)
        except grpc.RpcError as e:
            try:
                self.channel = grpc.insecure_channel(
                    self.backup1[0] + ":" + self.backup1[1]
                )
                self.stub = crawl_pb2_grpc.CrawlStub(self.channel)
                res = self.stub.CreateWorker(worker)
            except:
                self.channel = grpc.insecure_channel(
                    self.backup1[0] + ":" + self.backup2[1]
                )
                self.stub = crawl_pb2_grpc.CrawlStub(self.channel)
                res = self.stub.CreateWorker(worker)
        if res.success:
            print(f"Assigned Worker number is {res.content}")
            self.number = int(res.content)
            # start a thread to listen for messages from the server
            self._listen_thread = threading.Thread(
                target=self._listen_for_messages, daemon=True
            )
            self._listen_thread.start()
            # set the online flag to True to indicate that the client is online
            self.online = True
            self.start()
        else:
            print(f"Create user error: {res.content}")

    def start(self):
        """Command loop"""
        while True:
            pass


if __name__ == "__main__":
    # parse the command line arguments for the address and port
    with open("config.json", "r") as f:
        config = json.load(f)
    address = config["master"]["host"]
    port = config["master"]["port"]
    backup_server_1 = (config["slave1"]["host"], config["slave1"]["port"])
    backup_server_2 = (config["slave2"]["host"], config["slave2"]["port"])
    # create a client object to start the client program
    CrawlWorker(address, port, backup_server_1, backup_server_2)
