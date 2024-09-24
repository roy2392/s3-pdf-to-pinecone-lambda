import json
from lambda_function import lambda_handler

def test_lambda_handler():
    # Create a mock S3 event
    event = {
        "Records": {
            "s3": {
                "bucket": {"name": "your-test-bucket"},
                "object": {"key": "test.pdf"}
            }
        }
    }

    # Call the lambda_handler function
    result = lambda_handler(event, None)

    # Assert the result
    assert result['statusCode'] == 200
    assert "Successfully processed" in result['body']

if __name__ == "__main__":
    test_lambda_handler()
    print("Test passed successfully!")