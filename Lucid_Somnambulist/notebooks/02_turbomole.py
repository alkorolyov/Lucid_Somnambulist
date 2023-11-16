
import subprocess
import sys
import os
from time import time

from subprocess import Popen, PIPE, CalledProcessError

def execute(cmd):
    with Popen(cmd, stdout=PIPE, bufsize=1, universal_newlines=True) as p:
        for line in p.stdout:
            print(line, end='') # process line here
            pass

    if p.returncode != 0:
        raise CalledProcessError(p.returncode, p.args)

# def execute(command):
#     subprocess.check_call(command, shell=True, stdout=sys.stdout, stderr=subprocess.STDOUT)


if __name__ == '__main__':
    start = time()
    execute(['./run.sh', 'crest_best.xyz'])
    print(f'Total time spent: {time() - start:.1f}s')

