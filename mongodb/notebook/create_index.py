# Create MongoDB Vector Search Index
# Required packages: pymongo, motor
import asyncio

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection, AsyncIOMotorDatabase
from pymongo.operations import SearchIndexModel


async def create_vector_search_index():
    # MongoDB connection details
    connection_string = "mongodb://localhost:27017"
    database_name = "ca_foundation"
    collection_name = "documents"

    # Connect to MongoDB with Motor
    client: AsyncIOMotorClient = AsyncIOMotorClient(connection_string)
    db: AsyncIOMotorDatabase = client[database_name]
    collection: AsyncIOMotorCollection = db[collection_name]

    vector_search_index = "ca_foundation_index"
    # Define search index model
    search_index_model: SearchIndexModel = SearchIndexModel(
        definition={
            "fields": [
                {
                    "type": "vector",
                    "path": "embedding",
                    "similarity": "cosine",
                    "numDimensions": 1536,
                },
                {
                    "type": "filter",
                    "path": "bench",
                },
                {
                    "type": "filter",
                    "path": "date_of_judgement",
                },
                {
                    "type": "filter",
                    "path": "court",
                },
                {
                    "type": "filter",
                    "path": "case_number",
                },
            ]
        },
        name=vector_search_index,
        type="vectorSearch",
    )

    # Create the search index
    await collection.create_search_index(model=search_index_model)
    print("Vector search index created successfully.")

    # Close the MongoDB connection
    client.close()


async def main():
    try:
        await create_vector_search_index()
    except Exception as e:
        print(f"Error creating vector search index: {e}")


if __name__ == "__main__":
    asyncio.run(main())
