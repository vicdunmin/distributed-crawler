import shutil
from concurrent import futures
import grpc
import json
import threading
import os
from collections import defaultdict
import time
from datetime import datetime
import argparse
from .youtube import get_trending_urls
from . import crawl_pb2
from . import crawl_pb2_grpc

# We get top 10 most popular comments by default
DEFAULT_TOP_COMMENT = 10


# An abstract class for the working queue (work status)
class Queue:
    def __init__(self) -> None:
        # all the trending urls
        self.work_queue = []
        # all the pending urls
        self.pending_queue = []
        # all the completed urls
        self.completed_queue = []


class CrawlServer(crawl_pb2_grpc.CrawlServicer):
    """Provides methods that implement functionality of web scraping server."""

    def __init__(self, top_comments, num_urls = -1, timer : bool = False) -> None:
        self.top_comments = top_comments
        # we need to load the tasks from the logs if they exist
        self.init_state(num_urls)
        # time the completion of tasks
        self.timer = timer
        if self.timer:
            self.start = datetime.now()
            self.time_per_url = []

    def init_state(self, num_urls):
        # set the upperbound for number of urls
        self.num_urls = num_urls
        # load from json files if they exist
        if os.path.exists("logs/tasks.json"):
            with open("logs/tasks.json", "r") as f:
                self.tasks = json.load(f)
        else:
            self.tasks = {}
        if os.path.exists("logs/output.json"):
            with open("logs/output.json", "r") as f:
                self.output = defaultdict(list, json.load(f))
        else:
            self.output = defaultdict(list)
        if os.path.exists("logs/queue.json"):
            with open("logs/queue.json", "r") as f:
                self.queue_dict = json.load(f)
            # we need to convert the dict to Queue object
            queue = Queue()
            queue.completed_queue = self.queue_dict["completed_queue"]
            queue.pending_queue = self.queue_dict["pending_queue"]
            queue.work_queue = self.queue_dict["work_queue"]
        else:
            trending_urls = get_trending_urls(num_urls)
            queue = Queue()
            queue.work_queue = trending_urls
        self.queue = queue
        if os.path.exists("logs/url_finished.json"):
            with open("logs/url_finished.json", "r") as f:
                # we use defaultdict to avoid key error
                self.url_finished = defaultdict(bool, json.load(f))
        else:
            self.url_finished = defaultdict(bool)
        # assigned worker number starts from 0
        if os.path.exists("logs/worker_nums.json"):
            with open("logs/worker_nums.json", "r") as f:
                self.worker_nums = json.load(f)["number"]
        else:
            self.worker_nums = 0

    def CreateWorker(self, request, context):
        """Create a worker"""

        i = self.worker_nums
        if i not in self.tasks.keys():
            worker_id = i
            self.tasks[worker_id] = []
            self.worker_nums += 1
        print(f"Created Worker {worker_id}")
        time.sleep(1)
        # We need to save the state after creating a worker
        self.save_state()
        res = crawl_pb2.Response(content=str(worker_id), success=1)
        # start a thread to distribute tasks to the worker that was just created
        threading.Thread(
            target=self.distribute_task, args=(worker_id,), daemon=True
        ).start()
        return res

    def distribute_task(self, worker_id):
        """Distribute Task Among workers"""
        print(f"Distributing tasks to worker {worker_id}...")
        # If there are any work left, we distribute the work to the worker
        while self.queue.work_queue:
            # assignment to worker
            task = self.queue.work_queue.pop()
            print(f"current task for worker {worker_id} is {task[-11:]}")
            # we need to add the task to the pending queue
            self.queue.pending_queue.append(task)
            msg = {"username": str(worker_id), "url": task, "timestamp": "1"}
            self.tasks[worker_id].append(msg)
            # We need to check whether task is finished or not in case a worker has timeout
            self.check_for_finished_task(task, worker_id)

    def check_for_finished_task(self, url, worker_id):
        start = datetime.now()
        while not self.url_finished[url]:
            # We set the timeout to be 20s. If after 20s, the task is not finished, we reassign the task to another worker
            # by adding the task back to the work queue and pop it from the pending queue
            if (datetime.now() - start).total_seconds() >= 20:
                print(
                    f"Worker {worker_id} failed to finish task in time, reassigning..."
                )
                self.queue.work_queue.append(url)
                self.queue.pending_queue.remove(url)
                break
        # If the task is finished, we remove the task from the pending queue and add it to the completed queue
        if self.url_finished[url]:
            process_time = (datetime.now() - start).total_seconds()
            print(
                f"Worker {worker_id} finished scraping url[{url[-11:]}] in [{process_time:.1f}]s!"
            )
            if self.timer:
                self.time_per_url.append(process_time)
            self.queue.pending_queue.remove(url)
            self.queue.completed_queue.append(url)
            print(
                f"[TODO: {len(self.queue.work_queue)}] [Pending: {len(self.queue.pending_queue)}] [Completed: {len(self.queue.completed_queue)}]"
            )
            # All task finished
            if self.timer and len(self.queue.completed_queue) == self.num_urls:
                end = datetime.now()
                print(f"TASK FINISHED: Scraping {self.num_urls} urls takes {(end - self.start).total_seconds():.1f}s.")
                print(f"               Average process time is {sum(self.time_per_url)/len(self.time_per_url):.1f}s.")
            # We need to save the state after a task is finished
            self.save_state()

    def ReceiveComment(self, request: crawl_pb2.Comment, context):
        """Receive Comment from workers"""
        # Some videos have no comments, so we need to check if the request is bad
        # If it is, we set the url_finished to be True and no longer need the comments from that video
        if request.isBad:
            self.url_finished[request.url] = True
            return crawl_pb2.Response(success=0)
        print(
            f"Worker {request.worker_id} sent comment [{request.sequence}] [{request.content[:5]}...]"
        )
        self.output[request.url].append(request.content)
        # Check if the length of the comments is equal to the top_comments
        # If it is, we set the url_finished to be True
        if request.sequence == self.top_comments - 1:
            self.url_finished[request.url] = True
        return crawl_pb2.Response(success=1)

    def TaskStream(self, request: crawl_pb2.Worker, context):
        """Stream the crawl messages"""
        while True:
            # if self.tasks[request.number] and self.worker_status[request.number]:
            # we stream the messages to the user until the buffer is empty
            while len(self.tasks[request.number]) > 0:
                n = self.tasks[request.number].pop(0)
                # print(n)
                msg = crawl_pb2.Task(
                    username=n["username"],
                    url=n["url"],
                    timestamp=n["timestamp"],
                )
                yield msg
                self.save_state()

    def save_state(self):
        """Save the state of the server"""
        # create a folder for the server state
        if not os.path.exists("logs"):
            os.mkdir("logs")
        with open("logs/tasks.json", "w") as f:
            json.dump(self.tasks, f)
        with open("logs/output.json", "w") as f:
            json.dump(self.output, f)
        with open("logs/queue.json", "w") as f:
            json.dump(self.queue.__dict__, f)
        with open("logs/url_finished.json", "w") as f:
            json.dump(self.url_finished, f)
        # save the number of workers
        with open("logs/worker_nums.json", "w") as f:
            d = {"number": self.worker_nums}
            json.dump(d, f)

    def SendHeartbeat(self, request, context):
        """Send heartbeat to slave server"""
        res = crawl_pb2.Ack(content="ack")
        return res


def serve(host, port, top_comments):
    """Run the server"""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    crawl_server = CrawlServer(top_comments, num_urls=30, timer=True)
    crawl_pb2_grpc.add_CrawlServicer_to_server(crawl_server, server)
    print("Starting server...")
    server.add_insecure_port(f"{host}:{port}")
    server.start()
    print("Start successful")
    server.wait_for_termination()
    return server


if __name__ == "__main__":
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

    # read the host and port from config.json
    with open("src/config.json", "r") as f:
        config = json.load(f)
    host = config["master"]["host"]
    port = config["master"]["port"]
    # delete log folder if existed
    if os.path.exists("logs"):
        shutil.rmtree("logs")
    threading.Thread(target=serve, args=(host, port, top_comments), daemon=True).start()
    while True:
        pass
