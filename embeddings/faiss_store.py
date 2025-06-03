import faiss
import numpy as np
import os
from typing import List, Tuple

class FAISSStore:
    def __init__(self, dimension: int):
        """
        Initialize the FAISS index.
        :param dimension: The dimensionality of the vectors.
        """
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)  # L2 similarity
        self.id_map = faiss.IndexIDMap(self.index)

    def add_vectors(self, vectors: np.ndarray, ids: List[int]):
        """
        Add vectors to the FAISS index.
        :param vectors: A numpy array of shape (n, dimension).
        :param ids: A list of unique IDs associated with the vectors.
        """
        if len(ids) != len(vectors):
            raise ValueError("Number of IDs must match the number of vectors.")
        if vectors.shape[1] != self.dimension:
            raise ValueError(f"Vectors must have a dimension of {self.dimension}, but got {vectors.shape[1]}.")

        self.id_map.add_with_ids(vectors, np.array(ids, dtype=np.int64))

    def search_vectors(self, query_vector: np.ndarray, top_k: int) -> List[Tuple[int, float]]:
        """
        Search for similar vectors in the FAISS index.
        :param query_vector: A numpy array of shape (1, dimension).
        :param top_k: Number of top results to return.
        :return: A list of tuples (id, distance).
        """
        if query_vector.shape[1] != self.dimension:
            raise ValueError(f"Query vector must have a dimension of {self.dimension}, but got {query_vector.shape[1]}.")

        distances, indices = self.id_map.search(query_vector, top_k)
        return list(zip(indices[0], distances[0]))

    def save_index(self, file_path: str):
        """
        Save the FAISS index to a file.
        :param file_path: Path to save the index file.
        """
        faiss.write_index(self.id_map, file_path)

    def load_index(self, file_path: str):
        """
        Load the FAISS index from a file.
        :param file_path: Path to the index file.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Index file not found at {file_path}.")
        
        loaded_index = faiss.read_index(file_path)
        if not isinstance(loaded_index, faiss.IndexIDMap):
            raise TypeError("Loaded index is not of type IndexIDMap.")
        
        self.id_map = loaded_index


def main():
    """
    Example usage of FAISSStore.
    """
    # Initialize FAISSStore
    dimension = 128
    store = FAISSStore(dimension)

    # Create some dummy data
    vectors = np.random.random((10, dimension)).astype("float32")
    ids = list(range(10))

    # Add vectors
    print("Adding vectors to the index...")
    store.add_vectors(vectors, ids)

    # Search for similar vectors
    query_vector = np.random.random((1, dimension)).astype("float32")
    top_k = 5
    results = store.search_vectors(query_vector, top_k)
    print("Search Results (ID, Distance):", results)

    # Save and load the index
    index_file = "faiss_index.bin"
    print(f"Saving the index to {index_file}...")
    store.save_index(index_file)

    print(f"Loading the index from {index_file}...")
    store.load_index(index_file)
    print("Index loaded successfully!")


if __name__ == "__main__":
    main()
