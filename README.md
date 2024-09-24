# S3 PDF to Pinecone Lambda Function

This Lambda function processes PDF files uploaded to an S3 bucket, extracts the text content, generates embeddings using Amazon Bedrock, and stores the results in a Pinecone index.

## Features

- Automatically triggered by S3 file uploads
- Extracts text from PDF files
- Generates embeddings using Amazon Bedrock's Titan model
- Stores document text and embeddings in Pinecone for efficient similarity search

## Prerequisites

- AWS account with access to Lambda, S3, and Bedrock
- Pinecone account and API key
- Python 3.8 or later

## Setup

1. Clone this repository
2. Create a new Lambda function in AWS
3. Set up the following environment variables in your Lambda function:
   - `PINECONE_API_KEY`: Your Pinecone API key
   - `PINECONE_INDEX_NAME`: The name of your Pinecone index
4. Set up an S3 trigger for your Lambda function
5. Ensure your Lambda function has the necessary IAM permissions for S3, Bedrock, and CloudWatch Logs
6. Deploy the `lambda_function.py` code to your Lambda function

## Usage

Simply upload a PDF file to the configured S3 bucket. The Lambda function will automatically process the file and store the results in Pinecone.

## Testing

Run the `test_lambda_function.py` script to perform a basic test of the Lambda function:


## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.