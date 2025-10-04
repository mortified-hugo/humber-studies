import json


with open("event.json") as file:
    event = json.load(file)


def lambda_handler(event, context):
    bucket_name = event['Records'][0]['s3']["bucket"]["name"]
    object_key = event['Records'][0]['s3']['object']['key']
    print(f"My bucket: {bucket_name} now has\n"
          f"this {object_key} in it")


lambda_handler(event, None)
