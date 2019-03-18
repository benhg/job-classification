# Job Classification

## What's the bigger picture?

In a 'zoomed-out' picture, the problem we are dealing with is high performance job scheduling. Currently, HPC jobs are almost always scheduled with a combination of two deciding factors: Whose job was in the queue first, and whose job has a higher priority. This model has worked for quite a long time.

However, it's not really good enough. Scheduling jobs like this can cause all kinds of problems, and end up lowering efficiency of large, shared HPC systems.

We view the next step as something we like to call "Job Awareness." What we mean by that is "can I guess how your job is going to behave?" One example of this is if we have two jobs, one of which is "bound" by memory, and the other of which is "bound" by CPU, those jobs may run well together. Also, if two jobs are both "bound" by CPU, it's probably best to keep them as far from each other as possible. 

This repo hosts code to solve the first part of the problem at hand: Classifying jobs into what resource "binds," or "constrains" them.

## How are we doing it?

Right now, we parse the Abstract Syntax Trees of the labelled HPC jobs and manually extract features (things like how many for loops, variable assignments, function calls, etc.) and pass them to various types of models (SVMs, RNNs, simple fully connected NNs). 

We are currently working on designing a protocol so that we can feed in a normalized version of the AST itself rather than features derived from the AST. We would like to follow the example of people in the field of Natural Language Processing (who do a great job of feeding in just the data and not adding human bias to it).

## What exactly is a "Job"?

Right now, we are focusing entirely on python-based scripts. This is a nice starting point because of all of the resources surrounding Python and specifically, parsing of Python Abstract Syntax Trees (ASTs). Python scripts are also very nice for this project because of its context. Python is an incredibly commonly used language in the research computing space, and even when the programs are written in other languages, HPC jobs are often "orchestrated" by python scripts. This means that if there's one language to start with, it's probably Python.

Additionally, there is one considerable restriction on what separates just any old code from a "job". A "job" must have a start and an end. For example, a python-defined web server with an infinite loop waiting for users to contact it would not count as a "job," but a script which runs several other scripts before exiting would.

## What are some next steps?

After we get the classification working, the next steps are pretty clear. We would like to:
    - Develop add-ons to schedulers (SLURM, etc) that allow us to use our classifications with existing HPC software
    - Make our model learn from its mistakes (have it profile jobs it classifies and check itself)
    - Experiment with things like predicting WHEN jobs are going to be scheduled rather than just how they'll behave (scheduling is trivial if you know the future :) )
    - Expand to more languages (with less easily accessible ASTs)

## Who are we?

The primary developer of this project is [Ben Glick](mailto:glick@lclark.edu). He's an undergraduate student at Lewis & Clark College in Portland Oregon. This project is supported by his advisor, Jens Mache. Please feel free to contact Ben <glick@lclark.edu> if you have any questions, comments or suggestions.