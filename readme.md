# UMassCTF '24 Challenge Release Repo

Each challenge follows the following hierarchy: `category/challenge_name/`
and includes the following:

- `README.md` - This file should contain a description and how to solve it along with the flag and other notes.
- `/challenge` - The directory containing the challenge source and build/run information
- `/static` - This directory contains the file(s) that are static
- `/solve` - This directory contains any file(s) and scripts used to solve the challenge
- `/challenge.yaml` - The kctf config for deploying the challenge
- `/metadata.yaml` - A yaml config that stores the public data for the challenge

## How to Run
This repo is set up as a kctf project so to run it you either need a Kubernetes cluster or docker. To run most of the challenges(everything except web/cash_cache and pwn/red40), first, activate the kctf environment:
```
source kctf/activate
```
Then just cd into the project you want to run and run it with docker
```
cd category/challenge_name
kctf chal debug docker
```
### How to Run cash_cache
Make sure you have docker-compose then just use it to spin up the file located in 
```
docker-compose -f ./web/cash_cache/challenge/docker-compose.yml up
```
### How to Run red40
Just use docker to build and run the docker file in pwn/red40/challenge
