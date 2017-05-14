# [Starter Amazon Flask Server](https://github.com/WesMC/starter-amazon-flask-server)

![Starter Amazon Flask Server Logo][logo]

A starting point for amazon server instances that have git and ansible preconfigured. This starter uses Docker to create flask server instances with different production and staging versions.

## Table of Contents
- [Flask Server Setup](#flask-server-setup)
  - [Make a Repo](#make-a-repo-for-verion-control)
  - [Code for Web App](#code-for-web-app)
  - [Unit / Acceptance Testing](#unit-acceptance-testing)
  - [Dockerfile and Docker](#dockerfile-and-docker)
- [Continuous Integration with Docker Cloud](#continuous-integration-with-docker-cloud)
- [AWS Instance](#aws-instance)
  - [Getting to AWS](#getting-to-aws)
- [References](#references)
- [Other Useful Commands](#other-useful-commands)

## Flask Server Setup

When we are already to start trying to deploy, this is a great start to double check that we have done everything.

### Make a Repo for Version Control

This is sort of self explanatory. You need Version Control for any deployable web app in order to achieve CI / CD / CD. For this project, we use Github.

### Code for Web App

In order to have any sort of web app, we need to make the web app in the first place. In our case, it is nothing more than importing Flask, defining a home root / index, then setting the python file to run the app by using:

```python
if __name__ == '__main__':
    app.run()
```

sometimes, you might want to run it in debug mode, or set the host IP and Port specifically as such: `app.run(debug=True, host='0.0.0.0', port=5000)`

### Unit / Acceptance Testing

Once we've written our app, we want to make sure that what the output is, is exactly what we expect it to be. For our app, we use a bash script to run a python3 script that imports a library called `unittest`. Using that, we set it so that it expects, and searches for our content that should be there.

### Dockerfile and Docker

With using docker, we are able to create virtual machine images that act as an OS with pre-installed programs and libraries that we want to use.

We also have a .yml file for our build tests for continuous integration on docker cloud. It executes the `Dockerfile` so that it builds, then it calls the `run_tests.sh` script to test if the flask server works.

As for what is in the Dockerfile, it should be setup in such a way that we can use the cached steps of previous versions of the file. With this in mind, its probably proper to separate the libraries every so many. In our example, we are updating the OS as well as installing python 3  and pip 3 within the same line, but after that we should separate how many libraries pip installs every so often. Because we only install flask as well as some of it's dependencies, theres no need to separate it in this case.

## Continuous Integration with Docker Cloud

With docker acting as the helm of how we setup our containers, it makes sense to use a continuous integration system with either Codeship, or Docker Cloud. In our case, we have setup with Docker Cloud.

First, we need to create a Docker Cloud account, then create a new repository, and within the options, we want to link our github account to it. Once linked, we need to setup rules with building our releases. On the builds tab of your repository on Docker Cloud, hit the 'Configure Automated Builds' button. Hit the plus (+) sign next to 'Build Rules', and for the source type we want to select 'Tag'. For the source, type in `/^[0-9.]+$/`, Docker tag should be `release-{sourceref}`, Dockerfile Location wherever the Dockerfile is located in the project. Build Context should be `/` and both autobuild and caching should be activated.



## AWS instance

Using a specified key, we login to our AWS instance using SSH, install docker and git software, clone the master Repo from Github. Once cloned, we want to build our image. Because at the time of this writing we have not achieved CI / CD / CD, we are going to do

```
sudo docker build -t test .
```

This translates to "'Build an image with the files in the current directory and tag it with the name 'test'"

Once complete, we are going to use the following command to run a container

```
sudo docker run -d -p 8080:5000 -t test python3 unh698.py tail -f /dev/null
```

it states that we want to run the container in a detached state, funnel all traffic from port 8080 of the host OS to the container's port 5000, using the image tagged as 'test', use python3 to run the file unh698.py as soon as it's started, and continuously run. The `tail -f /dev/null` may or may not be necessary. It depends if the application runs continuously runs in the foreground. For more information [check here](http://stackoverflow.com/questions/30209776/docker-container-will-automatically-stop-after-docker-run-d)


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

## References

* [Learn Git Branching](http://learngitbranching.js.org/) - Website to learn how to use Git effectively
* [Flask](http://flask.pocoo.org/) - Our python 3 based web server
* [Ansible](https://www.ansible.com/) - Used for automated configuration, see [Other README](ansible/README.md)
* [Amazon Web Service](https://aws.amazon.com/) - Used to host server
* [Docker](https://www.docker.com/) - Build containers that run our web app
* [Docker Cloud](https://cloud.docker.com/) - Used to perform build tests for our Web App

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

[logo]: https://raw.githubusercontent.com/WesMC/starter-amazon-flask-server/master/Images/finalLogo.png "Starter Amazon Flask Server"
