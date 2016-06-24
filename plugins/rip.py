import re
import time
from util import hook, user
from collections import defaultdict

RIP_RE = (r"\brip\b|\bRIP\b", re.I)
F_RE = (r"\bf\b|\bF\b", re.I)

RESPECTS = defaultdict(int)

def send(conn, chan, line):
    out = "PRIVMSG %s :\x01ACTION %s\x01" % (chan, line)
    conn.send(out)

@hook.regex(*RIP_RE)
def rip_mod(match, conn=None, chan=None):
    if chan in RESPECTS:
        return

    send(conn, chan, 'Press F to pay respects')
    RESPECTS[chan]=0
    time.sleep(10)
    r_paid = RESPECTS.get(chan)
    del RESPECTS[chan]
    if r_paid == 1:
        return '1 respect has been paid'
    return '%d respects have been paid' % r_paid

@hook.regex(*F_RE)
def f_mod(match, chan=None):
    if chan in RESPECTS:
        RESPECTS[chan] += 1
