"""The Python implementation of the GRPC Ast client."""

from __future__ import print_function

import grpc

import ast_pb2 as ast_pb2
import ast_pb2_grpc as ast_pb2_grpc

import sys

class AstClient(object):
    """
    AST gRPC client.
    """

    def __init__(self, endpoint: str):
        """
        Initializes a new instance of AstClient.
        :param endpoint: The address of the AstClient server, \
               for example "0.0.0.0:50051"
        """
        self._channel = grpc.insecure_channel(endpoint)
        self.stub = ast_pb2_grpc.AstStub(self._channel)

    def parse(self, language: str, contents: str):
        # try:
        response = self.stub.getAst(ast_pb2.AstRequest(language=language, file_content=contents))
        return response
        # except:
        #     e = sys.exc_info() [0]
        #     print("Exception in fetching ast," + str(e))
        #     raise

    def get_ast_diff(self, file_path: str, first_file_content: str, second_file_content: str):
        return self.stub.getAstDiff(ast_pb2.AstDiffRequest(file_path=file_path,
                                                           first_file_content=first_file_content,
                                                           second_file_content=second_file_content))

    def get_ast_cluster_diff(self, file_path: str, first_file_content: str, second_file_content: str):
        return self.stub.getAstClusterDiff(ast_pb2.AstDiffRequest(file_path=file_path,
                                                           first_file_content=first_file_content,
                                                           second_file_content=second_file_content))

    def close(self):
        self._channel.close()


def role_id_to_name(value: int):
    return ast_pb2.Node.Role.Name(value)

