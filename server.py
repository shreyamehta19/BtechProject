
"""The Python implementation of the GRPC helloworld.Greeter server."""

from concurrent import futures
import logging

import grpc

import transfer_pb2
import transfer_pb2_grpc


class Greeter(transfer_pb2_grpc.GreeterServicer):

    def SayHello(self, request, context):
        #return helloworld_pb2.HelloReply(message='Hello, %s!' % request.name)
	fileName = "Native2ASCIIEncoding.txt"
	fp = open(fileName, "r")
	text = fp.readlines()
	UAST_text = ''.join(text)
	return transfer_pb2.HelloReply(message=UAST_text)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    transfer_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
