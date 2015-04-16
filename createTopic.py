import boto.sns

c = boto.sns.connect_to_region("us-west-2")

topicname = "kitkatTopic2"

topicarn = c.create_topic(topicname)

print topicname, "has been successfully created with a topic ARN of", topicarn