import re
from util import hook

WIDE_MAP = dict((i, i + 0xFEE0) for i in xrange(0x21, 0x7F))
WIDE_MAP[0x20] = 0x3000

FUTURE_RE = (r"%(.*?)%", re.I)

def is_odd(num):
    return num & 0x1

def widen(s):
    return unicode(s).translate(WIDE_MAP)

def send(conn, chan, line):
    out = "PRIVMSG %s : %s" % (chan, line.decode('utf-8'))
    conn.send(out)

@hook.command
def ft(inp):
    caps = inp.upper()
    future = widen(caps.decode('utf-8')).encode('utf-8')
    return future

@hook.regex(*FUTURE_RE)
def secrit_future(match, conn=None, input=None, nick=''):
    user_message = input.get('msg')
    words = input.get('msg').split(' ')
    fwd_chan = None
    try:
        if words[0][0] == "#":
            fwd_chan = words[0]
            user_message = ' '.join(words[1:])
    except Exception as e:
        pass
    user_message = user_message.split('%')
    for i, val in enumerate(user_message):
        if is_odd(i):
            user_message[i] = widen(user_message[i].decode('utf-8')).encode('utf-8')
        else:
            user_message[i] = user_message[i].encode('utf-8')
    reply =  ''.join(user_message)
    if fwd_chan != None:
        send(conn, fwd_chan, reply)
        return
    return reply
