import subprocess
import threading

import ptyprocess


class PtyProcessUnicode(ptyprocess.PtyProcessUnicode):
    def _reader_thread(self, buffer):
        """

        :param buffer: list
        :return:
        """
        # buffer.extend(self.readline())
        buffer.extend(self.read())

    def restrict_read(self, timeout=None):
        timeout = timeout or 1
        stdout_buff = list()

        stdout_thread = threading.Thread(target=self._reader_thread, args=(stdout_buff,))
        stdout_thread.daemon = True
        stdout_thread.start()
        stdout_thread.join(timeout=timeout)

        is_alive = stdout_thread.is_alive()
        if is_alive:
            raise Exception("readline timeout: %s seconds" % timeout)

        return "".join(stdout_buff)


class Popen(subprocess.Popen):
    @property
    def alive(self):
        if self.poll() is None:
            return True
        else:
            return False

    def _line_reader_thread(self, buffer):
        """

        :param buffer: bytearray
        :return:
        """
        buffer.extend(self.stdout.readline())

    def stdout_restrict_readline(self, timeout=None):
        timeout = timeout or 1
        stdout_buff = bytearray()

        stdout_thread = threading.Thread(target=self._line_reader_thread, args=(stdout_buff,))
        stdout_thread.daemon = True
        stdout_thread.start()
        stdout_thread.join(timeout=timeout)

        is_alive = stdout_thread.is_alive()
        if is_alive:
            raise Exception("readline timeout: %s seconds" % timeout)

        return stdout_buff
