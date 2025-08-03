import boto3
import json
import numpy as np

def stream_to_aws(data: dict, bucket: str = "qcl-data"):
    """
    Streams data to AWS S3.
    """
    s3 = boto3.client("s3")
    s3.put_object(Body=json.dumps(data), Bucket=bucket, Key=f"session_{np.random.randint(1000)}.json")
    return {"status": "uploaded"}
