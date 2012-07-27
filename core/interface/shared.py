import os

# core command: clear
def do_clear(self, line):
    cmd = ['clear','cls'][os.name == 'nt']
    os.system(cmd)
