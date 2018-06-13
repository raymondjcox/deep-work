#!/usr/local/bin/python3

import sys
from deep_work.work import DeepWork
from deep_work import constants

def usage_error():
    """Exits out on invalid usage"""
    sys.exit('usage: deep <{}>'.format(' | '.join(constants.VALID_OPS)))

def main():
    """Application entry point"""
    if len(sys.argv) < 2 or sys.argv[1].lower() not in constants.VALID_OPS:
        usage_error()

    operation = sys.argv[1].lower()
    deep_work = DeepWork(constants.DEEP_PATH)

    if operation == constants.CLEAR:
        deep_work.clear()
    elif operation == constants.JSON:
        print(deep_work.to_json())
    elif operation == constants.LOG:
        print(deep_work.log())
    elif operation == constants.START:
        deep_work.start()
    else:
        deep_work.stop()

if __name__ == "__main__":
    main()
