"""Display file status

SYNOPSIS:
    stat [-L] <FILE>

OPTIONS:
    -L
        follow symbolic links

DESCRIPTION:
    Get remote file status informations

AUTHOR:
    nil0x42 <http://goo.gl/kb2wf>
"""

import sys
import stat

from api import plugin
from api import server
from api import environ

from ui.color import colorize
from datatypes import ByteSize


def println(name, content):
    print(colorize("%Bold", "{:>15}: ".format(name)) + str(content))


def device_repr(devno):
    return hex(devno)[2:] + 'h/' + str(devno) + 'd'


def mode_perms(mode):
    octal = oct(stat.S_IMODE(mode))[2:].zfill(4)
    literal = stat.filemode(mode)
    return "%s (%s)" % (octal, literal)


def mode_filetype(mode):
    mode = stat.S_IFMT(mode)
    dic = {
            stat.S_ISFIFO: "fifo file",
            stat.S_ISCHR: "character device",
            stat.S_ISDIR: "directory",
            stat.S_ISBLK: "block device",
            stat.S_ISREG: "regular file",
            stat.S_ISLNK: "symbolic link",
            stat.S_ISSOCK: "socket",
            stat.S_ISDOOR: "door",
            }
    for test_func, name in dic.items():
        if test_func(mode):
            return name
    return "???"


def is_device(mode):
    mode = stat.S_IFMT(mode)
    return stat.S_ISCHR(mode) or stat.S_ISBLK(mode)


def dev_name(rdev):
    major = ((rdev >> 8) & 0xfff) | ((rdev >> 32) & ~0xfff)
    minor = (rdev & 0xff) | ((rdev >> 12) & ~0xff)
    return "%s,%s" % (major, minor)
    

if len(plugin.argv) == 2:
    follow_links = False
    relative_path = plugin.argv[1]
elif len(plugin.argv) == 3 and plugin.argv[1] == '-L':
    follow_links = True
    relative_path = plugin.argv[2]
else:
    sys.exit(plugin.help)

absolute_path = server.path.abspath(relative_path)
# FIX: diferenciate /bin/ from /bin for interpreting symlinks on linux
if not environ['PLATFORM'].startswith("win"):
    if not absolute_path.endswith("/") and relative_path.endswith("/"):
        absolute_path += "/"

payload = server.payload.Payload("payload.php")
payload['FILE'] = absolute_path
payload['FOLLOW_LINKS'] = follow_links

r = payload.send()

println("File Name", r["file_repr"])

println("File Size", ByteSize(r["size"]))

if r["blocks"] != -1:
    println("Blocks of 512b", r["blocks"])

if r["blksize"] != -1:
    println("I/O Block Size", r["blksize"])

println("File Type", mode_filetype(r["mode"]))

if r["ino"] != 0:
    println("Inode Number", r["ino"])

println("Number of Links", r["nlink"])

println("Device", r["dev"])

if is_device(r["mode"]):
    println("Device Name", dev_name(r["rdev"]))

if "posix_pwuid" in r.keys():
    println("Access Mode", mode_perms(r["mode"]))
    println("UID Owner", "%d (%s)" % (r["uid"], r["posix_pwuid"]))
    println("GID Owner", "%d (%s)" % (r["gid"], r["posix_grgid"]))


println("Readable", r["readable"])
println("Writable", r["writable"])

println("Accessed", r["atime"])
println("Modified", r["mtime"])
println("Changed", r["ctime"])
