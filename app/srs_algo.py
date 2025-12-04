# (r) Retrievability - how likely an item can be recalled at current time -> measured in %
# (s) Stability - how long before recall degrades significantly -> measured in days
# r = boolean of last X attempts =
# S = date of max(r) - date of min(r)
# interval = S - 1
from datetime import datetime
from typing import List
from collections import deque


def calculate_retrievability(r: List[bool]) -> float:
    rlength = len(r)
    correct_count = 0
    for attempt in r:
        if attempt:
            correct_count += 1
    retrievability = correct_count / rlength
    return round(retrievability, 2)


def calculate_stability(initial_date, end):
    pass


def simple_srs_algo(results):
    if results[-1] == False:
        next_hit = 1
    else:
        r = calculate_retrievability(results)
        if r < 0.5:
            next_hit = 1
        elif r > 0.49 and r < 0.80:
            next_hit = 3
        else:
            next_hit = 7
    print(next_hit)


# define fake start list outside of function
rec_res = deque([])


def run_algo():
    testing = True
    quit_check = input(f"quit? y/n: ")
    if quit_check == "y":
        testing = False
    while testing:
        hit_result = input("(r)ight or (w)rong: ")
        if len(rec_res) > 3:
            rec_res.popleft()
        if hit_result == "r":
            rec_res.append(True)
        else:
            rec_res.append(False)

        print(f"X recent hit results = {rec_res}")
        simple_srs_algo(rec_res)


run_algo()
