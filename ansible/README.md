# Automated Configuration with Ansible

With our main work within the flask server, we want to have the ability to configure and spin up docker containers relatively easily. It's more or less a question of 'when' versus 'if' you ever come across a complete server failure

Now that we have a good idea (and documentation) of how to configure a
server to run our starter flask website within a docker container, we're
going to take the additional step of automating the configuration
of the host using Ansible (https://www.ansible.com/).

We're also going to take the additional step of running two instances
of your website in separate docker containers.  The first
will be the production version which will be accessible on
port 8080 and will be running the previously tagged version of
your website (Just the main page with the flask Website).  The
second container will be running the newest tagged version of
the website and accessible on port 8081.

Ansible is a open-sourced automation platform that can help with configuration management and application deployment. It is currently supported by Red Hat.

## How it works

Ansible works via a tier system within the `ansible` folder. Within this folder is one of two different structures (according to the [Documentation](http://docs.ansible.com/ansible/playbooks_best_practices.html#content-organization)). Our example uses the first structure:

```
production                # inventory file for production servers
staging                   # inventory file for staging environment

group_vars/
   group1                 # here we assign variables to particular groups
   group2                 # ""
host_vars/
   hostname1              # if systems need specific variables, put them here
   hostname2              # ""

library/                  # if any custom modules, put them here (optional)
filter_plugins/           # if any custom filter plugins, put them here (optional)

site.yml                  # master playbook
webservers.yml            # playbook for webserver tier
dbservers.yml             # playbook for dbserver tier

roles/
    common/               # this hierarchy represents a "role"
        tasks/            #
            main.yml      #  <-- tasks file can include smaller files if warranted
        handlers/         #
            main.yml      #  <-- handlers file
        templates/        #  <-- files for use with the template resource
            ntp.conf.j2   #  <------- templates end in .j2
        files/            #
            bar.txt       #  <-- files for use with the copy resource
            foo.sh        #  <-- script files for use with the script resource
        vars/             #
            main.yml      #  <-- variables associated with this role
        defaults/         #
            main.yml      #  <-- default lower priority variables for this role
        meta/             #
            main.yml      #  <-- role dependencies
        library/          # roles can also include custom modules
        lookup_plugins/   # or other types of plugins, like lookup in this case

    webtier/              # same kind of structure as "common" was above, done for the webtier role
    monitoring/           # ""
    fooapp/               # ""
```

What we are mainly using are top level `.yml` files, that use packages that are configured via roles. Within the roles, we setup our docker, and our flask Server. For more information on what these files do, I would direct you to the official [Reference](http://docs.ansible.com/ansible/index.html)

## Setup

Here, we'll use git as a method for tracking changes to your ansible playbook and deploying it onto your AWS instance.

1) Login to your new AWS server, clone your starter-amazon-flask-server repository.

```bash
cd ~
git clone [your starter-amazon-flask-server repo]
cd [your starter-amazon-flask-server repo]
git checkout pick-a-branch-name
```

2) Run the configure-host.yml playbook (on the AWS server) as-is to verify ansible is setup.

```bash
# Replace xxxxxxx here with your AWS username
ansible-playbook configure-host.yml -v --extra-vars "username=xxxxxxx"
```

Make changes to the ansible playbook locally, `git push` them to github and
`git pull` them down on your AWS instance for testing.

## Playbooks

There are three playbooks included here:

* configure-host.yml
* deploy-website-production.yml
* deploy-website-staging.yml


### Playbook - configure-host.yml

This playbook configures the local machine to run docker.
When executed, the playbook should install and run the
community edition of docker found from docker's official
apt repository.

Run this command on your AWS instace.

```bash
# Replace xxxxxxx here with your AWS username
ansible-playbook configure-host.yml -v --extra-vars "student_username=xxxxxxx"
```

### Playbook - deploy-website-staging.yml, deploy-website-production.yml

These playbooks deploy and start two versions of your website.
One a production instance and the second a staging version.

Run the playbooks with these commands

```bash
ansible-playbook deploy-website-production.yml -v
ansible-playbook deploy-website-staging.yml -v
```

## Completion and Final Testing

As with any testing, you always want to check to see if it is up and running correctly. Go to your specified URL and then check:

* The url for your production instance's main webpage
* The url for your staging instance's main webpage
* The url for your github pull request
