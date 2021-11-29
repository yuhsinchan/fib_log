import paho.mqtt.client as mqtt

from logging import log
import os
import os.path as osp
import sys
import threading

BUILD_DIR = osp.join(osp.dirname(osp.abspath(__file__)), "build/service/")
sys.path.insert(0, BUILD_DIR)
import argparse

import grpc
from concurrent import futures

import log_pb2
import log_pb2_grpc

history = []


class logServicer(log_pb2_grpc.logServicer):
    def __init__(self):
        pass

    def Query(self, request, context):
        response = log_pb2.LogResponse()
        response.value = str(history)

        return response


def runLogServer():
    args = {"ip": "0.0.0.0", "port": 8081}

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    servicer = logServicer()
    log_pb2_grpc.add_logServicer_to_server(servicer, server)

    try:
        server.add_insecure_port(f"{args['ip']}:{args['port']}")
        server.start()
        print(f"Run gRPC Server at {args['ip']}:{args['port']}")
        server.wait_for_termination()
    except KeyboardInterrupt:
        pass


def on_message(client, obj, msg):
    print(f"GET: {msg.payload.decode()}")
    history.append(int(msg.payload.decode()))


def subscribe(args):
    # Establish connection to mqtt broker
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(host=args["ip"], port=args["port"])
    client.subscribe("order", 0)

    try:
        client.loop_forever()
    except KeyboardInterrupt as e:
        pass


if __name__ == "__main__":
    t = threading.Thread(target=subscribe, args=({"ip": "localhost", "port": 1883},))
    t.start()
    runLogServer()
