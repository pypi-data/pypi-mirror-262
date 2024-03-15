# Rispack - Pack of shared libraries from Rispar

Rispack is a collection of libraries developed by Rispar to help with serverless development on AWS.


## Handler
The Handler module is designed to make serverless development on AWS Lambda functions easier. There is two types of handler: route and job.

### Route Handler
The **route** decorator is used to define a route (http endpoint) for a Lambda function. It handles the API requests and responses and makes it easy to define the route handlers.

Here's an example of using the route decorator to define a route handler:

```python
from rispack.handler import Request, Response, route
from actions import GetProfile
from params import GetProfileParams

@route
def get_profile(request: Request):
    params = GetProfileParams.load(request.params)
    profile = GetProfile.run(params)

    return Response.ok(profile)
```

The **route** decorator handles the incoming request and passes it to the decorated function. The decorated function must return a Response object with the appropriate HTTP status code and response body.

#### Interceptors
The route decorator also supports interceptors, which are functions that can be run before the route handler to perform additional checks or processing.

The two built-in interceptors are the **token interceptor** and the **role interceptor**.

#### Token Interceptor

The token interceptor checks if the request has a valid authorization token. You can add the token parameter to the route decorator to enable the token interceptor.

```python
@route(token=True)
def create_loan(request: Request):
    # ...
```

#### Role Interceptor

The role interceptor checks if the user has the required role to access the route. You can add the role parameter to the route decorator to enable the role interceptor.

```python
@route(role="PROFILE_VIEW")
def get_profile(request: Request):
    # ...
```


### Job Handler
The Rispack handler module also includes functionality for background job processing via the **@job** decorator. The provided job function parameter,
is based on the event being processed, which could be any supported AWS SAM events.

There is 2 built-in types, provided by the Rispack:

1. FileRecord - For S3 file events.
2. EventRecord - For SQS events (more details below).

Here is an example of a job using an FileRecord parameter:

```python
@job
def process_file(record: FileRecord):
    # do some processing with the file
```

And another one using EventRecord:

```python
@job
def process_event(record: EventRecord):
    # do something with the event payload
```

### Event System
Rispack's event system is designed around a fanout pattern, where events are published to SNS and then distributed to SQS queues. Each queue is responsible for handling the specific event that it receives.

It uses a strict payload format that must be used to ensure proper functionality. This format is defined by the EventRecord class:

```python
class EventRecord:
    id: UUID
    aggregate_id: UUID
    payload: Dict[str, Any]
    type: str
    origin: str
    at: datetime
    version: str
```

The **EventRecord** class contains information such as the event ID, the aggregate ID, the payload data, and the event type, among other fields. This information is used by the event system to ensure that events are handled correctly and consistently.


## Database
Manage connection to RDS Cluster (or RDS Proxy) via Secret Manager.

## AWS
The AWS module included in the Rispack provides functions that simplify the use of some AWS services in Python. Here's a brief explanation of each function:

**get_signed_auth()**

Returns a signed URI for calling endpoints with IAM authorization. This is useful for accessing protected APIs, such as those created with AWS API Gateway.

**get_ssm_parameter(name: str, encrypted: bool = False) -> str**

Returns a parameter value from the Systems Manager parameter store.

- name: The name of the parameter.
- encrypted: Flag indicating whether the value is encrypted or not.

**put_ssm_parameter(name: str, value: str, param_type: str = "String", overwrite: bool = True) -> int**

Creates or updates a parameter in the Systems Manager parameter store.

- name: The name of the parameter.
- value: The value to be stored.
- param_type: The type of the parameter. Default is "String".
- overwrite: Whether to overwrite an existing parameter. Default is True.

**get_secret(name: str) -> str**

Returns a secret value from AWS Secrets Manager.

- name: The name of the secret.

**enqueue(queue_name: str, message: Any) -> None**

Adds a new message to an Amazon Simple Queue Service (SQS) queue.

- queue_name: The name of the SQS queue.
- message: The message to publish.

**get_url(bucket_name: str, object: str, expiration_in_seconds: int = 300) -> str**

Returns a presigned URL for an Amazon S3 object.

- bucket_name: The name of the S3 bucket.
- object: The complete object path.
- expiration_in_seconds: The period in seconds until URL expiration. Default is 300 (5 minutes).



## Schemas
Base Schema for entities, events and other data classes.


## Logger
AWS Lambda Powertools logger

## Stores
Base Store class and decorators to work with transactions
