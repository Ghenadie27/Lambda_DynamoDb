import json
import boto3
import uuid
import time
from botocore.exceptions import ClientError
from datetime import datetime

# Initialize DynamoDB
dynamodb = boto3.resource('dynamodb')
table_name = "form"  # Replace with your table name
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    try:        
        # Parse the request body
        body = json.loads(event.get('body', '{}'))
        name = body.get('name')
        email = body.get('email')
        message = body.get('message')

        # Validate inputs
        if not name or not email or not message:
            return {
                "statusCode": 400,
                'headers': {"Access-Control-Allow-Origin": "*",
                },
                "body": json.dumps({"error": "Missing required fields"})
            }
                        

        # Create a unique identifier and timestamp
        item_id = str(uuid.uuid4())
        #timestamp = str(int(time.time()))
        now = datetime.now()
        timestamp = now.strftime("%H:%M:%S")

        # Save data to DynamoDB
        table.put_item(
            Item={
                'id': item_id,       # Unique identifier
                'name': name,
                'email': email,                
                'message': message,
                'timestamp': timestamp  # Unix timestamp
            }
        )

        return {
            "statusCode": 200,
            'headers': {"Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps({"message": "Data submitted successfully"})
        }
               

    except ClientError as e:
        return {
            "statusCode": 500,
            'headers': {"Access-Control-Allow-Origin": "*",
                },
            "body": json.dumps({"error": "DynamoDB Error", "details": str(e)})
        }
       
        
    except json.JSONDecodeError:
        return {
            "statusCode": 400,
            'headers': {"Access-Control-Allow-Origin": "*",
                },
            "body": json.dumps({"error": "Invalid JSON input"})
        }
        
        
    except Exception as e:
        return {
            "statusCode": 500,
            'headers': {"Access-Control-Allow-Origin": "*",
                },
            "body": json.dumps({"error": str(e)})
        }
       