import argparse
from api import plugin
import ui.output


def help_format_network_scan(prog):
    kwargs = dict()
    kwargs['width'] = ui.output.columns()
    kwargs['max_help_position'] = 34
    format = argparse.HelpFormatter(prog, **kwargs)
    return (format)


def parse(args):
    parser = argparse.ArgumentParser(prog="scan", add_help=False, usage=argparse.SUPPRESS)
    parser.formatter_class = help_format_network_scan
    parser.add_argument('-p', '--port',
                        metavar="<PORT>", default='20-10000')
    parser.add_argument('-t', '--timeout', type=float,
                        metavar="<SECONDES>", default=0.2)
    parser.add_argument('address')
    options = vars(parser.parse_args(args))
    options['port'] = parse_port(options['port'])

    return options

def parse_port(input):
    if '-' in input:
        return input.split('-')
    else:
        return (input, input)