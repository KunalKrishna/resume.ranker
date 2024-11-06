
class PINECONESettings:
    _model = "multilingual-e5-large"
    
    _cloud = "aws"
    _region= "us-east-1"
    _metric= "cosine"   # [cosine|dotproduct|euclidean] --read more: https://docs.pinecone.io/guides/indexes/understanding-indexes
    
    _index_name= "cv-index2" #required for saving & querying in vector db 

    cv_repo_rel_path="resume.ranker/CV"
