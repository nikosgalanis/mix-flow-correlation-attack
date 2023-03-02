# Mix flow-corellation attack

## TODOs

### For proposal
 - What the attack/vulnerability is about (Arian)
 - Why you picked that paper (Nick)

#### What exactly you will implement. (Mustafa)
 - mix structure (n seenders -> mix -> n recievers)
 - data flow/corellation attack attack
 - extract information based on the metric given in the paper (distignuish the data flow)
 - produce graphs to show the sucess of the attack


### For implementation
  - figure out wavelet (M)
  - make to 1 file, create pipeline (N)
  - decide wtf is going on with selections (Mail to steven)
  - create metrics + graphs (N+M)
 

### For documentation
EVERYTHING MAX 400 WORDS

#### What Vuln the attack exploits
 - high-level of the mix networks + idea behoind flow corellation (M)
 - Implementation choices (type of mix) - Arian, Mustafa
 - step by step attack proccess + metrics (M)

#### Threat + adversarial models
 - Data selection choices (n_nodes, n_packets, prob_of_same_node, time_window) (N)
 - Attack choises (wavelet stuff, ...) (M)
 - explain why we oversimplify it and why that doesn't change anything (M)
 - IMPORTANT: EXPLAIN WHY DO NOT CHEAT (input + output never coreated) (N)

#### Importance of the attack
 - results + graphs (+ comments) (M)

#### Defending
 - defence ideas (++ cite other papers that implement) (N)

### For the VM
 - pdf on how the vm works (instructions)
 - setup
 - create a script to run automatically (parameters)

## Rules for the repo
 - No writing on the same file
 - We all commit to main branch, no need for pull requests
 - Commits with helpful messages (will hlep us with bugs later)
 - **No git push -f**

Steps for commiting:

```
git add .
git commit -m "bla bla"
git pull
git push
```