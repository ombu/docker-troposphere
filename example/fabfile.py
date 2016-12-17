import os
import sys
from datetime import datetime
from boto import cloudformation
from fabric.api import task, run, runs_once, env

@task
@runs_once
def list_stacks():
    """
    List stacks
    """
    stacks = _get_cf_connection().describe_stacks()
    for stack in stacks:
        print " - %s\t%s\t%s" % (stack.stack_name, stack.creation_time,
                                 stack.stack_status)


@task
@runs_once
def create(name, template):
    """
    Launches the stack.
    :param template: The template name
    :param name: The stack name
    """
    result = _get_cf_connection().create_stack(
        "%s-%s-%s" % (name,
                      datetime.now().strftime("%Y%m%d"),
                      datetime.now().strftime("%H%M%S%z")
                      ),
        template_body=_get_template(template).to_json(),
        capabilities=['CAPABILITY_IAM'],
        parameters=default_parameters,
        )
    print(result)


@task
@runs_once
def delete(name):
    """
    Deletes the stack.
    :param name: The stack name
    """
    print(_get_cf_connection().delete_stack(name))


@task
@runs_once
def status(name):
    """
    Get the status of the stack.
    :param name: The stack name
    """
    stack = _get_cf_connection().describe_stacks(name)[0]
    for e in stack.describe_events():
        print " - %s\t%s\t%s" % (e.resource_status, e.resource_type,
                                 e.resource_status_reason or '')
    print("Stack status: %s" % stack.stack_status)


@task
@runs_once
def list_stacks():
    """
    List stacks
    """
    stacks = _get_cf_connection().describe_stacks()
    for stack in stacks:
        print " - %s\t%s\t%s" % (stack.stack_name, stack.creation_time,
                                 stack.stack_status)


@task
@runs_once
def status(name):
    """
    Get the status of the stack.
    :param name: The name of the stack
    """
    stack = _get_cf_connection().describe_stacks(name)[0]
    for e in stack.describe_events():
        print " - %s\t%s\t%s" % (e.resource_status, e.resource_type,
                                 e.resource_status_reason or '')
    print("Stack status: %s" % stack.stack_status)
    if hasattr(stack, 'outputs'):
        print "\nOutputs:"
        for output in stack.outputs:
            print " - %s\n\t%s\n\t%s" % (output.key, output.value,
                                         output.description or '')


@task
@runs_once
def render_template(template):
    """
    Prints the stack's template.
    :param template: The template name
    """
    print(_get_template(template).to_json())


def _get_template(template):
    sys.path.append('cloudformation')
    return __import__(template).template


def _get_cf_connection():
    conn = cloudformation.connect_to_region(os.environ['AWS_DEFAULT_REGION'])
    try:
        conn.region
        return conn
    except AttributeError:
        print "Unable to obtain a Cloud Formation connection. Review the " \
              "README to ensure you've provided the correct environment to " \
              "connect to AWS."
        exit()


