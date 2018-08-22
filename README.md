Using the Troposphere Docker image
===================================

A Docker image for building AWS stacks with
[Troposphere](https://github.com/cloudtools/troposphere). Also includes Fabric
and the AWS CLI to help launch and manage stacks.

Build the Docker image locally
------------------------------

    docker build -t ombu/troposphere:1.9.6 .

Push the local image to the remote repository
---------------------------------------------

The image `ombu/troposphere` in Docker Hub is configured to build images
for every new tags pushed to Github, so there's no need to push locally built
images. This should suffice to trigger a new image build:

    git commit -m 'Upgrades troposphere to 1.9.6'
    git tag 1.9.6
    git push --tags

Docker Hub builds for the image can be tracked here:
https://hub.docker.com/r/ombu/troposphere/builds/

Run
---

The repo includes an example fabfile with tasks to build Troposphere templates
and manage stacks in Cloudformation. To get a list of available tasks in the
example fabfile:

    docker run -v $PWD/example:/tmp ombu/troposphere:1.9.6 fab -l

To run a task that talks to AWS you have to export your AWS credentais to the
environment:

    export AWS_DEFAULT_REGION=us-west-2
    export AWS_ACCESS_KEY_ID=...
    export AWS_SECRET_ACCESS_KEY=...

    docker run -v $PWD/example:/tmp \
    -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY -e AWS_DEFAULT_REGION \
    ombu/troposphere:1.9.6 fab list_stacks

