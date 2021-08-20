# Lambda updater
> A tiny script that simplifies the update of ECR-Docker based Lambdas.

<br/>

Docker based lambdas are a great way to overcome some of the limitations that regular lambdas have like: size of the code.
Unfortunately docker based lambdas do not auto update after a new image version has been pushed, this process has to be done manually.
This script that also runs in lambda is intented to solve that.

### Technologies used:

- AWS EventBridge
- AWS Lambda to run this code
<br/>

### How does this script solve the problem?

After a new image push:

 - A CloudTrail event is generated
 - EventBridge catches the even and parses it based on a rule
 - If event matches the rule, EventBridge then triggers the Lambda-updater
 - Lambda-updater executes an 'update-function-code' based on the recently pushed image tag, to the predefined docker based lambda
<br/>


## Steps to deploy

 - Create an IAM role with minimal permissions to be able to update the desired docker based lambda
 - Create a new python based lambda (Lambda-updater), make sure to use the role created before and use the same region as the docker based lambda
 - Copy the `updater.py` code into the Lambda-updater and make sure to add the name of the docker based lambda
      ```
      lambda_name = "add-docker-based-lambda-name"
      ```
 - Create the EventBridge rule that will catch the "push" event from CloudTrail. Add the corresponding ECR repository name in the rule.
      ```
      {
        "detail": {
          "eventSource": ["ecr.amazonaws.com"],
          "eventName": ["PutImage"],
          "requestParameters": {
            "repositoryName": ["add-ecr-repo-here"]
            }
        }
      }
      ```
      - Select the Lambda-updater as Target
<br/>

## Note:
  - This script assumes will run in the same region as the docker based lambda.
  - This script depends on the name the lambda that will be updated. In order to create a more generic script that can update any docker based lambda,
the ECR reposositories have to be named in a way that match their corresponding lambdas, then the lambda name can be created from the event sent to the 
Lambda-updater.