import sys
import site_config
from pathlib import Path

from inspect import getargspec, getmembers, isfunction


class Simulator:
    def __init__(self):
        pass

    def send(self, dest, msg):
        pass

PREFIX = "handler_"
PREFIX_LEN = len(PREFIX)

class SiteState:
    def __init__(self, handler):
        self.handler = handler
        self.store = dict()

def initialize_states():
    states = dict()
    for name, member in getmembers(site_config, isfunction):
        if name.startswith(PREFIX) and len(getargspec(member)[0]) == 2:
            states[name[PREFIX_LEN:]] = SiteState(member)
    return states


def main():
    states = initialize_states()
    print("has states for: {}".format(set(states.keys())))
    msg_list = []
    while True:
        print("available messages: [")
        for i, (dest, msg) in enumerate(msg_list):
            print("  [{}] @ {} {}".format(i, dest, msg))
        print("]")

        got = input("Next message to receive: ").split(" ")
        print("got", got)
        if len(got) == 3 and got[0] == "@":
            _, dest, msg = got
            if dest in states:
                print('sending to {} message {}'.format(dest, msg))
                msg_list.append((dest, eval(msg)))
            else:
                print("no state for dest '{}'".format(dest))
        elif len(got) == 1:
            try:
                index = int(got[0])
                dest, msg = msg_list.pop(index)
            except ValueError:
                print("tried to interpret that as an (integer) index of the msg to receive")
                continue
            except IndexError:
                print("no message to receive with that index")
                continue
            state = states[dest]
            state.handler(state.store, msg)

if __name__ == "__main__":
    main()