#!/usr/bin/env python
# -*- coding: utf-8 -*-

import zmq
import sys
import os
from cmd2 import Cmd

target_socket = sys.argv[1]
target_source = "cli"

if not target_socket:
    target_socket = os.environ['ALFRED_SPINE_INPUT']
    target_source = "env"
    if not target_socket:
        sys.exit("Could not find Alfred's socket from cli nor env var (ALFRED_SPINE_INPUT)")

zmq_ctx = zmq.Context()
spine_input = zmq_ctx.socket(zmq.PUSH)
spine_input.connect(target_socket)


class AlfredCli(Cmd):

    def do_msg(self, line):
        spine_input.send(line)

if __name__ == '__main__':
    AlfredCli().cmdloop()