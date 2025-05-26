from weaviate.classes.init import Auth
from dotenv import load_dotenv
import weaviate
import os

load_dotenv()

# Access the variables
DB_HOST = os.getenv('DB_HOST')
DB_USERNAME = os.getenv('DB_USERNAME')
DB_API_KEY = os.getenv('DB_API_KEY')
DB_MAIN_PORT = os.getenv('DB_MAIN_PORT')
DB_GRPC_PORT = os.getenv('DB_GRPC_PORT')
DB_DOC_COLLECTION_NAME = "DocumentChunks"
PDF_LAYOUT_PARSER_PORT = os.getenv('PDF_LAYOUT_PARSER_PORT')

LLM_MODEL_NAME = os.getenv('LLM_MODEL_NAME')
LLM_API_URL = os.getenv('LLM_API_URL')
LLM_API_KEY = os.getenv('LLM_API_KEY')

# aws_access_key = os.getenv("AWS_ACCESS_KEY")
# aws_secret_key = os.getenv("AWS_SECRET_KEY")
# headers = {
#     "X-AWS-Access-Key": aws_access_key,
#     "X-AWS-Secret-Key": aws_secret_key,
# }

try:
    dbclient = weaviate.connect_to_local(
        host = DB_HOST,
        port = DB_MAIN_PORT,
        grpc_port = DB_GRPC_PORT,
        auth_credentials = Auth.api_key(api_key=DB_API_KEY),
        # headers=headers
    )
except Exception as e:
    print(e)
    print('WARNING: Could not connect to Weaviate:Connection to Weaviate failed.')

if __name__ == '__main__':
    dbclient.close()
