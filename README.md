# Flow Correlation Attacks against Mixing Networks

## Attack implemented
In this project, we focus and implement attacks in Mix networks presented in [1]. Mix networks are a type of anonymity networks that are intended to safeguard users’ privacy by rerouting their traffic before it reaches its final destination. During such an attack, an adversary examines the patterns of the network’s traffic in an effort to achieve a correlation between the sender and the receiver of the message. This is shown to be accomplished by the authors by monitoring the traffic on the network and then analysing the timing of the messages in order to compare them with the messages that were sent by the person who is the object of the investigation. The attack pipeline uses math-based algoithms that allow an adversary to extract useful information and thus launch a flow correlation attack.

We replicated this attack by simulating an adversaries perspective of traffic analysis of a mix network such that they do not see any contents of the packets but only the times they are being sent and received. The attack is done by analyzing these times, and determining the distance between input and output nodes, providing a 100% detection rate, given enough packets are tracked. This is highly damaging for mix networks, and thus we have outlined the defences given in the paper, as well as in other similar pieces of work.

## Running the attack

Run using:
```
python3 FlowCorrelationAttack.py
```

Possible selections:

### Launching a single instance
The first choice allows the user to launch a single instance of an attack using the application. The attack will then output the detection rate.

### Extracting manual statistics
The second choice allows the user to extract manual statistics for a given range of messages. The output will be a graph, with the number of messages in the X-axis and the detection rate as the Y-axis, for all possible mix implementations.

### Extracting default statistics
The third choice in the application is to extract the default stats automatically. This option creates the above mentioned stats with default values for its parameters. These default values are used to run the attack several times. Finally, a plot of the detection rate versus the number of messages for the given values is once again generated.

## Team members
 - [Tahamid Arian Amanat](https://github.com/Ariel70)
 - [Mike Belegris](https://github.com/MBelegris)
 - [Nick Galanis](https://github.com/nikosgalanis)
 - [Mustafa Lattouf](https://github.com/musttouf)

This implementation has been submitted as a project for the module "Computer Security II" in the MSc Information Security at UCL. UCL Copyright terms apply.
## References
[1](original_paper.pdf): Ye Zhu, Xinwen Fu, Bryan Graham, Riccardo Bettati, and Wei Zhao. "On Flow Correlation Attacks and Countermeasures in Mix Networks" (2005). 
