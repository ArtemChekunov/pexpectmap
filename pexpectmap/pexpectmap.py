import re
from datetime import datetime
from datetime import timedelta
from subprocess import PIPE

import pexpectmap.util


def popen_expect(cmd, expect_map=None, timeout=1, readline_timeout=1):
    end_time = datetime.now() + timedelta(seconds=timeout)
    expect_map = expect_map if expect_map else {}

    proc = pexpectmap.util.Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    for line in iter(lambda: proc.stdout_restrict_readline(readline_timeout), ''):
        line = bytes(line).decode().strip('\n')

        if line:
            print(line)

        for search_pattern, input_str in expect_map.items():
            if re.search(search_pattern, line):
                proc.stdin.write(str(input_str + '\n').encode())
                proc.stdin.flush()

        if not proc.alive and line == '':
            break

        if datetime.now() > end_time:
            raise TimeoutError("Time out: %s seconds" % timeout)


def pty_expect(cmd, expect_map=None, timeout=1, readline_timeout=1):
    end_time = datetime.now() + timedelta(seconds=timeout)
    expect_map = expect_map if expect_map else {}

    proc = pexpectmap.util.PtyProcessUnicode.spawn(cmd)
    for line in iter(lambda: proc.restrict_read(readline_timeout), ''):
        line = line.rstrip('\n\r')

        if line:
            print(line)
        for search_pattern, input_str in expect_map.items():
            is_match = re.search(search_pattern, line)
            # print({"search_pattern": search_pattern,
            #        "line": line,
            #        "is_match": is_match})

            if is_match:
                proc.write(str(input_str + '\r'))

        if not proc.isalive():
            break

        if datetime.now() > end_time:
            raise TimeoutError("Time out: %s seconds" % timeout)

# if __name__ == '__main__':
#     cmd = ["./read_echo.sh"]
#     main(cmd, timeout=2, readline_timeout=3,
#          expect_map={
#              '^Say something:$': 'MY WORD',
#              # '^Say something else:$': 'MY NEW WORD',
#          })
