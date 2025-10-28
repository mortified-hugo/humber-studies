import boto3

print("Testing AWS Comprehend connection...")

try:
    comprehend = boto3.client('comprehend', region_name='us-east-1')
    
    response = comprehend.detect_sentiment(
        Text='I love this!',
        LanguageCode='en'
    )
    
    print("✓ SUCCESS! AWS Comprehend is working!")
    print(f"Test result: {response['Sentiment']}")
    
except Exception as e:
    print("✗ FAILED!")
    print(f"Error: {e}")

print("Testing AWS Comprehend connection...")

try:
    comprehend = boto3.client('comprehend', region_name='us-east-1')
    
    response = comprehend.detect_sentiment(
        Text='I love this!',
        LanguageCode='en'
    )
    
    print("✓ SUCCESS! AWS Comprehend is working!")
    print(f"Test result: {response['Sentiment']}")
    
except Exception as e:
    print("✗ FAILED!")
    print(f"Error: {e}")

print("Testing AWS Comprehend connection...")

try:
    comprehend = boto3.client('comprehend', region_name='us-east-1')
    
    response = comprehend.detect_sentiment(
        Text='I love this!',
        LanguageCode='en'
    )
    
    print("✓ SUCCESS! AWS Comprehend is working!")
    print(f"Test result: {response['Sentiment']}")
    
except Exception as e:
    print("✗ FAILED!")
    print(f"Error: {e}")
