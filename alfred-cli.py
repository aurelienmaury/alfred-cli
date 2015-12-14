#!/usr/bin/env python
# -*- coding: utf-8 -*-

import zmq
import os
from cmd2 import Cmd

global spine_input


class AlfredCli(Cmd):
    def do_connect(self, line):
        connect(line)

    def do_msg(self, line):
        global spine_input
        spine_input.send(line)


def connect(target_socket):
    zmq_ctx = zmq.Context()
    global spine_input
    spine_input = zmq_ctx.socket(zmq.PUSH)
    spine_input.connect(target_socket)
    print "Connected to: " + target_socket


def main():
    try:
        if os.environ['ALFRED_SPINE_INPUT']:
            connect(os.environ['ALFRED_SPINE_INPUT'])

        AlfredCli().cmdloop()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    AlfredCli().cmdloop()
