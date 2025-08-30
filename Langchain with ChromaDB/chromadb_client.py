import chromadb

# initialize the client
client = chromadb.Client()


# create a collection to store tour verctors
collection = client.create_collection(name = "my_collection")

print(collection)