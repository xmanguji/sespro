# AWS Deployment
#### How to deploy the API to a serverless environment

## Requirements
1. Docker image(s) (for Lambda)
2. A PostgreSQL database (and corresponding user) + uuid extension
3. An S3 bucket
4. An ECR repository to push the docker images to (e.g report-api-dev-NAME)

## Instructions
1. Prepare the Lambda function(s) by uploading images to ECR and then creating a lambda function with them
2. Configure each function with the corresponding environment variables that the python app requires
3. Ensure the Lambda function(s) have access to the correct services through permissions - for example, the API needs permission for the S3 bucket, SES, and to execute other Lambda functions. This can be done by going to the Lambda function and checking its **Execution Role** and attaching policies there.
4. Create an API instance using API Gateway. Define a single route and make it a Lambda proxy. The default settings are fine, just ensure to check all request types (GET, POST, OPTIONS, etc). It will ask for the name of the Lambda function that holds the API.
5. Once this is done, use the "Deploy" option to 'deploy' the API to a stage. This stage is what must be configured as `API_ROOT_PATH` in the configuration. Example: a stage named "staging" requires an `API_ROOT_PATH` of `/staging`
6. After deploying to an API Gateway stage, it should give you an URL for that stage that represents the root URL of the API.
7. Provided everything is configured correctly, you should be able to visit the `openapi.json` URL to confirm the API is functioning (usually `/v1_0/openapi.json` from the root URL).

## Troubleshooting
* API Gateway's root URL should be your first step in debugging. It will return descriptive errors if it is configured incorrectly/cannot execute lambda.
* Each lambda function has a `Monitor` section. You can hit a button there that says `View Logs in CloudWatch` which gives you the latest execution logs of the function.
* Remember to cover all the environment variables in each lambda function that is required for configuration.
* When updating a Lambda function (either deploying a new images or changing env vars) - it will sometimes cache for a few runs before running the new configuration.