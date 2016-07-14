# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import telnetlib


class Camera(object):

    def __init__(self, **kwargs):
        self._user = kwargs.get('user', 'admin')
        self._password = kwargs.get('password', 'password')
        self._host = kwargs.get('host')
        self._port = kwargs.get('port', '23')
        self._last_cmds = set()
        self._stop_cmd = 'stop'
        self._zoom_cmd = 'zoom'
        self._pan_cmd = 'pan'
        self._tilt_cmd = 'tilt'
        self._cc = self._get_camera()

    def _get_camera(self):
        c = telnetlib.Telnet(self._host, self._port)
        self._camera_login(c)
        return c

    def _make_cmd(self, cmd, *args):
        cmd_str = 'camera %s' % cmd
        for arg in args:
            if arg:
                cmd_str += ' %s' % arg
        cmd_str += '\n\r'
        return {'cmd': cmd, 'cmd_str': cmd_str}

    def _send_cmd(self, cmd, skip_add_to_last=None):
        self._cc.write(cmd['cmd_str'])
        if skip_add_to_last is None:
            self._last_cmds.add(cmd['cmd'])

    def _camera_login(self, c):
        c.read_until('login:', 3)
        c.write(self._user + '\n\r')
        c.read_until('Password:', 10)
        c.write(self._password + '\n\r')

    def _ping(self, c):
        try:
            c.write('ping')
            c.read_until('Syntax error', 1)
            return True
        except:
            return None

    def home(self):
        cmd = self._make_cmd('home')
        self._send_cmd(cmd, skip_add_to_last=True)

    def set_preset(self, preset):
        if preset in xrange(1, 7):
            raise Exception('Invalid Preset Number, please use 7 thru 12')
        cmd = self._make_cmd('preset', 'store', preset)
        self._send_cmd(cmd, skip_add_to_last=True)

    def goto_preset(self, preset):
        cmd = self._make_cmd('preset', 'recall', preset)
        self._send_cmd(cmd, skip_add_to_last=True)

    def tilt(self, direction, speed=5):
        direction = str(direction).lower()
        if direction not in ('up', 'down'):
            raise Exception('Invalid Direction, Use up or down')
        cmd = self._make_cmd(self._tilt_cmd, direction, speed)
        self._send_cmd(cmd)

    def pan(self, direction, speed=5):
        direction = str(direction).lower()

        if direction not in ('left', 'right'):
            raise Exception('Invalid Direction, Use left or right')

        cmd = self._make_cmd(self._pan_cmd, direction, speed)
        self._send_cmd(cmd)

    def zoom(self, direction, speed=2):
        direction = str(direction).lower()

        if direction not in ('in', 'out'):
            raise Exception('Invalid Direction, Usse in or out')

        cmd = self._make_cmd(self._zoom_cmd, direction, speed)
        self._send_cmd(cmd)

    def stop(self):
        to_remove = []
        for c in self._last_cmds:
            cmd = self._make_cmd(c, self._stop_cmd)
            self._send_cmd(cmd, skip_add_to_last=True)
            to_remove.append(c)
        for c in to_remove:
            self._last_cmds.remove(c)
