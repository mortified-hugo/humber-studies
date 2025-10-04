import boto3

# Create a SageMaker client
sagemaker = boto3.client('sagemaker', region_name='us-east-1')

# Set the name of the training job and the S3 location of the training data
job_name = 'mk5-training-job'
input_data_path = 's3://hfigueiraw5sagemaker/input/training_data.csv'

# Set the name and location of the output model artifacts
output_path = 's3://hfigueiraw5sagemaker/output/'

# Set the IAM role that will be used for the training job
iam_role = 'arn:aws:iam::330086343754:role/LabRole'

# Create the training job
response = sagemaker.create_training_job(
    TrainingJobName=job_name,
    AlgorithmSpecification={
        'TrainingImage': '246618743249.dkr.ecr.us-west-2.amazonaws.com/sagemaker-xgboost:1.5-1',
        'TrainingInputMode': 'File',
        #'AlgorithmName': 'XGBoost'
    },
      HyperParameters={
        'max_depth': '5',
        'eta': '0.2',
        'gamma': '4',
        'min_child_weight': '6',
        'subsample': '0.7',
        #'objective': 'binary:logistic',
        'num_round': '10'
        
    },
    RoleArn=iam_role,
    InputDataConfig=[
        {
            'ChannelName': 'train',
            'DataSource': {
                'S3DataSource': {
                    'S3DataType': 'S3Prefix',
                    'S3Uri': input_data_path
                }
            },
            'ContentType': 'text/csv',
            'CompressionType': 'None'
        }
    ],
    OutputDataConfig={
        'S3OutputPath': output_path
    },
    ResourceConfig={
        'InstanceType': 'ml.m4.xlarge',
        'InstanceCount': 1,
        'VolumeSizeInGB': 50
    },
    StoppingCondition={
        'MaxRuntimeInSeconds': 86400
    }
)
print(response)
