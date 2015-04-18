import boto.sqs

conn = boto.sqs.connect_to_region("us-east-1")

queuename = "kitkat_SQS"

q = conn.create_queue(queuename, 10)

print "getting all SQS queues:"

print conn.get_all_queues()