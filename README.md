
# DiemBFT v4

The goal of this project is to implement a consensus 
protocol known as DiemBFT, which is responsible for 
forming agreement on ordering and finalizing transactions 
among a configurable set of validators.

## Platform

DistAlgo is a very high-level language for programming distributed algorithms. 

Distalgo version used: 1.1.0b15 

The implementation used for python is CPython and python version is 3.7.11

Operating System: macOS Big Sur, version 11.6

Type of host: Laptop

## Workload generation

Workload generated by the client is based on parameters in the config file.
The file which contains the implementation isdiemv4/client.da 

## Timeouts

Round timer = 4 * delta,  where delta = 10 seconds


## Bugs and Limitations

Program is going into an infinite loop in early iterations. We haven't implemented the genenis block generation code.

## Main Files

Pathname of files containing clients and replicas:

* Master : diemv4/master.da
* Replica : diemv4/validator.da
* Client : diemv4/client.da

## Code Size

Number of non-blank, non-comment lines of code:

* Algorithm: 379
* Other: 111
* Total: 490

We used CLOC (https://github.com/AlDanial/cloc) to find the code size which is non-blank and non-comment.

Percentage of code that is for the algorithm itself is 100%.

## Language feature usage

The number of:

* List comprehensions: 5
* Dictionary comprehensions: none
* Set comprehensions: none
* Aggregations: none
* Quantifications: none
* Await statements: 2
* Receive handler: 5

## Contributions

Each team member had equal share in the development and testing tasks.
