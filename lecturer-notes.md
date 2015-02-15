# Notes for the Lecturer
What the lecturer needs to prepare for the hands-on course.


## AWS setup
Here are a few AWS-related steps:

1. Set up AWS account
    1. In the current lecture, I'm utilizing AWS account set up by
    SNU SRI.
1. Setup an admin user at [IAM console](https://console.aws.amazon.com/iam/home?#home).
    1. AWS Access Key ID and AWS Secret Access Key are created.
    1. Give the user the Administrator privilege, so you could admin.
    1. Going forward, sign in at  AWS Management Console Sign-in Page that looks 
    like, e.g. `https://648795808428.signin.aws.amazon.com/console/` where
    the numbers are your AWS account ID. 
    See this [doc](http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_AccessingConsole.html)
    for details. 
    Don't use your AWS account id to log into AWS.
1. Install [AWS CLI (command line interface)](http://aws.amazon.com/cli/).
    1. `sudo pip install awscli` would do it if you're on OSX.
1. [Configure CLI](http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html).
    1. You can keep multiple AWS credentials on a single machine
        in case you have your personal AWS account as well. Do
        `aws configure --profile snu-user` for example.
    1. Use them like:
        `aws s3 ls --profile snu-user`
    1. NOTE: dont use `AWS_ACCESS_KEY_ID` environment variable, since that will 
        get used instead of the different profiles.


## Creating student accounts via IAM
Now it's time to create a few user accounts for the class.
You can again use the IAM console, but you can create at most 5 users at a time.
Not very efficient.
CLI is your friend, since you can automate user creation.

Before we go on, we first create a group `HadoopStudents` 
who is attached to `AmazonElasticMapReduceFullAccess` policy.
Users in this group will be able to start and stop EMR Hadoop clusters.

Now, creating a single user who belongs to this group,
after you decide on `password`:

    aws iam --profile snu-user create-user --user-name user01
    aws iam --profile snu-user create-login-profile --user-name user01 --password $password
    aws iam --profile snu-user add-user-to-group --group-name HadoopStudents

Using simple bash, now it's trivial to create 10 of these users.

    for id in $(seq -f "%02g" 1 15)
    do
        aws iam --profile snu-user create-user --user-name user$id
        aws iam --profile snu-user create-login-profile --user-name user$id --password $password
        aws iam --profile snu-user add-user-to-group --user-name user$id --group-name HadoopStudents
        echo $i; 
    done

Then, test to see if a user id works by
signing on at [the AMS Management sign in page](https://648795808428.signin.aws.amazon.com/console/)
and try running a small cluster.


## Prepare and upload sample data to AWS S3

### Click prediction data
Download the click prediction data locally.
Assume files are available in `/mnt1/hadoop-click-prediction`:

    # run this first, since lynx can be unresponsive with very large download
    export LYNX_TEMP_SPACE=/mnt1/lynx-temp
    lynx http://labs.criteo.com/downloads/2014-kaggle-display-advertising-challenge-dataset/
    ...
    $ cd /mnt1/hadoop-click-prediction
    # Small subset
    $ head -10000 train.txt > train_first_10k.txt
    $ ll -h
        total 12G
        -rw-r--r-- 1 hadoop hadoop 1.9K Aug 22 23:08 readme.txt
        -rw-r--r-- 1 hadoop hadoop 1.4G Aug 22 23:03 test.txt
        -rw-r--r-- 1 hadoop hadoop 2.4M Jan 20 21:08 train_first_10k.txt
        -rw-r--r-- 1 hadoop hadoop  11G May 12  2014 train.txt
    $ wc -l *.txt 
        6042135 test.txt
        45840617 train.txt


Now, create a bucket and copy the files over:

    cd /mnt1/hadoop-click-prediction

    aws s3 mb s3://snu-sri-2015 --profile snu-user
    
    aws s3 cp . s3://snu-sri-2015/data/click-prediction/ --recursive --exclude "*" --include "*.txt" --profile snu-user


### Project Gutenberg data
Once the two files are downloaded to locally (see README.txt)
simply run:

    aws s3 cp data/pg10.txt s3://snu-sri-2015/data/gutenberg/ --profile snu-user
    aws s3 cp data/pg4300.txt s3://snu-sri-2015/data/gutenberg/ --profile snu-user


## Prepare and upload scripts to s3

Run:

    aws s3 cp src s3://snu-sri-2015/src/ --recursive --profile snu-user

        upload: src/wc_reducer.py to s3://snu-sri-2015/src/wc_reducer.py
        upload: src/wc_mapper.py to s3://snu-sri-2015/src/wc_mapper.py



## AWS sample data
The [AWS word count example](https://aws.amazon.com/articles/2273)
mentions the input data.

    aws s3 ls s3://elasticmapreduce/samples/wordcount/input/
    aws s3 cp s3://elasticmapreduce/samples/wordcount/input/0001 tmp
    more tmp

It is actually CIA world factbook dump.

