from numpy import argmin
from pwn import remote


def parse_time(line):
    # print(line)
    if 'm' in line and 's' not in line:
        return int(line.split('m')[0]) * 60
    if 's' in line and 'm' not in line:
        return int(line.split('s')[0])
    num_min, remaining = line.split('m')
    return int(num_min) * 60 + int(remaining.split('s')[0])


def parse_first_line(line):
    line = line.split(': ')[1]
    hours_str, remaining = line.split('h')
    minutes_str, remaining = remaining.split('m')
    seconds_str = remaining.split('s')[0]

    return int(hours_str) * 3600 + int(minutes_str) * 60 + int(seconds_str)


# def parse_job(file):
#     file.readline()
#     file.readline()
#     job_time = parse_time(file.readline().split(': ')[1].strip())
#     file.readline()
#     return job_time


# p = remote('address tbd', 'port tbd')

for n in range(5):
    # Read in time to beat from first line
    first_line = 'Day 1. Time to beat: 1h27m52s'  # TODO : make into actual read
    time_to_beat = parse_first_line(first_line)

    queue_times = [0] * 10

    for _ in range(1000):
        job_time = 0  # TODO : make into actual read
        i = argmin(queue_times)
        queue_times[i] += job_time

    # TODO : Dump remaining lines until Day n + 1
