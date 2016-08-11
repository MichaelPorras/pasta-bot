import json
import subprocess
from util import hook

config_keys = json.load(open('config'))
ACCESS_KEY = config_keys.get('ivonna_access_key')
SECRET_KEY = config_keys.get('ivonna_secret_key')
MUTE = False


# NOTE(evanscottgray) order is important when applying this, must be last deco
#                     added to the func. also makes calling @hook.command not
#                     work as intended, you must pass in a name instead.
def muteable(func):
    def inner(arg, conn=None, chan=None):
        if MUTE:
            return 'Fuck off, bot is muted.'
        return func(arg, conn=conn, chan=chan)
    return inner


def _say_words(words):
    cmd = ['node', './plugins/util/lul.js', ACCESS_KEY, SECRET_KEY]
    cmd.extend(words.split(' '))
    print 'running cmd: |%s|' % cmd
    print subprocess.check_output(cmd)


@hook.command('mutesay')
def mute(inp):
    global MUTE
    MUTE = True
    return 'Say Muted'


@hook.command('unmutesay')
def unmute(inp):
    global MUTE
    MUTE = False
    return 'Say Unmuted'


@hook.command('tts')
@muteable
def tts(inp, conn=None, chan=None):
    _say_words(inp)
