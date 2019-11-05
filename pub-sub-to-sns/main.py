import base64
import boto3


def handler(event, context):
    """Background Cloud Function to be triggered by Pub/Sub.
    Args:
         event (dict):  The dictionary with data specific to this type of
         event. The `data` field contains the PubsubMessage message. The
         `attributes` field will contain custom attributes if there are any.
         context (google.cloud.functions.Context): The Cloud Functions event
         metadata. The `event_id` field contains the Pub/Sub message ID. The
         `timestamp` field contains the publish time.
    """

    print("""This Function was triggered by messageId {} published at {}
    """.format(context.event_id, context.timestamp))

    if event.get('attributes') and \
            event['attributes'].get("origin", "") == "sns":
        print("Origin of message was SNS. Exiting.")
        return 

    message = base64.b64decode(event['data']).decode('utf-8')
    print("Publishing message to SNS: {}".format(message))
    sns = boto3.client('sns')
    region = "us-east-2"
    account = "292244388449"
    topic_name = "multi-cloud-messaging"
    attrs = {"origin": {'DataType': 'String', 'StringValue': "pubsub"}}
    topic = 'arn:aws:sns:{}:{}:{}'.format(region, account, topic_name)
    sns.publish(TopicArn=topic, Message=message,
                    MessageAttributes=attrs)
