#!/usr/bin/env python
# -*- coding: utf-8 -*-

import zmq
import os
from cmd2 import Cmd

global spine_input
global spine_output

zmq_ctx = zmq.Context()


class AlfredCli(Cmd):
    def do_publish_to(self, line):
        connect_publish(line)

    def do_subscribe_to(self, line):
        connect_subscribe(line)

    def do_msg(self, line):
        global spine_input
        spine_input.send(line)


def connect_publish(target_socket):
    global spine_input

    spine_input = zmq_ctx.socket(zmq.PUSH)
    spine_input.connect(target_socket)

    print "Connected to: " + target_socket


def connect_subscribe(target_socket):
    global spine_output

    spine_output = zmq_ctx.socket(zmq.SUB)
    spine_output.setsockopt(zmq.SUBSCRIBE, '/alfred/cli-output/')
    spine_output.connect(target_socket)

    print "Subscribed to: " + target_socket


def main():
    try:
        if os.environ['ALFRED_SPINE_INPUT']:
            connect(os.environ['ALFRED_SPINE_INPUT'])

        AlfredCli().cmdloop()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    AlfredCli().cmdloop()
