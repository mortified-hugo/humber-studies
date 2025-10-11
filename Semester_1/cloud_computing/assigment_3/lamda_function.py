import os
import json
import boto3
from contextlib import closing

# Environment variables configured on the Lambda function
# INPUT_BUCKET not required because the event contains the source bucket
OUTPUT_BUCKET = os.environ.get("OUTPUT_BUCKET", "my-output-bucket")
DEFAULT_SOURCE_LANG = os.environ.get("DEFAULT_SOURCE_LANG", "auto")
DEFAULT_TARGET_LANG = os.environ.get("DEFAULT_TARGET_LANG", "fr")

s3 = boto3.client("s3")
translate = boto3.client("translate")


def lambda_handler(event, context):
    # Expecting S3 Put event(s)
    records = event.get("Records", [])
    results = []

    for rec in records:
        s3_info = rec.get("s3", {})
        src_bucket = s3_info.get("bucket", {}).get("name")
        src_key = s3_info.get("object", {}).get("key")
        if not src_bucket or not src_key:
            results.append({"key": src_key, "status": "skipped", "reason": "missing bucket/key"})
            continue

        # Download and read the S3 object using a with-statement
        response = s3.get_object(Bucket=src_bucket, Key=src_key)
        with closing(response["Body"]) as stream:
            raw_bytes = stream.read()
        try:
            text = raw_bytes.decode("utf-8")
        except UnicodeDecodeError:
            # If file is binary or different encoding, fall back to latin-1 then replace
            text = raw_bytes.decode("latin-1", errors="replace")

        # Call Amazon Translate
        source_lang = rec.get("translationSourceLang", DEFAULT_SOURCE_LANG)
        target_lang = rec.get("translationTargetLang", DEFAULT_TARGET_LANG)
        translate_resp = translate.translate_text(
            Text=text,
            SourceLanguageCode=source_lang,
            TargetLanguageCode=target_lang
        )
        translated_text = translate_resp["TranslatedText"]

        # Prepare output key (same name but with _translated and .txt)
        base_name = src_key.rsplit("/", 1)[-1]
        if "." in base_name:
            name_only = ".".join(base_name.split(".")[:-1])
        else:
            name_only = base_name
        out_key = f"translated/{name_only}_{target_lang}.txt"

        # Write the translated text to the output S3 bucket
        s3.put_object(
            Bucket=OUTPUT_BUCKET,
            Key=out_key,
            Body=translated_text.encode("utf-8"),
            ContentType="text/plain; charset=utf-8"
        )

        results.append({"key": src_key, "output_key": out_key, "status": "ok"})

    return {
        "statusCode": 200,
        "body": json.dumps(results)
    }