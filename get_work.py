#!/usr/bin/python3

import argparse
import requests
import sys
import os

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--force", help="Get new work even if you already have more than the configured minimum amount", action="store_true")
parser.add_argument("-c", "--cores", type=int, help="Number of workers to collect work for")
parser.add_argument("-w", "--workunits", type=int, help="Number of workunits to collect work for each core/ worker")
parser.add_argument("-t", "--type", type=int, help="work type identifier id. ")
parser.add_argument("-m", "--minimum", type=int, help="minimum number of workunits in target file")
parser.add_argument("-v", "--verbose", action="store_true", help="verbose")
parser.add_argument("-o", "--output", type=str, help="specify an output file")
args = parser.parse_args()

def log(line):
    if args.verbose:
        print(line)

output = args.output or 'worktodo.txt'
minimum = args.minimum or 10
cores = args.cores or 2
num_to_get = args.workunits or 5
worktype = args.type or 2

log("using worktodo file: %s" % output)
log("minimum workunit count: %d" % minimum)
log("cores: %d" % cores)
log("num_to_get: %d" % num_to_get)
log("worktype: %d" % worktype)

if not os.path.isfile(output):
    open(output, 'w').close()

num_lines = sum(1 for line in open(output))
if num_lines > minimum and not args.force:
    log("already have enough work, exiting happy")
    sys.exit(0)

payload = {
    'cores': cores,
    'num_to_get': num_to_get,
    'pref': worktype,
    'exp_lo': '',
    'exp_hi': '',
}

log("payload: \n%s" % payload)
result = requests.get('http://www.mersenne.org/manual_assignment/', params=payload)
log("url: %s" % result.url)

log("parsing response")
start = '<!--BEGIN_ASSIGNMENTS_BLOCK-->'
end = '<!--END_ASSIGNMENTS_BLOCK-->'
work_string = (result.text.split(start))[1].split(end)[0]

work = work_string.split('\n')
with open(output, 'a') as todo_file:
    log(work)
    todo_file.write('\n'.join(work))
