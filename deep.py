#!/usr/local/bin/python3

import argparse
from deep_work.work import DeepWork
from deep_work import constants

def main():
    """Application entry point"""
    parser = argparse.ArgumentParser(description='Facilitate deep work schedule')
    parser.add_argument('action',
                        choices=[constants.START,
                                 constants.STOP,
                                 constants.CLEAR,
                                 constants.LOG,
                                 constants.UPDATE],
                        help='Deep work commands')
    parser.add_argument('--json', '-j', action='store_true', help='Prints log in json')
    args = parser.parse_args()
    process_args(args)

def process_args(args):
    """Takes an action based on the passed in args"""
    action = args.action.lower()
    deep_work = DeepWork(constants.DEEP_PATH, constants.VISUAL_PATH)

    if action == constants.CLEAR:
        deep_work.clear()
        print('Deep log cleared!')
    elif action == constants.UPDATE:
        deep_work.update_visual()
        print('Visualization updated!')
    elif action == constants.LOG:
        if args.json:
            print(deep_work.json())
        else:
            print(deep_work.log())
    elif action == constants.START:
        start_time = deep_work.start()
        print('Started deep working at {}'.format(start_time.strftime('%I:%M%p')))
    else:
        stop_time, [hours, minutes, _] = deep_work.stop()
        print("Stopped deep working at {}".format(stop_time.strftime('%I:%M%p')))
        print("{} hours {} minutes".format(hours, minutes))


if __name__ == "__main__":
    main()
