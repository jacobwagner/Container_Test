# Container_Test

# Installation

- cd /opt && git clone https://github.com/hakusama1024/Container_Test.git
- cd Container_Test
- pip install --upgrade pip
- pip install -r requirements.txt

# Execution

- Execute the command python main.py


# Overview 

The main class in this project is stack.py which provide base class and api for chaos creation. 

infoParser.py : provide a sample parser for inventory which return a instance of stack. you could wirte your own parser. 

serviceParser.py : return a serviceDic which contains all the services. you could add service to services.json.

in stack.py it provide container test and service test. 
    container test will first update container info and generate two lists for running containers and stoped containers. 
    then it will random choose one container to start or stop. 

    service test first will get servicedic, then update service state. also service test needs to generate running list and stoped list. 
    after get a random node it will create joblist for start/stop the service in the node. 

# Usage 

Usage : python main.py [container | service] [loglevel]


