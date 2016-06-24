import requests

from util import hook
from sets import Set


def make_request(tail):
    url = 'http://192.168.1.38:5000/ir/%s' % tail
    r = requests.post(url)
    if 'okay' in r.text:
        return
    return 'IR Server is not happy'

@hook.command('tv')
def tv_power(inp):
    t = inp.lower().strip()
    toggles = Set(['pwr', 'on', 'off', 'toggle'])
    channels = Set(['fox', 'nbc', 'cbs', 'bot', 'chrome'])
    if t in toggles:
        make_request('tv/on')
        return 'Toggling TV power'
    elif t in channels:
        make_request('tv?channel=%s' % t)
        return 'Changing TV to %s' % t
    elif 'input' in t:
        make_request('tv/input')
        return 'Next input'
    else:
        return 'wut?'

@hook.command('sound')
def soundbar_power(inp):
    t = inp.lower().strip()
    toggles = Set(['pwr', 'on', 'off', 'toggle'])
    channel = Set(['optical', 'bot'])
    if t in toggles:
        make_request('soundbar/on')
        return 'Toggling soundbar power'
    elif t in channel:
        make_request('soundbar?button=%s' % t)
        return 'Changing soundbar to %s' % t
    else:
        return 'wut?'

@hook.command('vol')
def volume_commands(inp):
    t = inp.lower()
    if 'up' in t or '+' in t :
        make_request('soundbar?button=vol_up')
        return 'Raising volume'
    elif 'down' in t or '-' in t:
        make_request('soundbar?button=vol_down')
        return 'Lowering volume'
    elif 'mute' in t:
        make_request('soundbar?button=mute')
        return 'Muting soundbar'
    else:
        return 'wut?'
