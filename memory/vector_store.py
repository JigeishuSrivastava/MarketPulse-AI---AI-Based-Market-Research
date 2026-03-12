import chromadb

client = chromadb.Client()

collection = client.get_or_create_collection("market_research")

def store_data(text):

    collection.add(
        documents=[text],
        ids=[str(hash(text))]
    )

def retrieve_data(query):

    results = collection.query(
        query_texts=[query],
        n_results=5
    )

    return results["documents"]