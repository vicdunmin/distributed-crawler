import threading
import time
from ..src.server import CrawlServer, crawl_pb2


def test_init_state():
    top_comments = 10
    n = 20
    server = CrawlServer(top_comments=top_comments, num_urls=n)
    assert server.top_comments == top_comments
    assert len(server.queue.pending_queue) == 0
    assert len(server.queue.work_queue) == n

def test_receive_comments():
    """test if server can receive comments"""
    top_comments = 10
    n = 20
    server = CrawlServer(top_comments=top_comments, num_urls=n)
    comment = "This is a nice video!"
    url = 'ramdom url 0'
    server.ReceiveComment(request=crawl_pb2.Comment(content=comment, sequence=0, url=url, worker_id=0, isBad=0), context=None)

    assert comment in server.output[url]
    assert not server.url_finished[url]

def test_receive_last_comment():
    """test if server can receive the last comment and mark task as done"""
    top_comments = 10
    n = 20
    server = CrawlServer(top_comments=top_comments, num_urls=n)
    comment = "This is a nice video!"
    url = 'ramdom url 1'
    server.ReceiveComment(request=crawl_pb2.Comment(content=comment, sequence=top_comments-1, url=url, worker_id=0, isBad=0), context=None)

    assert comment in server.output[url]
    assert server.url_finished[url]

def test_receive_bad_comments():
    """test if server receive bad comments"""
    top_comments = 10
    n = 20
    server = CrawlServer(top_comments=top_comments, num_urls=n)
    comment = "This is a nice video!"
    url = 'ramdom url 2'
    server.ReceiveComment(request=crawl_pb2.Comment(content=comment, sequence=0, url=url, worker_id=0, isBad=1), context=None)

    assert comment not in server.output[url]
    assert server.url_finished[url]

def test_check_finished_task():
    """test if server can remove finished tasks."""
    top_comments = 10
    n = 20
    server = CrawlServer(top_comments=top_comments, num_urls=n)
    url = 'ramdom url 3'
    server.queue.pending_queue.append(url)
    server.url_finished[url] = True
    server.check_for_finished_task(url, worker_id=0)
    assert url not in server.queue.pending_queue
    assert url in server.queue.completed_queue

def test_check_unfinished_task():
    """test if server can remove unfinished tasks."""
    top_comments = 10
    n = 20
    server = CrawlServer(top_comments=top_comments, num_urls=n)
    url = 'ramdom url 4'
    server.queue.pending_queue.append(url)
    server.url_finished[url] = False
    threading.Thread(
            target=server.check_for_finished_task, args=(url,0), daemon=True
        ).start()
    time.sleep(21) # sleep for more than timeout(20s)
    server.url_finished[url] = True
    time.sleep(1)
    
    assert url not in server.queue.pending_queue
    assert url not in server.queue.completed_queue
    assert url in server.queue.work_queue
    
