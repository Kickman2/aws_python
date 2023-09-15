import boto3

client = boto3.client('config')


response = client.select_aggregate_resource_config(
    Expression="SELECT \
        configuration.instanceId, \
        accountId, \
        availabilityZone, \
        awsRegion, \
        configuration.architecture, \
        configuration.platform, \
        configuration.clientToken, \
        configuration.cpuOptions.coreCount, \
        configuration.cpuOptions.threadsPerCore, \
        configuration.launchTime, \
        configuration.iamInstanceProfile.arn, \
        configuration.imageId, \
        configuration.instanceType, \
        configuration.launchTime, \
        configuration.privateIpAddress, \
        configuration.state.name, \
        resourceCreationTime, \
        resourceType, \
        tags \
        WHERE resourceType = 'AWS::EC2::Instance'",
    ConfigurationAggregatorName='<required_aggregator>',
    Limit=123,
    MaxResults=123,
    NextToken='string'
)