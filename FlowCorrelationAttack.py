from stats import *


while True:
    res = input("Do you want to launch a single instance of the attack, extract manual stats, or extract the default stats?\nPres I for instance, M for manual and A for automatic stats\n").upper()
    if res == 'M' or res == 'I' or res == "A":
        break

if res == 'I':

    print("A single instance of the attack will be executed, outputing the detection rate\n")
    
    n_mess = int(input("Give the number of messages sent through the network\n"))
    assert(n_mess > 100)

    random_time = 2 * n_mess

    dist = input("Give the distance function to be used: F for Fourier-based or M for mutual info\n").lower()
    assert (dist == 'f' or dist == 'm')
    if dist == 'f':
        dist_func = "mutual_info"
    else:
        dist_func = "fourier"

    n_nodes = int(input("Give the number of input and output nodes\n"))
    assert(n_nodes > 1)

    fixed_prob = float(input("Give the fixed probability, as a float. Ex 0.3 -> 30%\n"))
    assert(fixed_prob > 0 and fixed_prob < 1)

    f = 5
    p = 0.5
    time_window = 5
    threshold = 10

    mix = int(input("Select the mix implementation to use. Enter the corresponding number:\n[1]: Timed\n[2]: Threshold\n[3]: Threshold or Timed\n[4]: Threshold and Timed\n[5]: Threshold Pool\n[6]: Time Dynamic Pool\n[7]: Timed Pool\n"))

    if mix == 1:
        Timed.mix(n_mess, n_nodes, random_time, time_window,fixed_prob)
        res = attack.attack(dist_func, time_window)
    elif mix == 2:
        Threshold.mix(n_mess, n_nodes, random_time, threshold, fixed_prob)
        res = attack.attack(dist_func, time_window)
    elif mix == 3:
        ThresholdOrTimed.mix(n_mess, n_nodes, random_time, time_window, fixed_prob, threshold)
        res = attack.attack(dist_func, time_window)
    elif mix == 4:
        ThresholdandTimed.mix(n_mess, n_nodes, random_time, threshold, fixed_prob, time_window)
        res = attack.attack(dist_func, time_window) 
    elif mix == 5:
        ThresholdPool.mix(n_mess, n_nodes, random_time, threshold, fixed_prob, f)
        res = attack.attack(dist_func, time_window)
    elif mix == 6:
        TimedDynamicPool.mix(n_mess, n_nodes, random_time, threshold, fixed_prob, f, time_window, p)
        res = attack.attack(dist_func, time_window)
    elif mix == 7:
        TimedPool.mix(n_mess, n_nodes, random_time, threshold, fixed_prob, f, time_window)
        res = attack.attack(dist_func, time_window)
    else:
        print("Wrong selection, exiting...\n")
        exit(1)


    print("\nThe detection rate for the specific attack durface is\n\n")
    print(res)


elif res == 'M':
    min_mess = int(input("Give the min number of messages for the graph\n"))
    max_mess = int(input("Give the max number of messages for the graph\n"))
    assert(min_mess > 99 and max_mess < 10000000)

    dist = input("Give the distance function to be used: F for Fourier-based or M for mutual info\n").lower()
    assert (dist == 'f' or dist == 'm')
    if dist == 'f':
        dist = "mutual_info"
    else:
        dist = "fourier"

    n_nodes = int(input("Give the number of input and output nodes\n"))
    assert(n_nodes > 1)
    assert(min_mess / n_nodes > 10)
    fixed_prob = float(input("Give the fixed probability, as a float. Ex 0.3 -> 30%\n"))
    assert(fixed_prob > 0 and fixed_prob < 1)

    f = 5
    p = 0.5
    time_window = 5
    threshold = 10

    run_stats(min_mess, max_mess, n_nodes, time_window, threshold, fixed_prob, f, p, dist)

elif res == 'A':
    dist = "fourier"
    min_mess = 600
    max_mess = 100000
    n_nodes = 20
    time_window = 5
    threshold = 10
    fixed_prob = 0.1
    f = 5
    p = 0.5

    run_stats(min_mess, max_mess, n_nodes, time_window, threshold, fixed_prob, f, p, dist)
