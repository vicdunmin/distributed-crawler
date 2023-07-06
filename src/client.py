import threading
import grpc
import crawl_pb2 
import crawl_pb2_grpc
import sys
import time
from datetime import datetime
import json


# The client class for the chat server
class CrawlClient:
    def __init__(self, address, port, backup1, backup2) -> None:
        # connect to the server through the channel and create a stub
        self.channel = grpc.insecure_channel(address + ':' + port)
        self.stub = crawl_pb2_grpc.CrawlStub(self.channel)
        self.backup1 = backup1
        self.backup2 = backup2
        self.online = False
        self.create_user()
    
    # Prepare the client stream for sending messages
    # def _listen_request_stream(self):
    #     user = crawl_pb2.User(name=self.username)
    #     while True:
    #         yield user

    # def _listen_for_messages(self):
    #     """ listen for message in the background """
    #     print("Listening for messages...")
    #     try:
    #         self.stream = self.stub.ChatStream(self._listen_request_stream())
    #         # print all the messages received from the server
    #         for msg in self.stream:
    #             print(f"\n>>{msg.username}: {msg.content}")
    #             # if the client is not online, cancel the stream
    #             if not self.online:
    #                 print("Chat stream cancelled")
    #                 self.stream.cancel()
    #                 return
    #     except grpc.RpcError as e:
    #         try:
    #             self.channel = grpc.insecure_channel(backup_server_1[0] + ':' + backup_server_1[1])
    #             self.stub = crawl_pb2_grpc.ChatStub(self.channel)
    #         except:
    #             self.channel = grpc.insecure_channel(backup_server_2[0] + ':' + backup_server_2[1])
    #             self.stub = crawl_pb2_grpc.ChatStub(self.channel)

        
    
    def create_user(self):
        """ Prompt to create or login user """
        while True:
            username = input("Please enter your username: ")
            if username:
                # if the user enters quit, exit the program
                if username == 'quit':
                    break
                msg = crawl_pb2.User()
                msg.name = username
                res = self.stub.CreateUser(msg)
                # try:
                #     res = self.stub.CreateUser(msg)
                # except grpc.RpcError as e:
                #     try:
                #         self.channel = grpc.insecure_channel(backup_server_1[0] + ':' + backup_server_1[1])
                #         self.stub = crawl_pb2_grpc.ChatStub(self.channel)
                #         res = self.stub.CreateUser(msg)
                #     except:
                #         self.channel = grpc.insecure_channel(backup_server_2[0] + ':' + backup_server_2[1])
                #         self.stub = crawl_pb2_grpc.ChatStub(self.channel)
                #         res = self.stub.CreateUser(msg)
                
                if res.success:
                    print(res.content)
                    self.username = username
                    # start a thread to listen for messages from the server
                    # self._listen_thread = threading.Thread(target=self._listen_for_messages, daemon=True)
                    # self._listen_thread.start()
                    # set the online flag to True to indicate that the client is online
                    self.online = True
                    self.start()
                else:
                    print(f"Create user error: {res.content}")
            else:
                print('Please enter valid username')
    
    def send_message(self):
        """ Send message to an receiver """
        url = input('Please enter the URL: ')
        now = datetime.now()
        current_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        msg = crawl_pb2.Message(username=self.username, url=url, timestamp=current_time)
        res = self.stub.SentMessage(msg)
        # try:
        #     res = self.stub.SentMessage(msg)
        # except grpc.RpcError as e:
        #     try: # try connecting to another master server if failed
        #         self.channel = grpc.insecure_channel(backup_server_1[0] + ':' + backup_server_1[1])
        #         self.stub = crawl_pb2_grpc.ChatStub(self.channel)
        #         res = self.stub.SentMessage(msg)
        #     except:
        #         self.channel = grpc.insecure_channel(backup_server_2[0] + ':' + backup_server_2[1])
        #         self.stub = crawl_pb2_grpc.ChatStub(self.channel)
        #         res = self.stub.SentMessage(msg)
        
        if res.success:
            print(res.content)
        else:
            print("Send message error")
        
    def delete_user(self):
        """ You can only delete yourself """
        
        user = crawl_pb2.User(name=self.username)
        res = self.stub.DeleteUser(user)
        # try:
        #     res = self.stub.DeleteUser(user)
        # except grpc.RpcError as e:
        #     try: # try connecting to another master server if failed
        #         self.channel = grpc.insecure_channel(backup_server_1[0] + ':' + backup_server_1[1])
        #         self.stub = crawl_pb2_grpc.ChatStub(self.channel)
        #         res = self.stub.DeleteUser(user)
        #     except:
        #         self.channel = grpc.insecure_channel(backup_server_2[0] + ':' + backup_server_2[1])
        #         self.stub = crawl_pb2_grpc.ChatStub(self.channel)
        #         res = self.stub.DeleteUser(user)
        
        if res.success: 
            print(f"<Account {self.username} is successfully deleted>")
            return False # exit the program
        else:
            print(f"Delete account error: {res.content}")

        return True

    def user_offline(self):
        """ Logout current user """
        user = crawl_pb2.User(name=self.username)
        res = self.stub.OfflineUser(user)
        # try:
        #     res = self.stub.OfflineUser(user)
        # except grpc.RpcError as e:
        #     try: # try connecting to another master server if failed
        #         self.channel = grpc.insecure_channel(backup_server_1[0] + ':' + backup_server_1[1])
        #         self.stub = crawl_pb2_grpc.ChatStub(self.channel)
        #         res = self.stub.OfflineUser(user)
        #     except:
        #         self.channel = grpc.insecure_channel(backup_server_2[0] + ':' + backup_server_2[1])
        #         self.stub = crawl_pb2_grpc.ChatStub(self.channel)
        #         res = self.stub.OfflineUser(user)
        
        if res.success:
            # set the online flag to False to indicate that the client is offline
            self.online = False
            # cancel the stream
            self.stream.cancel()
            # wait for the thread to finish
            self._listen_thread.join()
            print(f"<Account {self.username} is now offline>")
        else:
            print(f"Account offline error")

    def start(self):
        """ Command loop """
        while True:
            print(' --------------------------')
            print('|Type 1 to send URL        |')
            print('|Type 2 to delete account  |')
            print('|Type 3 to get offline     |')
            print(' --------------------------')
            
            cmd = input("Please enter a number: ")
            if cmd == '1':
                self.send_message()
            elif cmd == '2':
                if not self.delete_user():
                    sys.exit()
            elif cmd == '3':
                # call the user_offline method to logout the user
                self.user_offline()
                time.sleep(0.5)
                sys.exit()


if __name__ == "__main__":
    # parse the command line arguments for the address and port
    with open("config.json", "r") as f:
        config = json.load(f)
    address = config["master"]["host"]
    port = config["master"]["port"]
    backup_server_1 = (config["slave1"]["host"], config["slave1"]["port"])
    backup_server_2 = (config["slave2"]["host"], config["slave2"]["port"])
    # create a client object to start the client program
    CrawlClient(address, port, backup_server_1, backup_server_2)
   