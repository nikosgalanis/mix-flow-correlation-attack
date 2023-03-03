"""
Create stats and graphs for the Flow-Corellation Attack
"""
import Timed
import Threshold
import attack
res = input("Select type of mix: A for Timed | B for Threshold\n").upper()

# Timed mix
if res == 'A':
    n_nodes = 6
    n_messages = 100
    time_window = 5
    random_time = 10

    Timed.mix(n_messages, n_nodes, random_time, time_window)
