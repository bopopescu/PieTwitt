import boto.sns

c = boto.sns.connect_to_region("us-east-1")

#CHANGE
topicarn = "arn:aws:sns:us-east-1:870592896542:kitkat_SNS"

urlEndpoint = "http://160.39.130.132:9090/kitkat"

subscription = c.subscribe(topicarn, "http", urlEndpoint)

print subscription