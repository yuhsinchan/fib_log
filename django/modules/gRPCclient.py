import os
import os.path as osp
import sys

BUILD_DIR = osp.join(osp.dirname(osp.abspath(__file__)), "../../gRPC/build/service/")
print(BUILD_DIR)
sys.path.insert(0, BUILD_DIR)
import argparse

import grpc
import fib_pb2
import fib_pb2_grpc
import log_pb2
import log_pb2_grpc

import paho.mqtt.client as mqtt

client = mqtt.Client()
client.connect(host="localhost", port=1883)
client.loop_start()


def grpcFib(args):
    host = f"{args['ip']}:{args['port']}"
    print(host)
    client.publish(topic="order", payload=args["order"])
    with grpc.insecure_channel(host) as channel:
        stub = fib_pb2_grpc.FibCalculatorStub(channel)

        request = fib_pb2.FibRequest()
        request.order = args["order"]

        response = stub.Compute(request)
        return response.value


def grpcLog(args):
    host = f"{args['ip']}:{args['port']}"
    print(host)
    with grpc.insecure_channel(host) as channel:
        stub = log_pb2_grpc.logStub(channel)

        request = log_pb2.LogRequest()

        response = stub.Query(request)
        return response.value
