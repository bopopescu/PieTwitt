import boto.sns

c = boto.sns.connect_to_region("us-east-1")

topicname = "kitkat_SNS"

topicarn = c.create_topic(topicname)

print topicname, "has been successfully created with a topic ARN of", topicarn