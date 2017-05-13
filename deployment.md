# Everything that is necessary on Flask Server Instance.

When we are already to start trying to deploy, this is a great start to double check that we have done everything.

## 1) Setup a repository on Github for Version Control

This is sort of self explanatory. You need Version Control for any deployable web app in order to achieve CI / CD / CD. For this project, we use Github.

## 2) Code for web app

In order to have any sort of web app, we need to make the web app in the first place. In our case, it is nothing more than importing Flask, defining a home root / index, then setting the python file to run the app by using:

```
if __name__ == '__main__':
    app.run()
```

sometimes, you might want to run it in debug mode, or set the host IP and Port specifically as such: `app.run(debug=True, host='0.0.0.0', port=5000)`

## 3) Unit / Acceptance Testing

Once we've written our app, we want to make sure that what the output is, is exactly what we expect it to be. For our app, we use a bash script to run a python3 script that imports a library called `unittest`. Using that, we set it so that it expects, and searches for our content that should be there.

## 4) Dockerfile for Docker containers / images

With using docker, we are able to create virtual machine images that act as an OS with pre-installed programs and libraries that we want to use.

We also have a .yml file for our build tests for continuous integration on docker cloud. It executes the `Dockerfile` so that it builds, then it calls the `run_tests.sh` script to test if the flask server works.

## 5) AWS instance

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
