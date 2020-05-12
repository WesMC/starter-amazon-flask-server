# [Starter Amazon Flask Server](https://github.com/WesMC/starter-amazon-flask-server)

![Starter Amazon Flask Server Logo][logo]

A starting point for Amazon server instances that have Git and Ansible preconfigured. This starter uses Docker to create Flask server instances with separate production and staging versions. 

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

Before we can do any development on our web app, we need to ensure that we have something to work on. This is a great time to double-check that we have done everything correctly. 

### Make a Repo for Version Control

This is sort of self-explanatory. You need Version Control for any deployable web app to achieve CI / CD / CD. For this project, we use GitHub. If you don't know how to use Git, I suggest you go to [References](#references) below and do a few of the git exercises.

### Code for Web App

To have any sort of web app, we need to make the web app in the first place. In our case, it is only importing Flask, defining a home root/index, then setting the python file to run the app using: 

```python
if __name__ == '__main__':
    app.run()
```

sometimes, you might want to run it in debug mode, or set the host IP and Port specifically as such: `app.run(debug=True, host='0.0.0.0', port=5000)`. You might want to simply keep it as `app.run(debug=False, host='0.0.0.0', port=5000)` for later since the default port for Flask servers is 5000. When we get into Docker and Ansible, this can make things a little easier when we define how we funnel our traffic.

### Unit / Acceptance Testing

Once we've written our app, we want to make sure that the output is exactly what we expect it to be. For our app, we use a bash script to run a python3 script that imports a library called `unittest`. Using that, we set it to expect, and search for our content that should be there. 

### Dockerfile and Docker

Using Docker, we can create virtual machine images that act as OS with pre-installed programs and libraries to use. 

We also have a .yml file for our build tests for continuous integration on Docker Cloud. It executes the `Dockerfile` so that it builds, then it calls the `run_tests.sh` script to test if the Flask server works.

As for what is in the Dockerfile, it should be set up to use the cached steps of previous versions of the file. It's probably proper to separate the libraries every so many. In our example, we are updating the OS and installing python 3 and pip 3 within the same line, but after that, we should separate how many libraries pip installs. Because we only install Flask and some of its dependencies, there is no need to separate it. 

## Continuous Integration with Docker Cloud

With docker acting as the helm of how we set up our containers, it makes sense to use a continuous integration system with Codeship or Docker Cloud. In our case, we'll use Docker Cloud. 

First, we need to create a Docker Cloud account, create a new repository, and within the options we want to link our GitHub account. Once linked, we need to set rules to build our releases. On the builds tab of your repository on Docker Cloud, hit the 'Configure Automated Builds' button. Hit the plus (+) sign next to 'Build Rules', and for the source type, we want to select 'Tag'. For the source, type in `/^[0-9.]+$/`, Docker tag should be `release-{sourceref}`, Dockerfile Location wherever the Dockerfile is located in the project. Build Context should be `/` and both autobuild and caching should be activated.

## AWS instance

Using a specified key, we login to our AWS instance using SSH, clone the master Repo from GitHub, then run the Ansible configuration files. 

### Getting to AWS

Use your given key to connect to your AWS EC2 Instance through SSH. 

`ssh -i keyname-xxxxxxxxxx.key <IP address>`

The final entry in the command is YOUR specific IP address. If you have an issue with it saying

```
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@         WARNING: UNPROTECTED PRIVATE KEY FILE!          @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
```

Then you need to execute the command: `chmod 0400 keyname-xxxxxxxxxx.key`, then re-run the ssh command, and it should work.

Once on your instance run the command  

`lsb_release -a`

That gives us information about the operating system. In this case, it should be similar to: 

```bash
No LSB modules are available.
Distributor ID:	Ubuntu
Description:	Ubuntu 16.04.2 LTS
Release:	16.04
Codename:	xenial
```

## Ansible

Ansible is our automated configuration software. In short, it allows us to set up a server with three simple commands, rather than installing everything by hand. This is useful in DevOps when building larger applications. If there happens to be a lot of traffic through your servers to the point where it starts to slow down, we can spin up new instances to have load balancing across our web app. Another example is if a server has a hardware crash, we can create another instance almost immediately. 

For documentation on how we use Ansible, please see [our other documentation](ansible/README.md) for more information.

## Metrics

One of the last pieces of this puzzle is to set up a way to collect and analyze metrics. It can help show unexpected or unexplained errors and slow run times on your pages/URLs. We use [Prometheus](https://prometheus.io/) for its various tools to monitor our app.

In Prometheus, there are 4 tools: Counters, Gauges, Histograms, and Summaries. Counters and Gauges are similar in that they both are single numeric representations. Counters can only go up, while Gauges can go up and down arbitrarily. Histograms and Summaries are both used for sample observations. Summaries also provide a total number of observations, as well as observations over some time. Although not entirely accurate, think of Summaries as a collection of Histograms. 

### Setup for Flask Server metrics

Everything is already done for you. But in case you need a reference or want to explore it, the file titled `prometheus_metrics.py` houses all the logic for our metrics, and is accessible in our web app through: 

```python
from prometheus_metrics import setup_metrics
setup_metrics(app)
```

which is located at the top of `flask_server.py`

## References

* [Learn Git Branching](http://learngitbranching.js.org/) - Website to learn how to use Git effectively
* [Flask](http://flask.pocoo.org/) - Our python 3 based webserver
* [Ansible](https://www.ansible.com/) - Used for automated configuration, see [Other README](ansible/README.md)
* [Amazon Web Service](https://aws.amazon.com/) - Used to host server
* [Docker](https://www.docker.com/) - Build containers that run our web app
* [Docker Cloud](https://cloud.docker.com/) - Used to perform build tests for our Web App
* [Prometheus](https://prometheus.io/) - Used for measuring metrics across entre app

## Other Useful Commands

Here are a few other useful commands I'd keep track of:

#### How to delete docker images and containers

<b>WARNING - this will delete all images and containers, and it will not be recoverable</b>

```bash
echo "Delete all containers"
docker rm $(docker ps -a -q)
echo "Delete all images"
docker rmi $(docker images -q)
```

## Manual Installation and Configuration

If for some reason, we don't want to use Ansible to automatically configure our AWS instance, the manual process of bringing this together isn't too difficult. I will assume you can log in to your AWS instance, and I will start from that point. 

You first need to install Docker. Run the command `apt-get install docker-ce` or `apt-get install docker.io`, with a preference for the former.

Next, we want to clone our repository on Docker Cloud using:

```bash
# If no version is specified, "latest" is assumed
docker pull your-docker-username/your-docker-repo-name # appended to end (:latest)

# Specifying a version of the image is done by appending it to the image with a semicolon, and then selecting the version by tag or hash
docker pull your-docker-username/your-docker-repo-name:release-x.x.x
```

Once the docker repo is downloaded, change directories into it, and then run the following:

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
