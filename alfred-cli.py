#!/usr/bin/env python
# -*- coding: utf-8 -*-

import zmq
import threading

from cmd2 import Cmd


class AlfredCli(Cmd):
    spine_input = None
    spine_output = None
    spine_listener = None

    def do_push_to(self, line):
        self.spine_input = zmq.Context().socket(zmq.PUSH)
        self.spine_input.connect(line)
        self.poutput("Pushing to: " + line)

    def do_subscribe_to(self, line):
        if self.spine_listener:
            self.spine_listener.stop()

        self.spine_output = zmq.Context().socket(zmq.SUB)
        self.spine_output.setsockopt(zmq.SUBSCRIBE, '/alfred/cli-output/')
        self.spine_output.connect(line)

        self.spine_listener = SpineListenerThread(self)
        self.spine_listener.start()

        self.poutput("Subscribed to: " + line)

    def do_msg(self, line):
        self.spine_input.send_string(line)


class SpineListenerThread(threading.Thread):
    def __init__(self, father):
        threading.Thread.__init__(self)
        self.father = father
        self.keep_on = False
        self.setDaemon(True)

    def run(self):
        self.keep_on = True
        while self.keep_on:
            try:
                message = self.father.spine_output.recv_string(flags=zmq.NOBLOCK)
                self.father.stdout.write("=> " + message + '\n')
            except zmq.Again:
                pass

    def stop(self):
        self.keep_on = False
        self.join()


def main():
    alfred_cli = AlfredCli()
    try:
        alfred_cli.cmdloop()
    except KeyboardInterrupt:
        pass
        print "\n"


if __name__ == '__main__':
    main()
