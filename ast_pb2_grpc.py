# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import ast_pb2 as ast__pb2


class AstStub(object):
  """AST service definition.
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.getAst = channel.unary_unary(
        '/astproto.Ast/getAst',
        request_serializer=ast__pb2.AstRequest.SerializeToString,
        response_deserializer=ast__pb2.Node.FromString,
        )
    self.getAstDiff = channel.unary_unary(
        '/astproto.Ast/getAstDiff',
        request_serializer=ast__pb2.AstDiffRequest.SerializeToString,
        response_deserializer=ast__pb2.AstDiff.FromString,
        )
    self.getAstClusterDiff = channel.unary_unary(
        '/astproto.Ast/getAstClusterDiff',
        request_serializer=ast__pb2.AstDiffRequest.SerializeToString,
        response_deserializer=ast__pb2.AstClusterDiff.FromString,
        )


class AstServicer(object):
  """AST service definition.
  """

  def getAst(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def getAstDiff(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def getAstClusterDiff(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_AstServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'getAst': grpc.unary_unary_rpc_method_handler(
          servicer.getAst,
          request_deserializer=ast__pb2.AstRequest.FromString,
          response_serializer=ast__pb2.Node.SerializeToString,
      ),
      'getAstDiff': grpc.unary_unary_rpc_method_handler(
          servicer.getAstDiff,
          request_deserializer=ast__pb2.AstDiffRequest.FromString,
          response_serializer=ast__pb2.AstDiff.SerializeToString,
      ),
      'getAstClusterDiff': grpc.unary_unary_rpc_method_handler(
          servicer.getAstClusterDiff,
          request_deserializer=ast__pb2.AstDiffRequest.FromString,
          response_serializer=ast__pb2.AstClusterDiff.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'astproto.Ast', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
