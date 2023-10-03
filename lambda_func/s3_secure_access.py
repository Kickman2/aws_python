import boto3
import re

def lambda_handler(event, context):
    # Extract unique_id and password from the event
    unique_id = event['unique_id']
    provided_password = event['password']
    
    # Initialize S3 client
    s3 = boto3.client('s3')
    
    # List objects in the S3 bucket
    try:
        response = s3.list_objects_v2(Bucket='your-bucket-name')
    except Exception as e:
        return {
            'statusCode': 500,
            'body': 'Error listing objects in S3'
        }
    
    # Iterate through objects to find the matching file
    found_object = None
    for obj in response.get('Contents', []):
        filename = obj['Key']
        if validate_filename_format(filename, unique_id):
            if is_password_correct(filename, provided_password):
                found_object = filename
                break
    
    if found_object is None:
        return {
            'statusCode': 404,
            'body': 'File not found'
        }
    
    # Generate a presigned URL for downloading the file
    presigned_url = s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': 'your-bucket-name', 'Key': found_object},
        ExpiresIn=3600  # URL expiration time in seconds (adjust as needed)
    )
    
    # Rename the file (remove the password from the filename)
    new_filename = remove_password_from_filename(found_object)
    s3.copy_object(
        CopySource={'Bucket': 'your-bucket-name', 'Key': found_object},
        Bucket='your-bucket-name',
        Key=new_filename
    )
    
    # Delete the old file
    s3.delete_object(Bucket='your-bucket-name', Key=found_object)
    
    return {
        'statusCode': 200,
        'body': presigned_url
    }

def validate_filename_format(filename, unique_id):
    # Define a regex pattern for the filename format
    pattern = re.compile(f'^{unique_id}_[a-zA-Z0-9]+\.[a-zA-Z0-9]+$')
    return bool(pattern.match(filename))

def is_password_correct(filename, provided_password):
    # Extract the password part from the filename
    extracted_password = filename.split('_')[1].split('.')[0]
    return extracted_password == provided_password

def remove_password_from_filename(filename):
    # Remove the password part from the filename
    parts = filename.split('_')
    return '_'.join(parts[:-1]) + '.' + parts[-1]
