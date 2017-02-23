import time
import sys
import re
from os.path import basename


def cutter(link):
    link = re.sub('-scaled(.*)', '.png', link)
    return link


def folder_name(name):
    forbidden = ['>', '<', ':', '"', '*', '/', '\\', '|', '?']
    name = ''.join(e for e in name if e not in forbidden)
    return name


def deco(t):
    for _ in range(t):
        for c in '/-\|':
            sys.stdout.write('\r' + c)
            sys.stdout.flush()
            time.sleep(0.2)


def img_name(name):
    name = re.sub('-(.*)', '.png', basename(name))
    return name
