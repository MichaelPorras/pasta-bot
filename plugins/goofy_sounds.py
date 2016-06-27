import subprocess
from util import hook

MUTE = False
PLAYER_CMD = 'aplay'
SOUNDS_PATH = './plugins/data/sounds/'
CMD_STR = PLAYER_CMD + ' ' + SOUNDS_PATH


# NOTE(evanscottgray) order is important when applying this, must be last deco
#                     added to the func. also makes calling @hook.command not
#                     work as intended, you must pass in a name instead.
def muteable(func):
    def inner(arg, conn=None, chan=None):
        if MUTE:
            return 'Fuck off, bot is muted.'
        return func(arg, conn=conn, chan=chan)
    return inner


def _playsound(filename):
    path = SOUNDS_PATH + filename
    subprocess.call([PLAYER_CMD, path])


def _send_message(msg, conn, chan):
    out = 'PRIVMSG %s : %s' % (chan, msg.decode('utf-8'))
    conn.send(out)


@hook.command('mutesounds')
def mute(inp):
    global MUTE
    MUTE = True
    return 'Goofy Sounds Muted'


@hook.command('unmutesounds')
def unmute(inp):
    global MUTE
    MUTE = False
    return 'Goofy Sounds Unmuted'


@hook.command('guten')
@hook.command('gutentag')
@hook.command('gutentaag')
@hook.command('gutentaaag')
@hook.command('gutentaaaag')
@muteable
def gutentag(inp, conn=None, chan=None):
    file_name = 'guetentaaaag.wav'
    msg = 'GUETENTAAAAG!'
    _send_message(msg, conn, chan)
    _playsound(file_name)


@hook.command('victory')
@muteable
def victory(inp, conn=None, chan=None):
    file_name = 'victory.wav'
    msg = 'Yay!!'
    _send_message(msg, conn, chan)
    _playsound(file_name)


@hook.command('out')
@muteable
def out(inp, conn=None, chan=None):
    file_name = 'out.wav'
    msg = 'Fuck this shit I\'m out'
    _send_message(msg, conn, chan)
    _playsound(file_name)


@hook.command('inception')
@muteable
def inception(inp, conn=None, chan=None):
    file_name = 'inception.wav'
    msg = 'BRRRRRRRAAAAAWWWWRWRRRMRMRMMRMRMMMMM!!!'
    _send_message(msg, conn, chan)
    _playsound(file_name)


@hook.command('nanas')
@muteable
def nanas(inp, conn=None, chan=None):
    file_name = 'bangnanas.wav'
    msg = 'B-A-N-G-N-A-N-A-S!'
    _send_message(msg, conn, chan)
    _playsound(file_name)


@hook.command('zelda')
@hook.command('secret')
@muteable
def zelda(inp, conn=None, chan=None):
    file_name = 'zelda_secret.wav'
    msg = 'do do do do do do de do.'
    _send_message(msg, conn, chan)
    _playsound(file_name)


@hook.command('in')
@muteable
def janice(inp, conn=None, chan=None):
    file_name = 'hey_janice.wav'
    msg = 'Hey Janice!'
    _send_message(msg, conn, chan)
    _playsound(file_name)


@hook.command('haha')
@hook.command('ostrich')
@muteable
def ostrich(inp, conn=None, chan=None):
    file_name = 'ostrich.wav'
    msg = 'Ha ha.'
    _send_message(msg, conn, chan)
    _playsound(file_name)


@hook.command('doot')
@hook.command('tranny')
@hook.command('spooky')
@hook.command('shemale')
@hook.command('calcium')
@hook.command('skeleton')
@hook.command('dootdoot')
@hook.command('skeletal')
@hook.command('calsiums')
@hook.command('mr_skeletal')
@hook.command('dootskootboogy')
@hook.command('thankyoumrskeletal')
@muteable
def spooky(inp, conn=None, chan=None):
    file_name = 'spooky.wav'
    msg = 'spooky scary skeletons'
    _send_message(msg, conn, chan)
    _playsound(file_name)


@hook.command('pressure')
@muteable
def pressure(inp, conn=None, chan=None):
    file_name = 'pressure.wav'
    msg = 'Dun dun dun dun.'
    _send_message(msg, conn, chan)
    _playsound(file_name)


@hook.command('cd')
@hook.command('can')
@hook.command('cando')
@hook.command('caando')
@hook.command('caandoo')
@muteable
def cando(inp, conn=None, chan=None):
    file_name = 'can_doo.wav'
    msg = 'Caaaaaan Dooooooo!'
    _send_message(msg, conn, chan)
    _playsound(file_name)


@hook.command('trump')
@hook.command('getout')
@hook.command('outoutout')
@muteable
def out_out_out(inp, conn=None, chan=None):
    file_name = 'OUT_OUT_OUT.wav'
    msg = 'OUT! OUT! OUT!'
    _send_message(msg, conn, chan)
    _playsound(file_name)
