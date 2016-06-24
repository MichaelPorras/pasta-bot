import mpd
from util import hook

CLIENT = mpd.MPDClient(use_unicode=True)


def check_for_pulse():
    try:
        CLIENT.ping()
    except Exception as e:
        CLIENT.connect('192.168.1.14', 6600)
    return


@hook.command('np')
def now_playing(inp):
    check_for_pulse()
    current_song = CLIENT.currentsong()
    cs_info = '%s by %s on %s %s' %(current_song.get('title'),
                                    current_song.get('artist'),
                                    current_song.get('album'),
                                    current_song.get('date'))
    return cs_info


@hook.command('next')
def next_song(inp):
    check_for_pulse()
    CLIENT.next()
    return 'Next song'


@hook.command('prev')
def prev_song(inp):
    check_for_pulse()
    CLIENT.previous()
    return 'Previous song'


@hook.command('pause')
def pause_music(inp):
    check_for_pulse()
    CLIENT.pause()
    return 'Pausing music'


@hook.command('play')
def play_music(inp):
    check_for_pulse()
    CLIENT.play()
    return 'Playing Music'


@hook.command('stop')
def stop_music(inp):
    check_for_pulse()
    CLIENT.stop()
    return 'Stopping Music'


@hook.command('wn')
def whats_next(inp):
    check_for_pulse()
    cur_sng = CLIENT.currentsong()
    current_pos = cur_sng.get('pos')
    strt = str(int(current_pos)+1)
    en = str(int(current_pos)+4)
    next_lst = CLIENT.playlistinfo('%s:%s' % (strt, en))
    up_next = ""
    for song in next_lst:
        title = song.get('title')
        artist = song.get('artist')
        up_next = "%s%s - %s, " %(up_next, title, artist)
    response = up_next[:-2] + " "
    return response
