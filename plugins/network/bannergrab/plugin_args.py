import argparse
import sys
import ui.output


def help_format_bannergrab(prog):
    kwargs = dict()
    kwargs['width'] = ui.output.columns()
    kwargs['max_help_position'] = 34
    format = argparse.HelpFormatter(prog, **kwargs)
    return (format)

def parse(args):
    parser = argparse.ArgumentParser(prog="scan", add_help=False, usage=argparse.SUPPRESS)
    parser.formatter_class = help_format_bannergrab
    parser.add_argument('-p', '--port',
                        metavar="<PORT>", default='20-10000')
    parser.add_argument('-t', '--timeout', type=float,
                        metavar="<SECONDES>", default=0.2)
    parser.add_argument('address')
    options = vars(parser.parse_args(args))
    options['port'] = parse_port(options['port'])

    return options

def parse_port(input):
    if input.count('-') == 1:
        data = input.split('-')
    else:
        data = [input, input]

    try:
        data = [int(x) for x in data]
    except ValueError:
        sys.exit("Illegal port specifications")

    if min(data) < 0 or max(data) > 65535:
        sys.exit("Ports specified must be between 0 and 65535 inclusive")
    if data[0] > data[1]:
        sys.exit("Your port range %d-%d is backwards. Did you mean %d-%d?"
                 % (data[0], data[1], data[1], data[0]))

    return data
