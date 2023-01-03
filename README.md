# ROUCAIROL-CARVALHO MUTUAL EXCLUSION IMPLEMENTATION WITH PYTHON AND GRPC

## Project Description

The project implements a distributed mutual exclusion algorithm called ROUCAIROL-CARVALHO which is an improvement of RICART-AGRAWALA algorithm. The most important attribute of the ROUCAIROL-CARVALHO algorithm is its efficiency, it may reduce the number of messages required to communicate between the processes to 0. The worst case message complexity is 2(N-1), N being the number of processes.

Here we implemented the algorithm in Python using the gRPC framework to communicate across processes. The clients send request to the server in order to access the critical section. If they are granted for the critical section they will update the "diary" by writing a message. The message consists process id.

## File Description

There are 3 pdf files, one for [describing the algorithm](https://github.com/cihanevren/Mutex/blob/main/algorithm_description.pdf), one for [explaining the implementation](https://github.com/cihanevren/Mutex/blob/main/algorithm_implementation.pdf) and for [the UML diagram](https://github.com/cihanevren/Mutex/blob/main/algorithm_workflow.pdf) of the workflow.


The server.py python file is to run the server and there are 4 client.py python files to run up the clients.


Mutex.proto is the protocol buffer file to generate python libraries for communication. Namely, mutex_pb2.py, mutex_pb2.pyi, mutex_pb2_grpc.py files.

## Run Guide

First start the server by running the server.py from a terminal. Secondly lit up another terminal to start the clients. For each client.py file, we need to open another terminal. The clients will automatically start sending requests to the server to access the critical section, there is some randomness implemented in the code so it may wait for a while till it sends the first request. The server will recieve requests and update the diary.

To stop the server or clients, use keyboard interruption (ctrl+c).

In case you need to regenerate grpc python libraries use;

"python -m grpc_tools.protoc -I=. --python_out=. --pyi_out=. --grpc_python_out=. mutex.proto"

This will create the mutex_pb2.py, mutex_pb2.pyi, mutex_pb2_grpc.py files.
