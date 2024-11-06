from pinecone import Pinecone, ServerlessSpec  # from pinecone.grpc import PineconeGRPC as Pinecone
from dotenv import load_dotenv
from config import PINECONESettings
from read_resumes import extract_texts_from_pdfs_in_folder
import time

# creat index
def get_or_create_index(pinecone_client, index_name):
    #if not exists
    if not pinecone_client.has_index(index_name):
        # create the index
        pinecone_client.create_index(
            name=index_name,
            dimension=1024,
            metric=PINECONESettings._metric,
            spec=ServerlessSpec(
                cloud= PINECONESettings._cloud,
                region=PINECONESettings._region
            )
        )
        while not pinecone_client.describe_collection(index_name).status['ready']:
            time.sleep(1)
        print(f"index created successfully with name {index_name}")
    #if already exists
    index = pinecone_client.Index(index_name)
    return index

def describe_index(pinecone_client, index_name) :
    #pc.describe_index("example-index")
    if pinecone_client.has_index(index_name):
        print(pinecone_client.describe_index(index_name))
    else:
        print(f"supplied PINECONE client has no inded named :{index_name}")

def does_index_exist(pinecone_client, index_name):
    existing_indexe_names = [
        index_info["name"] for index_info in pinecone_client.list_indexes()
    ]
    if index_name not in existing_indexe_names:
        print(f"index {index_name} not found using pc.list_indexes()")
    
    if not pinecone_client.has_index(index_name):
        print(f"index {index_name} not found using pc.has_index()")