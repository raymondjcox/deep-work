#!/usr/bin/env python3

import argparse
from deep_work.work import DeepWork
from deep_work import constants

def main():
    """Application entry point"""
    parser = _build_parser()
    args = parser.parse_args()
    deep_work = DeepWork(constants.DEEP_PATH, constants.VISUAL_PATH)
    try:
        args.func(deep_work, args)
    except AttributeError:
        parser.print_help()

def _build_parser():
    parser = argparse.ArgumentParser(description='Facilitate deep work schedule')
    subparsers = parser.add_subparsers()

    start_parser = subparsers.add_parser('start')
    start_parser.set_defaults(func=_start)
    start_parser.add_argument('--description', '-d', help='Adds an optional description')

    stop_parser = subparsers.add_parser('stop')
    stop_parser.set_defaults(func=_stop)

    clear_parser = subparsers.add_parser('clear')
    clear_parser.set_defaults(func=_clear)

    log_parser = subparsers.add_parser('log')
    log_parser.set_defaults(func=_log)
    log_parser.add_argument('--json', '-j', action='store_true', help='Prints log in json')

    update_parser = subparsers.add_parser('update')
    update_parser.set_defaults(func=_update)

    return parser

def _start(deep_work, args):
    start_time = deep_work.start(args.description)
    desc = args.description
    if not desc:
        desc = ''
    print('Started deep working at {} {}'.format(start_time.strftime('%I:%M%p'), desc))

def _stop(deep_work, _):
    stop_time, [hours, minutes, _] = deep_work.stop()
    print("Stopped deep working at {}".format(stop_time.strftime('%I:%M%p')))
    print("{} hours {} minutes".format(hours, minutes))

def _clear(deep_work, _):
    deep_work.clear()
    print('Deep log cleared!')

def _log(deep_work, args):
    if args.json:
        print(deep_work.json())
    else:
        print(deep_work.log())

def _update(deep_work, _):
    deep_work.update_visual()
    print('Visualization updated!')

if __name__ == "__main__":
    main()
