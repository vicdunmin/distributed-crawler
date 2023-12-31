# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from . import crawl_pb2 as crawl__pb2


class CrawlStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CreateWorker = channel.unary_unary(
                '/grpc.Crawl/CreateWorker',
                request_serializer=crawl__pb2.Worker.SerializeToString,
                response_deserializer=crawl__pb2.Response.FromString,
                )
        self.TaskStream = channel.unary_stream(
                '/grpc.Crawl/TaskStream',
                request_serializer=crawl__pb2.Worker.SerializeToString,
                response_deserializer=crawl__pb2.Task.FromString,
                )
        self.SentTask = channel.unary_unary(
                '/grpc.Crawl/SentTask',
                request_serializer=crawl__pb2.Task.SerializeToString,
                response_deserializer=crawl__pb2.Response.FromString,
                )
        self.SendHeartbeat = channel.unary_unary(
                '/grpc.Crawl/SendHeartbeat',
                request_serializer=crawl__pb2.Worker.SerializeToString,
                response_deserializer=crawl__pb2.Ack.FromString,
                )
        self.LogTask = channel.unary_stream(
                '/grpc.Crawl/LogTask',
                request_serializer=crawl__pb2.Worker.SerializeToString,
                response_deserializer=crawl__pb2.Task.FromString,
                )
        self.ReceiveComment = channel.unary_unary(
                '/grpc.Crawl/ReceiveComment',
                request_serializer=crawl__pb2.Comment.SerializeToString,
                response_deserializer=crawl__pb2.Response.FromString,
                )


class CrawlServicer(object):
    """Missing associated documentation comment in .proto file."""

    def CreateWorker(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def TaskStream(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SentTask(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SendHeartbeat(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def LogTask(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ReceiveComment(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_CrawlServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'CreateWorker': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateWorker,
                    request_deserializer=crawl__pb2.Worker.FromString,
                    response_serializer=crawl__pb2.Response.SerializeToString,
            ),
            'TaskStream': grpc.unary_stream_rpc_method_handler(
                    servicer.TaskStream,
                    request_deserializer=crawl__pb2.Worker.FromString,
                    response_serializer=crawl__pb2.Task.SerializeToString,
            ),
            'SentTask': grpc.unary_unary_rpc_method_handler(
                    servicer.SentTask,
                    request_deserializer=crawl__pb2.Task.FromString,
                    response_serializer=crawl__pb2.Response.SerializeToString,
            ),
            'SendHeartbeat': grpc.unary_unary_rpc_method_handler(
                    servicer.SendHeartbeat,
                    request_deserializer=crawl__pb2.Worker.FromString,
                    response_serializer=crawl__pb2.Ack.SerializeToString,
            ),
            'LogTask': grpc.unary_stream_rpc_method_handler(
                    servicer.LogTask,
                    request_deserializer=crawl__pb2.Worker.FromString,
                    response_serializer=crawl__pb2.Task.SerializeToString,
            ),
            'ReceiveComment': grpc.unary_unary_rpc_method_handler(
                    servicer.ReceiveComment,
                    request_deserializer=crawl__pb2.Comment.FromString,
                    response_serializer=crawl__pb2.Response.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'grpc.Crawl', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Crawl(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def CreateWorker(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/grpc.Crawl/CreateWorker',
            crawl__pb2.Worker.SerializeToString,
            crawl__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def TaskStream(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/grpc.Crawl/TaskStream',
            crawl__pb2.Worker.SerializeToString,
            crawl__pb2.Task.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SentTask(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/grpc.Crawl/SentTask',
            crawl__pb2.Task.SerializeToString,
            crawl__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SendHeartbeat(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/grpc.Crawl/SendHeartbeat',
            crawl__pb2.Worker.SerializeToString,
            crawl__pb2.Ack.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def LogTask(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/grpc.Crawl/LogTask',
            crawl__pb2.Worker.SerializeToString,
            crawl__pb2.Task.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ReceiveComment(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/grpc.Crawl/ReceiveComment',
            crawl__pb2.Comment.SerializeToString,
            crawl__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
