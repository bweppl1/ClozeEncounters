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


test_case = [True, True, False, False, True, False, True, True, True, False]

print(calculate_retrievability(test_case))


def calculate_stability(initial_date, end):
    pass


# define fake start list outside of function
rec_res = deque([True, False, True, False, False])


def run_algo():
    hit_result = input("(r)ight or (w)rong: ")
    if len(rec_res) > 10:
        rec_res.popleft()
    if hit_result == "r":
        rec_res.append(True)
    else:
        rec_res.append(False)

    print(f"X recent hit results = {rec_res}")

    # calculate r
    r = calculate_retrievability(list(rec_res))

    print(f"Retrievability: {r}")
    return [r, fake_date]


testing = True
slog = []
r_threshold = 0.75
fake_date = 0
s = 1

while testing:
    fake_date += 1
    continue_request = input("Type 'exit' to quit: ")
    if continue_request != "exit":
        new_test_input = run_algo()
        # check if r > r_threshold
        if new_test_input[0] > r_threshold:
            slog = []
        slog.append(new_test_input)
        print(f"s log: {slog}")
    else:
        testing = False

    # test for r threshold
    # if retrievability becomes to low, recalculate s (new interval time)
    if slog[-1][0] <= r_threshold:
        print(f"{slog[-1][0]} below threshold: {r_threshold}")
        s = slog[-1][1] - slog[0][1]

        print(f"new s = {s}. Interval set for {s - 1} days")
    else:
        s *= 1.5
        print(f"latest r: {slog[-1][0]} remains above {r_threshold}")
    print(f"Current interval is {s - 1} days.")
