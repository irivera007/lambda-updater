import boto3
import time
import logging
from botocore.exceptions import ClientError

def update_lambda(name,uri,region):
    '''
    Initialize the boto client
    '''
    session = boto3.session.Session()
    client = session.client(
    service_name = 'lambda',
    region_name = region
    )

    '''
    Make the update request
    '''
    response = client.update_function_code(
    FunctionName = name,
    ImageUri = uri,
    Publish = True
    )

    return response

def lambda_handler(event, context):
    '''
    Initialize logger
    '''
    log = logging.getLogger(" __LambdaUpdater__ ")
    log.setLevel(logging.INFO)

    '''
    Add the name of the lamba that will be updated
    '''
    lambda_name = "add-docker-based-lambda-name"

    '''
    Gather all the required info from the event comming from EventBridge
    '''
    eventName = event.get('detail').get('eventName')
    eventSource = event.get('detail').get('eventSource')
    region = event.get('detail').get('awsRegion')
    registry = event.get('detail').get('requestParameters').get('registryId')
    repo = event.get('detail').get('requestParameters').get('repositoryName')
    tag = event.get('detail').get('requestParameters').get('imageTag')
   
    log.info('Details are:  event: {0}, source: {1}, region: {2}, registry: {3}, repo: {4}, tag: {5}'.format(eventName, eventSource, region, registry, repo, tag))

    image_uri = registry+".dkr.ecr."+region+".amazonaws.com/"+repo+":"+tag

    '''
    Allow some time while the image fully registers in ECR and visible to Lambda
    '''
    time.sleep(5)
    response = update_lambda(lambda_name, image_uri,region)

    log.info('Response: {0}'.format(response))