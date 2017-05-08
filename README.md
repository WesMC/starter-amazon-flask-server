# [Starter Amazon Flask Server](https://github.com/WesMC/starter-amazon-flask-server)
A starting point for amazon server instances that have git and ansible preconfigured. This starter uses Docker to create flask server instances with different production and staging versions.

## Table of Contents
- [Getting to AWS](#getting-to-aws)
- [References](#references)
- [Other Useful Commands](#other-useful-commands)

## Getting to AWS

You are using you given key to connect to your AWS EC2 Instance through SSH, command looks like

`ssh -i keyname-xxxxxxxxxx.key <IP address>`

The last entry in the command is YOUR specific IP address. If you have an issue with it saying

```
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@         WARNING: UNPROTECTED PRIVATE KEY FILE!          @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
```

Then you need to execute command: `chmod 0400 keyname-xxxxxxxxxx.key`, then re-run the ssh command, and it should work

Once on your instance run the command  

`lsb_release -a`

That should give us the information of the operating system. In this case, it should be almost like:

```bash
No LSB modules are available.
Distributor ID:	Ubuntu
Description:	Ubuntu 16.04.2 LTS
Release:	16.04
Codename:	xenial
```

Next, as long as you have either sudo or root privileges, you should run the command `sudo apt-get update -y` to update your VM

## References

## Other Useful Commands

Sometimes, there is no good way to fix or explore something without getting your hands dirty. Here are a few commands I'd keep track of when you're muddling through the mud.

#### How to delete docker images and containers

<b>WARNING - this will delete all images and containers, and it will not be recoverable</b>

```bash
echo "Delete all containers"
docker rm $(docker ps -a -q)
echo "Delete all images"
docker rmi $(docker images -q)
```
