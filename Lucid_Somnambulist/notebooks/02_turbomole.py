#
# from subprocess import Popen, PIPE, CalledProcessError
#
# def execute(cmd):
#     with Popen(cmd, stdout=PIPE, bufsize=1, universal_newlines=True) as p:
#         for line in p.stdout:
#             print(line, end='') # process line here
#
#     if p.returncode != 0:
#         raise CalledProcessError(p.returncode, p.args)

import subprocess
import sys


def execute(command):
    subprocess.check_call(command, shell=True, stdout=sys.stdout, stderr=subprocess.STDOUT)

if __name__ == '__main__':
    # execute(['source','setup.sh'])
    execute('./run.sh')