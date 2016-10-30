#!/usr/bin/python3

import requests
import sys

num_lines = sum(1 for line in open('worktodo.txt'))
if num_lines > 1000:
	sys.exit(0)

payload = {
    'cores': 12,
    'num_to_get': 50,
    'pref': 2,
    'exp_lo': '',
    'exp_hi': '',
}

result = requests.get('http://www.mersenne.org/manual_assignment/', params=payload)

start = '<!--BEGIN_ASSIGNMENTS_BLOCK-->'
end = '<!--END_ASSIGNMENTS_BLOCK-->'
work_string = (result.text.split(start))[1].split(end)[0]

work = work_string.split('\n')

with open('worktodo.txt', 'a') as todo_file:
    todo_file.write('\n'.join(work))
