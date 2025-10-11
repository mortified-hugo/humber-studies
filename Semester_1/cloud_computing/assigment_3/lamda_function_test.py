import json
import boto3
from contextlib import closing

s3 = boto3.client("s3")
translate = boto3.client("translate")
output_bucket = "hfigueira-assing3-output"
file_name = "translated_text.txt"


def lambda_handler(event, context):
    record = event.get("Records", [])[0]
    src_bucket = record["s3"]["bucket"]["name"]
    src_key = record["s3"]["object"]["key"]
    print(f"bucket: {src_bucket}", f"key:{src_key}")

    response = s3.get_object(Bucket=src_bucket, Key=src_key)

    with closing(response["Body"]) as stream:
        raw_bytes = stream.read()

    text = raw_bytes.decode("utf-8")
    translate_response = translate.translate_text(
        Text=text,
        SourceLanguageCode='en',
        TargetLanguageCode='pt'
    )

    translated_content = translate_response['TranslatedText']

    final_response = s3.put_object(
        Body=translated_content.encode("utf-8"),
        Bucket=output_bucket,
        Key=file_name,
        ContentType="text/plain; charset=utf-8"
    )
    print(final_response)
