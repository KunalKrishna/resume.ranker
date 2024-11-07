from pinecone import Pinecone, ServerlessSpec  # from pinecone.grpc import PineconeGRPC as Pinecone
from dotenv import load_dotenv
import os
import time
from config import PINECONESettings
from read_resumes import extract_texts_from_pdfs_in_folder
import pandas as pd

_pinecone_client = None

def get_pinecone_client():
    global _pinecone_client

    load_dotenv()
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    
    if _pinecone_client is None:
        try:
            _pinecone_client = Pinecone(api_key=PINECONE_API_KEY)
            print("Pinecone client connection successful!")
        except Exception as e:
            print(f"Error creating pinecone client: {e}. \nPlease ensure PINECONE_API_KEY is correct.")
            _pinecone_client = None  # Reset
    else:
        print("Using existing Pinecone client instance.")
    
    return _pinecone_client

def get_PID_embeddings_vector_list(PID_list, cv_embeddings_list) :
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

def generate_cv_embeddings_list(pc, raw_data_list):
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
        vectors = get_PID_embeddings_vector_list(pdf_files_list, cv_embeddings_list)
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

def upsert_cv_embeddings(pc, vectors):
    #1. create index 
    #2. use the index to upsert 
    index_name= PINECONESettings._index_name
    if index_name not in pc.list_indexes():
        pc.create_index(
            name= index_name,
            dimension= len(vectors[0]['values']),
            metric= PINECONESettings._metric,  # [cosine| dotproduct| euclidean] --read more: https://docs.pinecone.io/guides/indexes/understanding-indexes#euclidean
            spec= ServerlessSpec(
                cloud=PINECONESettings._cloud,
                region=PINECONESettings._region
            )
        )
    # Check if the index is ready
    index_description = pc.describe_index(PINECONESettings._index_name)
    is_ready = index_description["status"]["ready"]
    while not is_ready:
        time.sleep(1)

    # Get the index to upsert vectors
    index = pc.Index(index_name) 
    index.describe_index_stats()
    index.upsert(
        vectors=vectors
    )
    print(f"{len(vectors)} : vectors upsurted successfully! ")

def get_query_embedding(pc, query_str):#TODO finish
    query_text = "Your search text here"
    query_vector = []
    
    results = pc.inference.embed(
        model= PINECONESettings._model,  
        inputs= [query_str],
        parameters={
            "input_type": "passage",
            "truncate": "END"
        }
    )
    # print("dimension of ques_str vector = ",end="")
    # print(len(results.data[0]['values']))
    vector = results.data[0]['values'] 
    print(f"{query_str} : embedded.")
    return vector

def execute_query(pc, query_vector, top_k):
    # Creating an Index 

    index = pc.Index(PINECONESettings._index_name)

    # Execute Query
    results= index.query(
        vector=query_vector,
        top_k=top_k,
        include_values=False
    )
    return results

    # index_name.query(
    #     namespace="example-namespace",
    #     vector=[0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3],
    #     filter={
    #         "genre": {"$eq": "documentary"}
    #     },
    #     top_k=3,
    #     include_values=True,
    #     include_metadata=True,
    #     filter={"genre": {"$eq": "action"}}
    # )

def _test(pc, query_list, top_k):
    for query in query_list: 
        query_vector = get_query_embedding(pc, query)
        print(f"\nFinding Top {top_k} matches for {query} : ")
        final_matches= execute_query(pc, query_vector, top_k)
        for match in final_matches['matches']:
            print(match['id'])
'''
    {'matches': [{'id': 'Grace_Hopper.pdf', 'score': 0.809550643, 'values': []},
                 {'id': 'Keisha_R_Brown.pdf', 'score': 0.79268086, 'values': []}],
     'namespace': '',
     'usage': {'read_units': 5}}
'''

if __name__ == "__main__":
    pc = get_pinecone_client() # create pinecone client

    # TODO filter content - remove personal details, page number etc. 
    # cv_raw_data_list = extract_texts_from_pdfs_in_folder(PINECONESettings.cv_repo_rel_path)
    #     #[{'PID','text'},{'PID','text'},{'PID','text'}]

    # vectors = generate_cv_embeddings_list(pc, cv_raw_data_list) # Generate respective vector embeddings for each CV

    # upsert_cv_embeddings(pc, vectors) # Save embeddings in vector database

    query_list = [
        "flutter developer", 
        "java developer", 
        "social media campaigner", 
        "C# coder"]
    top_k=2
    _test(pc, query_list, top_k)