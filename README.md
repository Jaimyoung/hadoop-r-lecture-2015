# Hadoop Basics and Click Predicition on Hadoop/R Platform
This is the repository for 
Hadoop-R Lecture at 
SNU (Seoul National University)
SRI (Statistical Research Institute),
scheduled for Feb 27, 2015.
The lecture covers the following materials, among others:

1. Hadoop Basics
1. MapReduce Basics
1. Hadoop Streaming
1. Word-count Exercise
1. Click prediction Exercise

This repository hosts documents (excluding lecture slides)
and scripts (Python, R, shell, ...) for the hands-on session
of the lecture.


## Prerequisites
Prerequisites include:

1. Unix/Linux/OS-X system is assumed to run Unix-flavored commands.
    Windows system should be OK, with such extra softwares as
    [Cygwin](https://www.cygwin.com/) or
    [http://win-bash.sourceforge.net/](http://win-bash.sourceforge.net/). 
1. Git installation (of course).
    1. `git clone https://github.com/Jaimyoung/hadoop-r-lecture-2015.git`
1. Python installation.
    1. [Anaconda](http://continuum.io/downloads)
    seems a good Python distribution that's painless to use.
1. (Optional) Local Hadoop installation to run on local single-node setup
    1. On OS-X, it's as simple as `brew install hadoop` 
    (after installing `brew` of course).
1. (Optional) AWS EMR (Amazon Web Service Elastic MapReduce)
    account to run Hadoop on EMR.
    1. AWS account will be given to the lecture attendees during
    the lecture period.


### Prepare the data
Once this repository is cloned, `cd hadoop-r-lecture-2015` and
download a few data locally.
First, a couple of classic documents from the
[Project Gutenberg](http://www.gutenberg.org/).


    wget http://www.gutenberg.org/cache/epub/4300/pg4300.txt -O data/pg4300.txt
    wget http://www.gutenberg.org/cache/epub/10/pg10.txt -O data/pg10.txt

Then download a small click prediction data. 
(Larger data would be accessible on AWS S3)

    wget $somewhere \
        -O data/click-prediction-small.csv.gz



## Wordcount Exercise
### Local
`src/wc_mapper.py` and `src/wc_reducer.py` are 
minimalistic Python codes for Hadoop Word Count Exercise.
You can test it locally via:

    echo "foo bar foo" | src/wc_mapper.py
    echo "foo bar foo" | src/wc_mapper.py | src/wc_reducer.py

Run it on input files like:

    cat data/pg10.txt | src/wc_mapper.py | src/wc_reducer.py > data/kjv-wc.txt
    cat data/pg4300.txt | src/wc_mapper.py | src/wc_reducer.py > data/ulyss-wc.txt


### (Side Topic) Power of Unix Commands for Data Science Tasks
Unix commands are useful for lots of data science tasks.
Let's illustrate it by a few examples.

This shows the total number of rows (# of different words) in each file:

    $ wc -l data/*-wc.txt
        34057 data/kjv-wc.txt
        50106 data/ulyss-wc.txt
        84163 total

To browse the most frequent words in each text, run:

    sort -nr -k2 data/kjv-wc.txt | more
    sort -nr -k2 data/ulyss-wc.txt | more

We can filter for words that are likely to be a person's name 
by using ["regular expression" in Unix `grep`](http://www.robelle.com/smugbook/regexpr.html).

    grep '^[A-Z]' data/kjv-wc.txt | more

Again, we can sort them by the frequency:

    grep '^[A-Z]' data/kjv-wc.txt | sort -nr -k2 | more

It shows lots of false positives, but we get some ideas on most mentioned
names in the source text. (Google `most frequent names in bible` for
more accurate statistics)


### Exercises
TBD


### Remote
To run the word count example on hadoop, we have a few options:

1. **Native Java Codes** : Maximum flexibility (and performance).
    This could be challenging for non-CS people, though.
1. **High-level Environments**  such as Apache Pig: This could be easier
    to use, but less flexible. Jobs tend to be less optimized than
    Java or Streaming options.
1. **Hadoop Streaming** via Python: Good balance between 
    ease of use and flexibility. 
    Also, Python is a must-to-have skill for data scientists anyway.

We opt for Streaming in this lecture.
We will use above codes for streaming as well.
For running Streaming jobs, we have a few options:

1. **Web Interface**: Run the job using AWS web interface.
1. **AWS CLI**: Run the job using AWS CLI from the command line.
1. **SSH** (Advanced): Run the job from the CLI from SSH session. 


We will run our codes on web interface first, and then show AWS CLI commands.

First, we need to upload the scripts we have above to an S3 location.
This is done already on this S3 bucket/folder. You can check it via:
    
    aws s3 ls s3://snu-sri-2015/src/ --profile snu-user

Now go into the the 
[AWS EMR console](https://us-west-2.console.aws.amazon.com/elasticmapreduce/home?region=us-west-2#cluster-list:)
to create a cluster. 
See the lecture slides for details.

Run the job by adding a Streaming step with the following information.

1. mapper: `s3://snu-sri-2015/src/wc_mapper.py`
1. reducer: `s3://snu-sri-2015/src/wc_reducer.py`
1. input:   `s3://snu-sri-2015/data/gutenberg/pg10.txt`
1. output: `s3://snu-sri-2015/tmp/user01/kjv-wc`

Or, if you're advanterous, you could try:

    aws emr add-steps --profile snu-user \
        --cluster-id j-23N35K5IPTZQN  \
        --steps file://./wc-job.json

with the `wc-job.json` file.
You may have to delete the s3 output location first, before you run this, via:

    aws s3 rm s3://snu-sri-2015/tmp/user01/kjv-wc

## Click Prediction Using Hadoop + R
TBD

### Local testing

### Remote run

### Download the data

### R analysis


### Hadoop scoring using the coefficients



## References:

1. [Hadoop Streaming from Documentation](http://hadoop.apache.org/docs/r1.2.1/streaming.html)
1. [Michael G. Noll's Note](http://www.michael-noll.com/tutorials/writing-an-hadoop-mapreduce-program-in-python/)
