import re
import random
from util import hook

responses = (
    ("sanic", ("GOTTA GO FAST", "GOTTA GO FAST")),
    ("gotta go fast", ("SANIC", "SANIC")),
    ("vtec", ("JUST KICKED IN", "VTEC JUST KICKED IN")),
    ("wop", ("wop", "wop")),
)

pronouns = {
    "i'm": "you're",
    "i": "you",
    "me": "you",
    "yours": "mine",
    "you": "I",
    "am": "are",
    "my": "your",
    "you're": "I'm",
    "was": "were"
}


@hook.singlethread
@hook.event('PRIVMSG')
def ai_sieve(paraml, input=None, notice=None, db=None, bot=None, nick=None,
             conn=None, server=None):
    server = server.split('.')[1]
    full_reply = ''

    # replace = {
    #     'nick':input.nick
    # }
    # process all aif

    # process pastabot ai

    for pattern in responses:
        wildcards = []
        s = bot.config['connections'][server.title()]['user'].lower()
        match = pattern[0].replace('{name}', s)
        if re.match(match, input.msg.lower()):
            # print "Matched: {}".format(pattern[0])
            wildcards = filter(bool, re.split(pattern[0], input.msg.lower()))
            # replace pronouns
            wildcards = [' '.join(pronouns.get(word, word) for word in
                         wildcard.split()) for wildcard in wildcards]
            response = random.choice(pattern[1])

            s = bot.config['connections'][server.title()]['user'].lower()
            response = response.replace('{nick}',
                                        input.nick).replace('{name}', s)
            response = response.format(*wildcards)
            full_reply += response + ' '
            return full_reply
