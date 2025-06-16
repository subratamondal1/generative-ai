# END TO END VECTOR SEARCH PIPELINE
import asyncio
import os
import traceback
from typing import Any, Dict, List, Optional, Tuple, cast

from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_openai import OpenAIEmbeddings
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.collection import Collection

# Constants for common filter operations
COMMON_FILTERS = {
    "supreme_court": {"bench": "Supreme Court"},
    "high_court": {"court": "High Court"},
    "recent_cases": {"date_of_judgement": {"$gte": "2020-01-01"}},
}


def embeddingmodel_init():
    """Initialize the OpenAI embedding model"""
    load_dotenv()

    OPENAI_API_KEY: str | None = os.getenv(key="OPENAI_API_KEY", default=None)

    embedding_model = OpenAIEmbeddings(
        model="text-embedding-3-large",
        dimensions=1536,  # Updated to match the index dimensions
        disallowed_special=(),
        api_key=OPENAI_API_KEY,
    )
    print(f"Embedding model: {embedding_model}")
    return embedding_model


async def mongodb_init():
    """Initialize async MongoDB client using Motor"""
    load_dotenv()

    MONGODB_CONNECTION_STRING: str | None = os.getenv(key="MONGODB_CONNECTION_STRING", default=None)

    if not MONGODB_CONNECTION_STRING:
        raise ValueError("MONGODB_CONNECTION_STRING environment variable not set")

    # Use Motor's async client instead of PyMongo
    client = AsyncIOMotorClient(
        host=MONGODB_CONNECTION_STRING,
        tls=True,
        tlsAllowInvalidCertificates=True,
    )
    print(f"MongoDB client initialized: {client}")
    return client


async def mongodb_retriever_pipeline(
    query: str = "Explain me about legal precedents",
    vector_search_index: str = "ca_foundation_index",
    db_name: str = "legal_database",
    collection_name: str = "legal_cases",
    pre_filters: Optional[Dict[str, Any]] = None,
    post_filter_pipeline: Optional[List[Dict[str, Any]]] = None,
    k: int = 10,
    score_threshold: Optional[float] = None,
    filter_template: Optional[str] = None,
) -> List[Tuple[Document, float]]:
    """
    Perform vector search using Motor async MongoDB client

    Args:
        query: The search query text
        vector_search_index: Name of the vector index in MongoDB
        db_name: MongoDB database name
        collection_name: MongoDB collection name
        pre_filters: MongoDB query to filter documents before vector search
        post_filter_pipeline: MongoDB aggregation pipeline for post-processing
        k: Number of results to return
        score_threshold: Minimum similarity score to include in results
        filter_template: Name of predefined filter template from COMMON_FILTERS
    """
    # Initialize filters
    if pre_filters is None:
        pre_filters = {}

    if filter_template and filter_template in COMMON_FILTERS:
        # Apply a predefined filter template if provided
        pre_filters.update(COMMON_FILTERS[filter_template])

    # Set up post-filtering pipeline if provided
    if post_filter_pipeline is None:
        post_filter_pipeline = []

    # Add score threshold to post-filter if specified
    if score_threshold is not None:
        post_filter_pipeline.append({"$match": {"score": {"$gte": score_threshold}}})

    # Initialize MongoDB client
    client = await mongodb_init()
    db = client[db_name]
    collection = db[collection_name]
    print(f"Using collection: {collection_name}")

    # Initialize embedding model
    embedding_model = embeddingmodel_init()

    # Create vector search object - cast Motor collection to pymongo Collection type
    vector_search = MongoDBAtlasVectorSearch(
        collection=cast(Collection, collection),
        embedding=embedding_model,
        index_name=vector_search_index,
    )

    # Explanation of filters:
    print("\nSearch configuration:")
    print(f"- Query: '{query}'")
    print(f"- Pre-filters: {pre_filters if pre_filters else 'None'}")
    print(f"- Post-filter pipeline: {post_filter_pipeline if post_filter_pipeline else 'None'}")
    print(f"- Requesting {k} results\n")

    # Perform similarity search
    # Note on filters:
    # - pre_filter: Acts like a WHERE clause in SQL - filters documents BEFORE vector search
    #   Think of it like: "Only search within these specific documents"
    # - post_filter_pipeline: MongoDB aggregation pipeline that runs AFTER vector search
    #   Think of it like: "From the results, further refine or transform them"
    results = await asyncio.to_thread(
        vector_search.similarity_search_with_score,
        query=query,
        k=k,
        pre_filter=pre_filters,
        post_filter_pipeline=post_filter_pipeline,
    )

    print(f"Found {len(results)} results for query: '{query}'")
    return results


async def process_search_results(results: List[Tuple[Document, float]]):
    """Process and display search results"""
    for i, (doc, score) in enumerate(results):
        print(f"\nResult {i + 1}: Score = {score:.4f}")
        # Access Document page_content and metadata
        print(f"Bench: {doc.metadata.get('bench', 'N/A')}")
        print(f"Court: {doc.metadata.get('court', 'N/A')}")
        print(f"Case Number: {doc.metadata.get('case_number', 'N/A')}")
        print(f"Date of Judgment: {doc.metadata.get('date_of_judgement', 'N/A')}")
        print(f"Content: {doc.page_content[:200] if doc.page_content else ''}...")


async def main():
    """Main function to run the pipeline"""
    try:
        # Example 1: Basic search without any filters
        print("\n=== Example 1: Basic Search (No Filters) ===")
        results1 = await mongodb_retriever_pipeline(
            query="constitutional rights in India",
        )
        await process_search_results(results1)

        # Example 2: Search with pre-filters
        # Pre-filters narrow down the search BEFORE looking at semantic similarity
        # Think of it like: "Only search within Supreme Court cases"
        print("\n=== Example 2: Search with Pre-Filters ===")
        results2 = await mongodb_retriever_pipeline(
            query="criminal procedure code interpretation",
            pre_filters={"bench": "Supreme Court"},
        )
        await process_search_results(results2)

        # Example 3: Search with a pre-defined filter template
        # This uses one of the pre-defined filters from COMMON_FILTERS
        print("\n=== Example 3: Search with Filter Template ===")
        results3 = await mongodb_retriever_pipeline(
            query="property rights dispute",
            filter_template="recent_cases",
        )
        await process_search_results(results3)

        # Example 4: Search with post-filters
        # Post-filters process results AFTER the vector search is done
        # This example sorts results by date and limits to 5 docs
        print("\n=== Example 4: Search with Post-Filters ===")
        results4 = await mongodb_retriever_pipeline(
            query="taxation legal precedents",
            post_filter_pipeline=[
                # Sort results by date of judgment (newest first)
                {"$sort": {"metadata.date_of_judgement": -1}},
                # Limit to 5 results after sorting
                {"$limit": 5},
            ],
            k=20,  # Request more initial results since we'll filter them
        )
        await process_search_results(results4)

        # Example 5: Combining pre-filters and post-filters with score threshold
        # This shows a more advanced search configuration
        print("\n=== Example 5: Combined Filtering Strategy ===")
        results5 = await mongodb_retriever_pipeline(
            query="human rights violations",
            pre_filters={"court": "High Court"},  # Only search High Court cases
            post_filter_pipeline=[
                # Extract year from date field for analysis
                {"$addFields": {"year": {"$substr": ["$metadata.date_of_judgement", 0, 4]}}},
                # Group by year to see trends
                {"$group": {"_id": "$year", "cases": {"$push": "$$ROOT"}, "count": {"$sum": 1}}},
                # Sort by year
                {"$sort": {"_id": 1}},
            ],
            score_threshold=0.75,  # Only consider results with at least 75% similarity
            k=50,  # Request more initial results for post-processing
        )
        # This would normally need custom processing due to the grouping
        # For demo, we'll just print the structure
        print(f"Found results grouped by year: {results5}")

    except Exception as e:
        print(f"Error in pipeline: {e}")
        traceback.print_exc()
    finally:
        # Cleanup
        pending = asyncio.all_tasks()
        for task in pending:
            if task is not asyncio.current_task():
                task.cancel()


if __name__ == "__main__":
    asyncio.run(main())
