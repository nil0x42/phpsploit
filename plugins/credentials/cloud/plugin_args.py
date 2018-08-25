import argparse
import ui.output


def help_format_cloudcredgrab(prog):
    kwargs = dict()
    kwargs['width'] = ui.output.columns()
    kwargs['max_help_position'] = 34
    format = argparse.HelpFormatter(prog, **kwargs)
    return (format)

def parse(args):
    parser = argparse.ArgumentParser(prog="cloudcredgrab", add_help=False, usage=argparse.SUPPRESS)
    parser.formatter_class = help_format_cloudcredgrab
    parser.add_argument('-u', '--username',
                        metavar="<USER>", default=None)
    parser.add_argument('platform')
    options = vars(parser.parse_args(args))
