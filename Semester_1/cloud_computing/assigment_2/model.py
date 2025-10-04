import sagemaker
from sagemaker import image_uris

# Create a SageMaker session
sagemaker_session = sagemaker.Session()

# Set the IAM role for the SageMaker session
iam_role = sagemaker.get_execution_role()

# Define the container image for the model
image = image_uris.retrieve(framework="xgboost", region="us-east-1", version="1.5-1")

# Define the model's S3 location
model_data = 's3://hfigueiraw5sagemaker/output/assignment2-training-job/output/model.tar.gz'

# Create the SageMaker model
model = sagemaker.create_model(
    model_name='assignment2-model',
    role=iam_role,
    container_defs={
        'Image': image
    },
    vpc_config={
        'Subnets': ['hf-sub01', 'hf-sub02'],
        'SecurityGroupIds': ['sg-0f489738a3a2603c2']
    }
)

# Save the model to your SageMaker account
model.save(sagemaker_session=sagemaker_session)
