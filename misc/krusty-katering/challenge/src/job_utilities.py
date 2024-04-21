from typing import Dict
from random import choices
from foods import foods, probabilities


def generate_jobs(num_jobs: int):
    # num_foods = len(foods)
    #
    # num_per_food = num_jobs // num_foods
    # num_residual = num_jobs % num_foods
    #
    # jobs = foods * num_per_food
    # jobs += [foods[-1]] * num_residual
    # shuffle(jobs)

    return choices(foods, probabilities, k=num_jobs)


def time_to_string(time: int) -> str:
    """Converts time to string"""
    if time >= 3600:
        return f'{time // 3600}h{(time % 3600) // 60}m{time % 60}s'
    if time < 60:
        return f'{time}s'
    if not time % 60:
        return f'{time // 60}m'
    return f'{time // 60}m{time % 60}s'


def job_to_string(job: Dict[str, int | str], i=None) -> str:
    return (f"{'' if i is None else f'Order #{i+1}: '}{job['name']}\n"
            f"├── Price: {job['price']}\n"
            f"└── Estimated time to cook: {time_to_string(job['time'])}\n")


if __name__ == '__main__':
    assert (t := time_to_string(3661)) == '1h1m1s', t
    assert time_to_string(32) == '32s'
    assert time_to_string(132) == '2m12s'
