import json
import os

from google.cloud import pubsub_v1


def lambda_handler(event, context):
    project_id = os.environ['PROJECT_ID']
    topic_name = os.environ['TOPIC_NAME']
    origin = event['Records'][0]['Sns'].get("MessageAttributes", {})\
                                .get("origin", {}).get("Value", "")
    if origin == "pubsub":
        return ("Origin is pub/sub. Exit.")

    message = event['Records'][0]['Sns']['Message']
    print("From SNS to pub/sub: " + message)
    publish_message(project_id, topic_name, message)
    return message


def publish_message(project_id, topic_name, message):
    """Publishes multiple messages to a Pub/Sub topic."""
    # Location of the service account key that should be bundled with your
    # function.
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "gcp-key.json"
    publisher = pubsub_v1.PublisherClient()
    # The `topic_path` method creates a fully qualified identifier
    # in the form `projects/{project_id}/topics/{topic_name}`
    topic_path = publisher.topic_path(project_id, topic_name)
    # When you publish a message, the client returns a future.
    future = publisher.publish(topic_path, data=message.encode("utf-8"),
            origin='sns')
    print(future.result())
