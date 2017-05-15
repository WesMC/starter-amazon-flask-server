# [Starter Amazon Flask Server](https://github.com/WesMC/starter-amazon-flask-server)

![Starter Amazon Flask Server Logo][logo]

A starting point for Amazon server instances that have Git and Ansible preconfigured. This starter uses Docker to create Flask server instances with different production and staging versions.

## Table of Contents
- [Flask Server Setup](#flask-server-setup)
  - [Make a Repo](#make-a-repo-for-verion-control)
  - [Code for Web App](#code-for-web-app)
  - [Unit / Acceptance Testing](#unit-acceptance-testing)
  - [Dockerfile and Docker](#dockerfile-and-docker)
- [Continuous Integration with Docker Cloud](#continuous-integration-with-docker-cloud)
- [AWS Instance](#aws-instance)
  - [Getting to AWS](#getting-to-aws)
- [Ansible](#ansible)
- [Metrics](#metrics)
  - [Setup for Flask Server metrics](#setup-for-flask-server-metrics)
- [References](#references)
- [Other Useful Commands](#other-useful-commands)
- [Manual Installation and Configuration](#manual-installation-and-configuration)

## Flask Server Setup

Before we can do any development on our web app, we need to ensure that we have something to work on. This is a great time to double check that we have done everything correctly for that.

### Make a Repo for Version Control

This is sort of self explanatory. You need Version Control for any deployable web app in order to achieve CI / CD / CD. For this project, we use Github. If you don't know how to use Git, I suggest you go [References](#references) below and do a few of the git exercises.

### Code for Web App

In order to have any sort of web app, we need to make the web app in the first place. In our case, it is nothing more than importing Flask, defining a home root / index, then setting the python file to run the app by using:

```python
if __name__ == '__main__':
    app.run()
```

sometimes, you might want to run it in debug mode, or set the host IP and Port specifically as such: `app.run(debug=True, host='0.0.0.0', port=5000)`. You might want to simply keep it as `app.run(debug=False, host='0.0.0.0', port=5000)` for later since the default port for Flask servers are 5000. As when we get into Docker and Ansible, this can make things a little easier when we define how we're funneling our traffic.

### Unit / Acceptance Testing

Once we've written our app, we want to make sure that the output is exactly what we expect it to be. For our app, we use a bash script to run a python3 script that imports a library called `unittest`. Using that, we set it so that it expects, and searches for our content that should be there.

### Dockerfile and Docker

With using docker, we are able to create virtual machine images that act as an OS with pre-installed programs and libraries that we want to use.

We also have a .yml file for our build tests for continuous integration on docker cloud. It executes the `Dockerfile` so that it builds, then it calls the `run_tests.sh` script to test if the flask server works.

As for what is in the Dockerfile, it should be setup in such a way that we can use the cached steps of previous versions of the file. With this in mind, its probably proper to separate the libraries every so many. In our example, we are updating the OS as well as installing python 3  and pip 3 within the same line, but after that we should separate how many libraries pip installs every so often. Because we only install flask as well as some of it's dependencies, theres no need to separate it in this case.

## Continuous Integration with Docker Cloud

With docker acting as the helm of how we setup our containers, it makes sense to use a continuous integration system with either Codeship, or Docker Cloud. In our case, we have setup with Docker Cloud.

First, we need to create a Docker Cloud account, then create a new repository, and within the options, we want to link our github account to it. Once linked, we need to setup rules with building our releases. On the builds tab of your repository on Docker Cloud, hit the 'Configure Automated Builds' button. Hit the plus (+) sign next to 'Build Rules', and for the source type we want to select 'Tag'. For the source, type in `/^[0-9.]+$/`, Docker tag should be `release-{sourceref}`, Dockerfile Location wherever the Dockerfile is located in the project. Build Context should be `/` and both autobuild and caching should be activated.

## AWS instance

Using a specified key, we login to our AWS instance using SSH, clone the master Repo from Github, then run the ansible configuraton files.

### Getting to AWS

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

## Ansible

Ansible is our automated configuration software. It in short lets up setup a server with three simple commands, rather than individually installing everything by hand. This can be quite useful in the world of DevOps. For instance, there happens to be a lot of traffic going through your servers to the point where it's starting to slow down. Now with Ansible, we can spin up new instances in order to have load balancing across our web app. Another example, is if for some reason a server has a hardware crash, then we can easily spin up another instance within seconds, not minutes or hours.

For the documentation of how we have setup Ansible, please see [our other documentation](ansible/README.md) for more information.

## Metrics

One of the last pieces of this puzzle is to setup a means of collecting and analyzing metrics. It can help show where there are unexpected or unexplained errors and slow run times on your pages / URLs. In our case, we have a [Prometheus](https://prometheus.io/) server using various tools and measurements to monitor our app.

In Prometheus, there are 4 types of tools used: Counters, Gauges, Histograms, and Summaries. Counters and Gauges are similar in that they both are single numeric representations, however Counters can only go up, while Gauges can go up and down arbitrarily. Histograms and Summaries are both used for sample observations, however, Summaries also provide a total count of observations, as well as observations over a period of time. Think of Summaries as a collection of Histograms, and you wouldn't be far off in your thinking.

### Setup for Flask Server metrics

Everything is already done for you. But in case you need a reference or want to explore it, the file titled `prometheus_metrics.py` houses all of the logic for our metrics, and is access in our web app through:

```python
from prometheus_metrics import setup_metrics
setup_metrics(app)
```

which is located at the top of `flask_server.py`

## References

* [Learn Git Branching](http://learngitbranching.js.org/) - Website to learn how to use Git effectively
* [Flask](http://flask.pocoo.org/) - Our python 3 based web server
* [Ansible](https://www.ansible.com/) - Used for automated configuration, see [Other README](ansible/README.md)
* [Amazon Web Service](https://aws.amazon.com/) - Used to host server
* [Docker](https://www.docker.com/) - Build containers that run our web app
* [Docker Cloud](https://cloud.docker.com/) - Used to perform build tests for our Web App
* [Prometheus](https://prometheus.io/) - Used for measuring metrics across entre app

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

## Manual Installation and Configuration

If for some reason, we don't want to use ansible to automatically configure our AWS instance, the manual process of bringing this together isn't too difficult. I will be assuming that you can login into your AWS instance, and I will be beginning from that point.

You first need to install Docker. Run the command `apt-get install docker-ce` or `apt-get install docker.io`, with a preference for the former.

Next, we want to clone our repository on Docker Cloud using:

```bash
# If no version is specified, "latest" is assumed
docker pull your-docker-username/your-docker-repo-name # appended to end (:latest)

# Specifying a version of the image is done by appending it to the image with a semicolon, and then selecting the version by tag or hash
docker pull your-docker-username/your-docker-repo-name:release-x.x.x
```

Once the docker repo is downloaded, change directories into it and then run the following:

```bash
sudo docker build -t docker-instance-name .
```

This translates to "'Build an image with the files in the current directory and tag it with the name 'test'"

Once complete, we are going to use the following command to run a container

```bash
sudo docker run -d -p 8080:5000 -t docker-instance-name python3 flask_server.py
```

it states that we want to run the container in a detached state, funnel all traffic from port 8080 of the host OS to the container's port 5000, using the image tagged as 'test', use python3 to run the file flask_server.py as soon as it's started.

The container should now be working.


[logo]: https://raw.githubusercontent.com/WesMC/starter-amazon-flask-server/master/Images/finalLogo.png "Starter Amazon Flask Server"
