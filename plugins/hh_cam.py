import re
import time
from util import hook
from util import camera
from functools import partial

HOST = '172.16.111.245'
WAIT = 1


PRESET_RE = re.compile('\d+')
HOME_RE = re.compile('h.*')

LEFT_RE = re.compile('l.*')
RIGHT_RE = re.compile('r.*')

UP_RE = re.compile('u.*')
DOWN_RE = re.compile('d.*')

IN_RE = re.compile('i.*')
OUT_RE = re.compile('o.*')


# TODO: make this smarter
def _get_cam():
    cam = camera.Camera(host='172.16.111.245')
    return cam


def _send_message(msg, conn, chan):
        out = 'PRIVMSG %s : %s' % (chan, msg.decode('utf-8'))
        conn.send(out)


def _recall_preset(inp, say):
    preset = int(PRESET_RE.match(inp).group(0))

    if preset in xrange(1, 13):
        say('Moving to preset %s' % inp)
        c = _get_cam()
        c.goto_preset(preset)
        time.sleep(WAIT)
    else:
        say('Preset %s does not exist. Please use 1 thru 12' % preset)


def _camera_home(inp, say):
    say('Moving camera to home.')
    c = _get_cam()
    c.home()
    time.sleep(WAIT)


def _camera_pan(inp, say):
    direction = None
    if inp.startswith('l'):
        direction = 'left'

    if inp.startswith('r'):
        direction = 'right'

    duration = 3
    if len(inp.split(' ')) > 1:
        custom_dur = int(inp.split(' ')[-1])
        if custom_dur in xrange(1, 16):
            duration = custom_dur
        else:
            say('I can only move for 15 seconds at a time..')

    say('Panning camera to the %s for %s seconds.' % (direction, duration))
    c = _get_cam()
    c.pan(direction, speed=7)
    time.sleep(duration)
    c.stop()
    time.sleep(WAIT)


def _camera_tilt(inp, say):
    direction = None
    if inp.startswith('u'):
        direction = 'up'

    if inp.startswith('d'):
        direction = 'down'

    duration = 3
    if len(inp.split(' ')) > 1:
        custom_dur = int(inp.split(' ')[-1])
        if custom_dur in xrange(1, 16):
            duration = custom_dur
        else:
            say('I can only move for 15 seconds at a time..')

    say('Tilting camera %s for %s seconds.' % (direction, duration))
    c = _get_cam()
    c.tilt(direction, speed=7)
    time.sleep(duration)
    c.stop()
    time.sleep(WAIT)


def _camera_zoom(inp, say):
    direction = None
    if inp.startswith('i'):
        direction = 'in'

    if inp.startswith('o'):
        direction = 'out'

    duration = 1
    if len(inp.split(' ')) > 1:
        custom_dur = int(inp.split(' ')[-1])
        if custom_dur in xrange(1, 16):
            duration = custom_dur
        else:
            say('I can only move for 15 seconds at a time..')

    say('Zooming camera %s for %s seconds.' % (direction, duration))
    c = _get_cam()
    c.zoom(direction, speed=1)
    time.sleep(duration)
    c.stop()
    time.sleep(WAIT)


@hook.singlethread
@hook.command('c')
def cam_move(inp, conn=None, chan=None):
    say = partial(_send_message, conn=conn, chan=chan)

    if PRESET_RE.match(inp):
        _recall_preset(inp, say)

    if HOME_RE.match(inp):
        _camera_home(inp, say)

    if LEFT_RE.match(inp) or RIGHT_RE.match(inp):
        _camera_pan(inp, say)

    if UP_RE.match(inp) or DOWN_RE.match(inp):
        _camera_tilt(inp, say)

    if IN_RE.match(inp) or OUT_RE.match(inp):
        _camera_zoom(inp, say)
