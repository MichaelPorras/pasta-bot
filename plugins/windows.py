import os
import re
import time
import socket
from util import hook


# TODO: make this autodetect either google-chrome or chromium-browser
CHROME_CMD = 'google-chrome'
HANGOUT_URL = 'h.clev.club'
HOSTNAME = socket.gethostname()
MRSKELTAL = ['▒▒▒░░░░░░░░░░▄▐░░░░',
             '▒░░░░░░▄▄▄░░▄██▄░░░',
             '░░░░░░▐▀█▀▌░░░░▀█▄░',
             '░░░░░░▐█▄█▌░░░░░░▀█▄',
             '░░░░░░░▀▄▀░░░▄▄▄▄▄▀▀',
             '░░░░░▄▄▄██▀▀▀▀░░░░░',
             '░░░░█▀▄▄▄█░▀▀░░░░░░',
             '░░░░▌░▄▄▄▐▌▀▀▀░░░░░',
             '░▄░▐░░░▄▄░█░▀▀░░░░░',
             '░▀█▌░░░▄░▀█▀░▀░░░░░',
             '░░░░░░░░▄▄▐▌▄▄░░░░░',
             '░░░░░░░░▀███▀█░▄░░░',
             '░░░░░░░▐▌▀▄▀▄▀▐▄░░░',
             '░░░░░░░▐▀░░░░░░▐▌░░',
             '░░░░░░░█░░░░░░░░█░░',
             '░░░░░░▐▌░░░░░░░░░█░']

DANCE = ['░░┌──┐░░░░░░░░░░┌──┐░░'
         '░╔╡▐▐╞╝░░┌──┐░░╔╡▐▐╞╝░'
         '░░└╥╥┘░░╚╡▌▌╞╗░░└╥╥┘░░'
         '░░░╚╚░░░░└╥╥┘░░░░╚╚░░░'
         '░░░░░░░░░░╝╝░░░ DANCE PARTY']

SPOOKY_RE = (r"\bgentle spooks\b", re.I)


def send(conn, chan, line):
    out = "PRIVMSG %s :\x01ACTION %s\x01" % (chan, line)
    conn.send(out)


def ascii_spam(conn, chan, spam):
    for line in spam:
        out = "PRIVMSG %s : %s " % (chan, line.decode('utf-8'))
        conn.send(out)
        time.sleep(.3)


def check_windows(title=None):
    open_windows = os.popen('DISPLAY=:0 wmctrl -l').readlines()
    if not title:
        return open_windows
    for win in open_windows:
        if title in win:
            return True
    return False


@hook.command('ow')
def open_windows(inp, conn=None, chan=None):
    open_windows = check_windows()
    if len(open_windows) == 0:
        return 'No open windows'
    for line in open_windows:
        title = line.split(HOSTNAME)[1]
        send(conn, chan, title)


@hook.command('cw')
def close_window(inp):
    target = inp.lower().strip()
    if not target:
        return 'Please specify window to close'
    if target == 'all':
        open_windows = os.popen('DISPLAY=:0 wmctrl -l').readlines()
        for line in open_windows:
            if 'Google Hangouts' not in line:
                hex_val = line.split('0 %s' % HOSTNAME)[0].strip()
                os.popen('DISPLAY=:0 wmctrl -ic "%s"' % hex_val)
        return 'Closing all windows'
    else:
        os.popen('DISPLAY=:0 wmctrl -c "%s"' % target)
        return 'Closing %s' % target


@hook.command('ls')
def launch_site(inp):
    os.popen('DISPLAY=:0 %s -new-window %s &' % (CHROME_CMD, inp))
    return 'Launching site %s' % inp


@hook.command('lyt')
def launch_youtube(inp):
    url_pieces = inp.split('/watch')
    new_url = '%s/tv#/watch%s' % (url_pieces[0], url_pieces[1])
    os.popen('DISPLAY=:0 %s -new-window %s &' % (CHROME_CMD, new_url))
    return 'Launching YouTube in TV MODE'


@hook.command('fw')
def focus_window(inp):
    os.popen('DISPLAY=:0 wmctrl -a %s &' % inp)
    return 'Focusing window %s' % inp


@hook.command('max')
def maximize_window(inp):
    os.popen(('DISPLAY=:0 wmctrl -r :ACTIVE: -b '
              'toggle,maximized_vert,maximized_horz &'))
    return 'Maximizing current window'


@hook.command('kp')
def key_press(inp):
    os.popen('DISPLAY=:0 xdotool key %s' % inp)
    return 'Pressing key: %s' % inp


@hook.regex(*SPOOKY_RE)
def gentle_doot(match, conn=None, chan=None):
    spooks = 'https://youtu.be/dMXBwKOfULY'
    os.popen('DISPLAY=:0 %s -new-window %s &' % (CHROME_CMD, spooks))
    ascii_spam(conn, chan, MRSKELTAL)


@hook.command('circle')
def launch_circle_dance(conn=None, chan=None):
    dance_vid = 'https://www.youtube.com/v/nUqrafe46B8&autoplay=1&'
                'loop=1&controls=0&showinfo=0&playlist=nUqrafe46B8'
    os.popen('DISPLAY=:0 %s -new-window %s &' % (CHROME_CMD, dance_vid))
    ascii_spam(conn, chan, DANCE)


@hook.command('hstart')
def hangout_start(inp):
    if check_windows('Google Hangouts'):
        return 'Hangouts is already running'
    os.popen('DISPLAY=:0 %s -new-window %s &' % (CHROME_CMD, HANGOUT_URL))
    return 'Starting Hangouts'


@hook.command('hkill')
def hangout_kill(inp):
    if not check_windows('Google Hangouts'):
        return 'Hangouts is not running'
    os.popen('DISPLAY=:0 wmctrl -c Google Hangouts')
    return 'Killing hangouts'


@hook.command('hstatus')
def hangout_status(inp):
    if not check_windows('Google Hangouts'):
        return 'Hangouts is not running'
    return 'Hangouts is running'
