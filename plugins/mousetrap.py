from util import hook
import os

@hook.command('mousetrap')
@hook.command('mouse')
@hook.command('mt')
def mousetrap(inp):
    try:
        inp = inp.lower().strip()
        x, y = inp.split(',')
    except:
        x = y = 0
    os.popen('DISPLAY=:0 xdotool mousemove --sync %s %s' % (x, y))
    return 'Gotcha bitch!'
