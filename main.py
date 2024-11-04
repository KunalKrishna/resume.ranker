from pinecone import Pinecone, ServerlessSpec  # from pinecone.grpc import PineconeGRPC as Pinecone
from dotenv import load_dotenv
import os
import time
from config import PINECONESettings
from read_resumes import extract_texts_from_pdfs_in_folder
from string import ascii_uppercase
import pandas as pd

load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

_pinecone_client = None

def get_pinecone_client():
    global _pinecone_client
    if _pinecone_client is None:
        try:
            _pinecone_client = Pinecone(api_key=PINECONE_API_KEY)
            print("Pinecone client connection successful!")
        except Exception as e:
            print(f"Error creating pinecone client: {e}. \nPlease ensure PINECONE_API_KEY is correct.")
            _pinecone_client = None  # Reset if there was an error
    else:
        print("Using existing Pinecone client instance.")
    
    return _pinecone_client

def get_PID_embeddings_binding_list(PID_list, cv_embeddings_list) :
    """
    Create a list of dictionaries with 'id' and 'values' keys, pairing each entry in PID_list with its
    corresponding embedding from cv_embeddings_list.

    Parameters:
        PID_list (list): A list of IDs, each representing a PID.
        cv_embeddings_list (list): A list of embedding vectors, where each corresponds to an entry in PID_list.

    Returns:
        list: A list of dictionaries in the format {"id": pid, "values": cv_embedding}.
    """
    #TODO supply list of PIDs instead of list of pdf file names
    n = min(len(PID_list), len(cv_embeddings_list))
    vectors = [{"id": PID_list[i], "values": cv_embeddings_list[i]} for i in range(n)]
    return vectors

def generate_embedding_values_list(raw_data_list, pc):
    """
    Generates embeddings for the provided raw data and returns the values_list.

    Parameters:
        raw_data_list (list of str): List of text data to embed.
        pc : A connected pinecone client 

    Returns:
        list: Embedding values for the first item in raw_data_list.
    """
    
    # Generate embeddings
    extracted_text_list = [list(item.values())[0] for item in raw_data_list]
    try:
        results = pc.inference.embed(
            model=PINECONESettings._model,
            inputs=extracted_text_list,
            parameters={
                "input_type": "passage",
                "truncate": "END"
            }
        )
        '''
        EmbeddingsList(
            model='multilingual-e5-large',
            data=[
                {'values': [0.0191802978515625, -0.01113128662109375, ..., -0.0281219482421875, -0.00665283203125]},
                {'values': [-0.0029850006103515625, -0.02435302734375, ..., -0.041961669921875, 0.0129547119140625]},
                {'values': [0.0211334228515625, -0.00498199462890625, ..., -0.007110595703125, -0.007579803466796875]},
                {'values': [-0.007659912109375, -0.00839996337890625, ..., 0.00801849365234375, 0.0037326812744140625]},
                {'values': [0.0029144287109375, -0.01200103759765625, ..., -0.0309295654296875, 0.02239990234375]}
            ],
            usage={'total_tokens': 2560}
        )
        '''

        pdf_files_list = [list(item.keys())[0] for item in raw_data_list]
        cv_embeddings_list = [entry['values'] for entry in results.data]
        vectors = get_PID_embeddings_binding_list(pdf_files_list, cv_embeddings_list)
        '''
            vectors=[
                {"id": "A", "values": [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]},
                {"id": "D", "values": [0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4]}
            ]
        '''

        return vectors 
    except Exception as e:
        print(f"Error generating embeddings: {e}")
        return None

def upsert_embeddings(vectors, pc):
    #1. create index 
    #2. use the index to upsert 
    index_name= PINECONESettings._index_name
    if index_name not in pc.list_indexes():
        pc.create_index(
            name= index_name,
            dimension= len(cv_raw_data_list[0]),
            metric= PINECONESettings._metric,  # [cosine| dotproduct| euclidean] --read more: https://docs.pinecone.io/guides/indexes/understanding-indexes#euclidean
            spec= ServerlessSpec(
                cloud=PINECONESettings._cloud,
                region=PINECONESettings._region
            )
        )

    while not pc.describe_collection(index_name).status['ready']:
        time.sleep(1)

    # Get the index to upsert vectors
    index = pc.Index(index_name) 
    index.describe_index_stats()
    index.upsert(
        vectors=vectors
    )
    print(index)

if __name__ == "__main__":
    cv_dir = ""

    # list of text/content of each resume 
    # TODO fileter content - remove personal details, page number etc. 
    cv_raw_data_list = extract_texts_from_pdfs_in_folder(PINECONESettings.cv_repo_rel_path) #[{'PID','text'},{'PID','text'},{'PID','text'}]

    # create pinecone client
    pc = get_pinecone_client()

    # generate respective vector embeddings for each CV
    vectors = generate_embedding_values_list(cv_raw_data_list, pc)

    # save embeddings in vector database
    upsert_embeddings(vectors, pc)