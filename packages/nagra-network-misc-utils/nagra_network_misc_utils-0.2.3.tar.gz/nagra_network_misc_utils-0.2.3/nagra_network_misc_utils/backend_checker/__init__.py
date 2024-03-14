import logging
import time

import click
import gitlab
from gitlab.exceptions import GitlabAuthenticationError, GitlabGetError

log = logging.getLogger('Backend Checker')

DEFAULT_SERVER = 'https://gitlab.kudelski.com/'
DEFAULT_MAX_RETRIES = 60
DEFAULT_RETRY_WAIT_INTERVAL = 60  # seconds

FINISHED_PIPELINE_STATUS = (
    'success',
    'failed',
    'canceled',
    'skipped',
)


def get_last_pipeline(project):
    pipelines = project.pipelines.list(all=True)
    if pipelines:
        return pipelines[0]
    return None


def get_pipeline_status(
    project,
    pipeline_id,
    max_retries=DEFAULT_MAX_RETRIES,
    retry_wait_interval=DEFAULT_RETRY_WAIT_INTERVAL,
):
    """
    Retrieve the final status of a finished pipeline.
    """
    for _ in range(max_retries):  # Prevent infinit loop
        status = project.pipelines.get(pipeline_id).status
        if status in FINISHED_PIPELINE_STATUS:
            return status
        log.info(
            'Pipeline currently in {0} status. Checking again in a minute'.
            format(status))
        time.sleep(retry_wait_interval)
    return ''


def check_target_pipeline_status(
    project,
    pipeline=None,
    max_retries=DEFAULT_MAX_RETRIES,
    retry_wait_interval=DEFAULT_RETRY_WAIT_INTERVAL,
):
    """
    Check the status of the last pipeline of the given repositor
    at the moment this function start.
    i.e. this will keep checking the same pipeline
    even if a new one is created while this function runs

    This function returns True if the pipeline finishes with "success",
    Returns False otherwise.
    (including if this function timeouts before the pipeline finishes)
    """
    if pipeline:
        pipeline = project.pipelines.get(pipeline)
    else:
        pipeline = get_last_pipeline(project)

    if not pipeline:
        return False
    status = get_pipeline_status(project,
                                 pipeline_id=pipeline.id,
                                 max_retries=max_retries,
                                 retry_wait_interval=retry_wait_interval)
    if status == 'success':
        log.info('Pipeline was successful.')
        return True
    else:
        log.error(('Pipeline failed with status {}. '
                   'Please check entire pipeline here: {}.').format(
                       status, pipeline.web_url))
        return False


@click.command('check', help='Check Pipeline status (default to the last one)')
@click.version_option('0.1.0', prog_name='hello')
@click.option(
    '-r',
    '--repository',
    'repo_name',
    help='Name of repository (e.g. network/paloalto/utils)',
    required=True,
)
@click.option(
    '-s',
    '--git-server',
    'server',
    default=DEFAULT_SERVER,
    help='Name of server (e.g. gitlab.kudelski.com)',
)
@click.option(
    '-t',
    '--gitlab-token',
    'api_key',
    envvar='GITLAB_TOKEN',
    help=('The access token required to manage gitlab'
          '(default to GITLAB_TOKEN environment variable)'),
    required=True,
)
@click.option('-p',
              '--pipeline',
              'pipeline_id',
              help=('The pipeline to check'
                    '(default to the last one)'))
def check_pipeline_status(repo_name: str, server: str, api_key: str,
                          pipeline_id: str):
    gl = gitlab.Gitlab(url=server, private_token=api_key)
    try:
        gl.auth()
    except GitlabAuthenticationError:
        log.error(('Authentication Failed. '
                   'Check the server and access token passed to the script'))
        exit(1)
    try:
        repo_name = repo_name.strip('/')
        project = gl.projects.get(repo_name)
    except GitlabGetError:
        log.error('Project does not exists')
        exit(1)

    if not check_target_pipeline_status(project, pipeline_id):
        exit(1)
