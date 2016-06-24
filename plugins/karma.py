import re
from util import hook, user

db_ready = False

KARMA_RE = (r"([-\w]+)(\s*)([+][+]|[-][-])", re.I)


def db_init(db):
    "check to see that our db has the the karma table and return a connection."
    db.execute("create table if not exists karma(name, chan, points INTEGER, "
               "host, primary key(name, chan))")
    db.commit()
    db_ready = True


def check_if_user(karma_nick, db, chan):
    last_message = db.execute("select name from seen where name like ? "
                              "and chan =  ?",
                              (str(karma_nick), chan, )).fetchone()
    if not last_message:
        return False
    return True


def adjust_points(karma_nick, sentiment, db, chan, input):
    user_in_karma = db.execute("select name from karma where "
                               "name like ? and chan = ?",
                               (karma_nick, chan, )).fetchone()
    if not user_in_karma:
        db.execute("insert into karma(name, chan, points, host)"
                   " values(?,?,?,?)", (karma_nick, chan, 0, input.mask))
        db.commit()
    if sentiment == "++":
        point_change = 1
    else:
        point_change = -1

    db.execute("update karma set points = points + ? where "
               "name like ? and chan = ?", (point_change, karma_nick, chan, ))
    db.commit()


def get_user_karma(karma_nick, db, chan):
    u_k = db.execute("select name, points from karma where "
                     "name like ? and chan = ?",
                     (karma_nick, chan, )).fetchone()
    if not u_k:
        return False
    return u_k


def get_all_karma(db, chan):
    karma_dump = db.execute("select name, points from karma where "
                            "chan = ? ORDER BY points desc",
                            (chan, )).fetchall()
    return list(karma_dump)


def format_all_karma(all_karma, nick):
    top3 = all_karma[:3]
    bottom3 = all_karma[-3:]

    response = "Highest Karma:"
    for i in top3:
        response = ("%s %s (%d), " % (response, i[0], i[1]))

    response = ("%s. Lowest Karma:" % response[:-2])
    for i in bottom3:
        response = ("%s %s (%d), " % (response, i[0], i[1]))
    response = response[:-2] + ". "

    for i, elem in enumerate(all_karma):
        if nick == elem[0]:
            response = "%s You (%s) are ranked %d out of %d." % (response,
                                                                 nick, i+1,
                                                                 len(all_karma)
                                                                 )
            return response

    response = "%s I couldn't find your Karma. Sorry :(" % response
    return response


@hook.regex(*KARMA_RE)
def karma_mod(match, nick=None, chan=None, db=None, input=None):
    if not db_ready:
        db_init(db)
    karma_nick = str(match.group(1))
    sentiment = str(match.group(3))

    if karma_nick.lower() == nick.lower():
        return "C'mon bro"

    if check_if_user(karma_nick, db, chan):
        adjust_points(karma_nick, sentiment, db, chan, input)
    else:
        return "I haven't seen %s before." % karma_nick


@hook.command
def karma(inp, nick='', db=None, chan=None, input=None):
    if inp.lower() == 'me' or inp.lower() == nick.lower():
        user_karma = get_user_karma(nick, db, chan)
        if not user_karma:
            return "I haven't seen you before. Do something nice, "
            "get some Karma."
        return "You have %d Karma" % user_karma[1]
    elif not inp:
        all_karma = get_all_karma(db, chan)
        all_karma_response = format_all_karma(all_karma, nick)
        return all_karma_response
    else:
        user_karma = get_user_karma(inp, db, chan)
        if not user_karma:
            return "I haven't seen %s before." % inp
        return "%s has %d Karma" % (user_karma[0], user_karma[1])
