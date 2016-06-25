import requests
import subprocess
import tempfile
import re
import hashtags
import datafiles
from mimetypes import guess_extension, guess_type
from util import hook, formatting


@hook.command("pomftube", adminonly=True)
@hook.command(adminonly=True)
def pomf(url):
    "pomf <url> -- Downloads file and uploads it"
    return formatting.output('pomf', [upload(url)])


@hook.command("pr", adminonly=True)
@hook.command("premember", adminonly=True)
@hook.command(adminonly=True)
def pomfremember(inp, chan=None, nick=None, say=None, db=None, adminonly=True):
        """
        pomfremember <word> <url>
        Downloads file, uploads it and adds it to the dictionary
        """
        word, url = inp.split(None, 1)
        pomfurl = upload(url)
        strsave = "{} {}".format(word, pomfurl)
        hashtags.remember(strsave, nick, db)
        output = formatting.output('pomf',
                                   ['{} remembered as {}'.format(word,
                                                                 pomfurl)])
        return(output)


@hook.command("padd", adminonly=True)
@hook.command(adminonly=True)
def pomfadd(inp, chan=None, nick=None, notice=None, db=None, say=None):
    """
    pomfadd <word> <url>
    Downloads file, uploads it and adds it to the dictionary
    """
    dfile, url = inp.split(None, 1)
    pomfurl = upload(url)
    strsave = "{} {}".format(dfile, pomfurl)
    datafiles.add(strsave, notice)
    return(formatting.output('pomf', ['{} remembered as {}'.format(pomfurl,
                                                                   dfile)]))


def upload(url):
    cclive = subprocess.Popen("cclive --support | xargs | tr ' ' '|'",
                              stdout=subprocess.PIPE, shell=True)
    (cclive_formats, err) = cclive.communicate()
    re_youtube = "youtube|youtu\.be|yooouuutuuube"
    search = ".*(?:{}|{}).*".format(re_youtube, cclive_formats)
    try:
        if re.match(search, url, re.I):
            if re.match(".*(?:{}).*".format(re_youtube), url, re.I):
                cmd = "youtube-dl --quiet --recode-video webm " \
                      "--format webm/mp4 --output " \
                      "/tmp/%\(id\)s.webm {}".format(url)
                p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
                yt = ".*(?:youtube.*?(?:v=|/v/)|youtu\.be/|yooouu" \
                     "utuuube.*?id=)([-_a-zA-Z0-9]+).*"
                file = "/tmp/{}.webm".format(re.match(yt, url, re.I).group(1))
            else:
                cmd = "cclive --quiet -f fmt43_360p {} --O " \
                      "/tmp/pomf.webm --exec 'echo -n %f'".format(url, "/tmp")
                p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
                (file, err) = p.communicate()
        else:
            extension = guess_extension(guess_type(url)[0]).replace('jpe',
                                                                    'jpg')
            temp = tempfile.NamedTemporaryFile(suffix=extension)
            content = requests.get(url).content
            temp.write(content)
            file = temp.name
            fh = open(file, "rb")
            fh.seek(0)
            content = requests.post(url="http://pomf.se/upload.php",
                                    files={"files[]": fh})
            if not content.status_code // 100 == 2:
                raise Exception("Unexpected response {}".format(content))
            r = content.json()["files"][0]["url"]
            return "http://a.pomf.se/{}".format(r)
    except Exception as e:
        return "Error: {}".format(e)
