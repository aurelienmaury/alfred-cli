#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import zmq
import os
from cmd2 import Cmd

global push_sock
global spine_output
global sub_thread_running
global sub_thread

sub_thread = None

sub_thread_running = False

class SubThread(threading.Thread):
    def run(self):
        global spine_output
        global sub_thread_running
        while sub_thread_running:
            print spine_output.recv_string()



class AlfredCli(Cmd):
    def do_push_to(self, line):
        connect_push(line)

    def do_subscribe_to(self, line):
        connect_subscribe(line)

    def do_msg(self, line):
        global push_sock
        push_sock.send_string(line)
        print "sent "+line


def connect_push(target_socket):
    global push_sock

    push_sock = zmq.Context().socket(zmq.PUSH)
    push_sock.connect(target_socket)

    print "Pushing to: " + target_socket


def connect_subscribe(target_socket):
    global spine_output
    global sub_thread
    global sub_thread_running
    sub_thread_running = False

    print "joining"
    if sub_thread:
        sub_thread.stop()
        sub_thread.join()

    zmq_ctx = zmq.Context()
    spine_output = zmq_ctx.socket(zmq.SUB)
    spine_output.setsockopt(zmq.SUBSCRIBE, '/alfred/cli-output/')
    spine_output.connect(target_socket)


    sub_thread_running = True
    sub_thread = SubThread()
    sub_thread.start()
    print "Subscribed to: " + target_socket


def main():
    try:
        AlfredCli().cmdloop()
    except KeyboardInterrupt:
        global sub_thread_running
        global sub_thread
        sub_thread_running = False
        if sub_thread:
            sub_thread.stop()
        sub_thread.join()
        pass


if __name__ == '__main__':
    main()
