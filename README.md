# A Simple Counter Resource for Concourse

This is a simple resource that's meant to act as a simpler versioning scheme
then the concourse provided [semver][semver].

The [semver][semver] resource is great for versioning pipelines that eventually
gets published for consumption (and thus need the concept of major, minor, and
patch versioning).

However, there are cases where a simple incrementing counter will do. This
resource can keep track of each run of the pipeline with an incrementing
counter. This is useful for pipelines that create artifacts for deployment or do
the deployment piece itself.

## Source Configuration

_Required_ fields:

  - `bucket`: The bucket that is used to keep state of the counter
  - `key`: The key that will be storing the state of the counter

_Optional_ fields:

  - `aws_access_key_id`: The access key to use for s3 access
  - `aws_secret_access_key`: The secret key to use for s3 access
  - `region`: The region for s3 access

Note that [boto3][boto3] is used internally. This means that any other way of
providing [credentials][cred] can be used (instance profiles, ENV variables,
etc).

## Parameters

There's only one optional parameter for the `get` task:

  - `inc`: Defaults to false. If set to true, will increment the counter locally,
    but not on s3

There's only one required parameter for the `put` task:

  - `file`: The path to the file with the count. In most cases this should be
    the same file placed with the `get` task. However it can be any file with a
    single non-negative value.

Note that concourse does seem to support the many ways of passing boolean values
in yaml. Check the [example][example].

## Usage

The `get` task will place a file in `resource-name/count`, where the content is
the count.

This resource should be the most useful used in the first job of the pipeline.
It's purpose is to tag a single run of the pipeline with a unique number. Use
it with `inc: true` at the beginning of the job, and place the put task as the
very last step.

This ensures that you will only bump up the counter if the entire job was
successful. Otherwise you would be bumping up the counter unnecessarily.

For a working example, check out [example][example].

A simple get with an increment (with an example of how to use it with [s3
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

If the counter is required in a downstream job, leave out the `inc`.

    plan:
    - get: counter
      passed: [prev-job]
    - task:
      ... do something ...

[semver]:  https://github.com/concourse/semver-resource
[s3]:      https://github.com/concourse/s3-resource
[boto3]:   https://boto3.readthedocs.io/en/latest/
[cred]:    https://boto3.readthedocs.io/en/latest/guide/configuration.html
[example]: example.yml
