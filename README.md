# A Simple Counter Resource for Concourse

A simple incrementing counter to version [concourse][concourse] pipelines.

## Overview

This is a simple resource that's meant to act as a simpler versioning scheme
than the concourse provided [semver][semver].

The `semver` resource is great for a pipeline that publishes something for
consumption (such as an executable or library).

However, there are a lot of cases in which a simple incrementing count would do.
This resource is for pipelines that do not need the concept of a major, minor,
or patch version.

If you currently use the `semver` resource but bump just one of major, minor, or
patch, then this might be for you.

## Resource Configuration

Currently s3 is the only backend that is supported for storing the state of the
counter. As such, the `source` configuration for the counter resource deals with
defining the s3 object that will store the counter.

_Required_ fields:

  - `bucket`: The name of the s3 bucket
  - `key`: The name of the key within the bucket

_Optional_ fields:

  - `aws_access_key_id`: The access key used for s3 access
  - `aws_secret_access_key`: The secret key used for s3 access
  - `region`: The region of the bucket

Note that [boto3][boto3] is used internally. This means that any other way of
providing [credentials][cred] can be used (instance profiles, environment
variables, or aws configure).

The following is an example resource configuration:

    resources:
    - name: counter
      type: counter-resource
      source:
        bucket: 'test-bucket'
        key: 'some_folder/counter/count'

    resource_types:
    - name: counter-resource
      type: docker-image
      source:
        repository: jinlee/counter-resource

## Parameters

This section defines the parameters you can pass when using the resource in a
task.

### Get

There's only one optional parameter for the `get` task:

  - `inc`: Defaults to false. If set to true, will increment the counter
    locally, but not on s3

Note that concourse does seem to support the many ways of passing boolean values
in yaml. Check the [example][example].

### Put

There's only one required parameter for the `put` task:

  - `file`: The path to the file with the count. In most cases this should be
    the same file placed with the `get` task. However, it can be any file with a
    single non-negative value.

## Usage

The `get` task will place a file in `resource-name/count`, where the content is
the count.

This resource should be the most useful when used in the first job of the
pipeline. Its purpose is to tag a single run of the pipeline with a unique
number. Use it with `inc: true` at the beginning of the job, and place the put
task as the very last step. This ensures that you will only bump up the counter
if the entire job was successful. Otherwise you would be bumping up the counter
unnecessarily.

A simple `get` with an increment (with an example of how to use it with the [s3
resource][s3]):

    plan:
    - get: counter
      params: {inc: yes}
    - task:
      ... produce artifact-$(cat counter/count).jar ...
    - put: s3
      params: {file: artifact-*.jar}
    - put: counter
      params: {file: counter/count}

If the counter is required in a downstream job, leave out the `inc`:

    plan:
    - get: counter
      passed: [prev-job]
    - task:
      ... do something ...

Check out the [example][example] pipeline using the counter resource.

## Required S3 Policy

The resource requires just two s3 actions: `s3:GetObject` and `s3:PutObject`.

The IAM Policy should look something like this:

    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Action": [ "s3:GetObject", "s3:PutObject" ],
          "Resource": [
            "arn:aws:s3:::test-bucket/some_folder/counter/count"
          ]
        }
      ]
    }

[boto3]:     https://boto3.readthedocs.io/en/latest/
[concourse]: https://concourse.ci/
[cred]:      https://boto3.readthedocs.io/en/latest/guide/configuration.html
[example]:   example.yml
[s3]:        https://github.com/concourse/s3-resource
[semver]:    https://github.com/concourse/semver-resource
