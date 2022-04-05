import sys
import site_config
# from pathlib import Path

# from inspect import getargspec, getmembers, isfunction


class Simulator:
    def __init__(self):
        self.messages = []
        self.states = dict()
        for name, store, handler in site_config.sites:
            self.states[name] = SiteState(store, handler)

    def site_exists(self, dest):
        return dest in self.states

    def send_msg(self, dest, msg):
        if self.site_exists(dest):
            self.messages.append((dest, msg))
            return True
        return False


PREFIX = "handler_"
PREFIX_LEN = len(PREFIX)

class SiteState:
    def __init__(self, store, handler):
        self.store = store
        self.handler = handler


def main():
    simulator = Simulator()
    print("has states for: {}".format(set(simulator.states.keys())))
    while True:
        print("available messages: [")
        for i, (dest, msg) in enumerate(simulator.messages):
            print("  [{}] @ {} {}".format(i, dest, msg))
        print("]")

        got = input("Next message to receive: ").split(" ")
        print("got", got)
        if not got:
            continue
        elif got[0] == '!':
            # send
            try: dest, msg = got[1:3]
            except: print("WHEE")
            try: assert(simulator.send_msg(dest, msg))
            except: print("WUH")
        elif got[0] == '?':
            try:
                index = int(got[1])
                dest, msg = simulator.messages.pop(index)
                state = simulator.states[dest]
                state.handler(simulator, state.store, msg)
                print('{} handled msg {}\n'.format(dest, msg))
            except IndexError: print("WEH")
        elif got[0] == "@":
            try:
                dest = got[1]
                state = simulator.states[dest]
                print(state.store)
            except: print("WAR")
        else: print("WHAT??")


if __name__ == "__main__":
    main()