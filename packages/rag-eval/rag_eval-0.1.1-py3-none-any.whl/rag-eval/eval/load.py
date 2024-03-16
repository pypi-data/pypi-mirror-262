from qdrant_client import QdrantClient
from dotenv import load_dotenv
load_dotenv()
import os
import json
from random import sample
from pydantic import BaseModel

qdrant_client = QdrantClient(url = os.getenv("QDRANT_URL"), api_key=os.getenv("QDRANT_API"))

results = qdrant_client.scroll(collection_name = "RAG_chunks", limit = 15000)



results_final = []
for idx,val in enumerate(results):
    try:
        text = json.loads(val.model_dump()['payload']['_node_content'])['text']
        id = val.id
    except:
        pass
    else:
        new_dict= {"chunk_id": id, "text": text}
        results_final.append(new_dict)

results_sample = sample(results_final, 500)


print(results_sample[0])

