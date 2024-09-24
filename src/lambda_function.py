import os
import boto3
import json
import PyPDF2
import io
from pinecone import Pinecone

# Initialize AWS clients
s3 = boto3.client('s3')
bedrock = boto3.client(service_name='bedrock-runtime')

# Initialize Pinecone
pc = Pinecone(api_key=os.environ['PINECONE_API_KEY'])
index = pc.Index(os.environ['PINECONE_INDEX_NAME'])

def extract_text_from_pdf(file_object):
    pdf_reader = PyPDF2.PdfReader(file_object)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def generate_embedding(text):
    body = json.dumps({"inputText": text})
    response = bedrock.invoke_model(
        modelId="amazon.titan-embed-text-v1",
        body=body
    )
    response_body = json.loads(response.get('body').read())
    return response_body.get('embedding')

def lambda_handler(event, context):
    # Get bucket name and file key from the S3 event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    print(f"Attempting to process file: {key} from bucket: {bucket}")
    
    try:
        # Get the PDF file from S3
        response = s3.get_object(Bucket=bucket, Key=key)
        file_content = response['Body'].read()
        
        # Extract text from PDF
        pdf_file = io.BytesIO(file_content)
        extracted_text = extract_text_from_pdf(pdf_file)
        
        # Generate embedding using Amazon Bedrock
        embedding = generate_embedding(extracted_text)
        
        # Create a unique ID for the document
        doc_id = f"{bucket}_{key}"
        
        # Upsert the extracted text and embedding to Pinecone
        index.upsert(vectors=[(doc_id, embedding, {"text": extracted_text})])
        
        return {
            'statusCode': 200,
            'body': f'Successfully processed {key} and stored in Pinecone'
        }
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': f'Error processing {key}: {str(e)}'
        }