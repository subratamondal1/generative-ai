import os
import pprint
import time

from dotenv import load_dotenv
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_openai import OpenAIEmbeddings
from pymongo import MongoClient
from pymongo.operations import SearchIndexModel

# Load environment variables
load_dotenv()

# Load API keys and connection strings
OPENAI_API_KEY: str | None = os.getenv(key="OPENAI_API_KEY", default=None)
MONGODB_CONNECTION_STRING: str | None = os.getenv(
    key="MONGODB_CONNECTION_STRING", default=None
)

# Initialize MongoDB client
client: MongoClient = MongoClient(
    host=MONGODB_CONNECTION_STRING, tls=True, tlsAllowInvalidCertificates=True
)

db_name: str = "embeddings"
collection_name: str = "text"

coll = client[db_name][collection_name]
vector_search_index = "vector_index"

# Clear existing documents
coll.delete_many(filter={})

# Sample texts
texts: list[str] = [
    "A martial artist agrees to spy on a reclusive crime lord using his invitation to a tournament there as cover.",
    "A group of intergalactic criminals are forced to work together to stop a fanatical warrior from taking control of the universe.",
    "When a boy wishes to be big at a magic wish machine, he wakes up the next morning and finds himself in an adult body.",
]

# Initialize embedding model
embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large",
    dimensions=768,
    disallowed_special=(),
)

# Generate embeddings
embeddings = embedding_model.embed_documents(texts=texts)

docs = []
for i in range(len(texts)):
    docs.append(
        {
            "text": texts[i],
            "embedding": embeddings[i],
        }
    )

try:
    coll.insert_many(documents=docs)
    print("Documents inserted successfully")
except Exception as e:
    print(f"An error occurred during insertion: {e}")

print("Documents embedded and inserted successfully")

time.sleep(10)  # Allow time for indexing

# Semantic queries
semantic_queries: list[str] = [
    "Secret Agent captures underworld boss.",
    "Awkward team of space defenders.",
    "A magical tale of growing up.",
]

# Check if vector search index already exists
existing_indexes = list(coll.list_search_indexes())
index_exists = any(index["name"] == vector_search_index for index in existing_indexes)

if not index_exists:
    # Define search index model
    search_index_model = SearchIndexModel(
        definition={
            "fields": [
                {
                    "type": "vector",
                    "path": "embedding",
                    "similarity": "dotProduct",
                    "numDimensions": 768,  # Corrected dimension to match embedding model
                }
            ]
        },
        name=vector_search_index,
        type="vectorSearch",
    )
    coll.create_search_index(model=search_index_model)
    print("Vector search index created successfully.")
else:
    print("Vector search index already exists.")

# Initialize vector search
vector_search = MongoDBAtlasVectorSearch(
    collection=coll,
    embedding=embedding_model,
    index_name=vector_search_index,
)

# Perform semantic search
for query in semantic_queries:
    result = vector_search.similarity_search_with_score(
        query=query,
        k=3,
    )
    print("SEMANTIC QUERY:", query)
    print("RANKED RESULTS:")
    pprint.pprint(result)
    print("\n")
