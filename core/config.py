import json
import sys
import os

# NOTE(evanscottgray) where the heck is 'bot' coming from..?
#                     that's why the noqa is present..


def save(conf):
    json.dump(conf, open('config', 'w'), sort_keys=True, indent=2)

if not os.path.exists('config'):
    print "Please rename 'config.default' to 'config' to set up your bot!"
    print "For help, see https://github.com/Anonymike/pasta-bot"
    print "Thank you for using PastaBot!"
    sys.exit()


def config():
    # reload config from file if file has changed
    config_mtime = os.stat('config').st_mtime
    if bot._config_mtime != config_mtime:  # noqa
        try:
            bot.config = json.load(open('config'))  # noqa
            bot._config_mtime = config_mtime  # noqa
        except ValueError, e:
            print 'error: malformed config', e


bot._config_mtime = 0  # noqa
