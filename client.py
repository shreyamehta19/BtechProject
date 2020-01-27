
"""The Python implementation of the GRPC helloworld.Greeter client."""

from __future__ import print_function
import logging

import grpc

import transfer_pb2
import transfer_pb2_grpc


def run():
    
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = transfer_pb2_grpc.GreeterStub(channel)
        response = stub.SayHello(transfer_pb2.HelloRequest(name='you'))
    print(" client received: " + response.message)


if __name__ == '__main__':
    logging.basicConfig()
    run()
