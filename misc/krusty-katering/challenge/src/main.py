"""This file generates the orders for the user to assign, and simulates the Chum Bucket"""
# Standard library
import sys
from numpy import argmin
from numpy.random import randint
from typing import List
# Local
from job_utilities import generate_jobs, job_to_string, time_to_string


def random(job_times: List[int], num_cooks: int):
    """Assigns jobs to random cooks"""
    queue_times = [0] * num_cooks

    for job_time in job_times:
        cook_number = randint(0, num_cooks)
        queue_times[cook_number] += job_time

    return queue_times


def cyclic(job_times: List[int], num_cooks: int):
    """Assigns job n to cook n % num_cooks"""
    queue_times = [0] * num_cooks

    for i, job_time in enumerate(job_times):
        queue_times[i % 10] += job_time

    return queue_times


def shortest_schedule(job_times: List[int], num_cooks: int):
    """Greedily assigns jobs to cook with the shortest schedule"""
    queue_times = [0] * num_cooks

    for job_time in job_times:
        cook_number = argmin(queue_times)
        queue_times[cook_number] += job_time

    return queue_times


path = './jobs/'
num_days = 5

description = '''
Krusty Katering is hemorrhaging money, and Mr. Krabs has brought you in to fix it.
You have 10 line cooks, and while they're okay at making Krabby patties, they can't agree on who cooks what and when.
To make matters worse, Squidward (trying to keep his job) refuses to give you the list of orders, and will only tell you them one by one.
Each time Squidward tells you a job, you get to add it to a cook's schedule for the day.
Cooks cannot trade jobs, once it's on the schedule, it stays there.
You want to ensure the last order finishes as soon as possible so that Mr. Krabs can close and count his profits.

The competing Plankton's Provisions assigns their jobs randomly.
So long as your crew is 10% more efficient than Team Chum Bucket every day this week, you're hired.
Can you save Mr. Krabs' business?
'''

print(f"{description}\n{'-' * 40}\n")

for n in range(num_days):
    orders = generate_jobs(1000)
    order_times = [order['time'] for order in orders]

    time_to_beat = max(random(order_times, 10))
    print(f'Day {n + 1}. Time to beat: {time_to_string(time_to_beat)}\n')

    times = [0] * 10

    for i, order in enumerate(orders):
        print(f'{job_to_string(order, i=i)}\n')

        try:
            cook_number = int(input('Which cook should handle this job? [1-10]\n').strip())
            print('')
            assert 1 <= cook_number <= 10
        except KeyboardInterrupt:
            sys.exit(0)
        except ValueError:
            print('Value could not be interpreted as an integer')
            sys.exit(0)
        except AssertionError:
            print('Value was successfully interpreted as an integer, but not an integer 1-10')
            sys.exit(0)

        times[cook_number - 1] += order['time']

    time = max(times)
    print(f'Your time: {time_to_string(time)}')
    result = round((time_to_beat / time - 1) * 100, 2)
    print(f'You did {result}% better than Team Chum Bucket.')

    if time_to_beat < 1.1 * time:
        print("You're fired.")
        sys.exit(0)
    else:
        print("Good work, come back tomorrow.\n")

print("You're hired, one could say that you're no UMASS{subst@nd@rd_c00k}")
