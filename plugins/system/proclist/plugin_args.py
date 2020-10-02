import argparse
import ui.output

def help_format_proclist(prog):
    kwargs = dict()
    kwargs['width'] = ui.output.columns()
    kwargs['max_help_position'] = 34
    format = argparse.HelpFormatter(prog, **kwargs)
    return (format)

def parse(args):
    parser = argparse.ArgumentParser(prog="scan", add_help=False, usage=argparse.SUPPRESS)
    options = vars(parser.parse_args(args))    
    return options

