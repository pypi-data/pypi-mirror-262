from qdrant_client import QdrantClient
from dotenv import load_dotenv
from datasets import Dataset

load_dotenv()
import os
import json
from random import sample
from pydantic import BaseModel


def set_client(base_url=os.getenv("QDRANT_URL"), api=os.getenv("QDRANT_API")):
    qdrant_client = QdrantClient(url=base_url, api_key=api)
    return qdrant_client


def retrieve_sample(client, collection: str, vector_limit=500, sample_n=100):
    results = client.scroll(collection_name=collection, limit=vector_limit)

    results_final = []
    for idx, val in enumerate(results[0]):
        try:
            text = json.loads(val.model_dump()["payload"]["_node_content"])[
                "text"
            ]
            id = val.id
        except:
            raise ValueError
        else:
            new_dict = {"chunk_id": id, "text": text}
            results_final.append(new_dict)

    # results_sample = sample(results_final, sample_n)
    return Dataset.from_list(results_final)
