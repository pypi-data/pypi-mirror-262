from langchain_text_splitters import NLTKTextSplitter

from komodo.framework.komodo_vector import MetaData, Vector
from komodo.shared.documents.text_extract import to_clean_text, extract_text_from_path
from komodo.shared.embeddings.openai import get_embeddings


class VectorStoreHelper:

    def __init__(self, path):
        self.path = path
        self.text = self.extract_text()
        if self.text and len(self.text) > 0:
            self.chunks = self.split_into_chunks()
            self.data = self.create_vectors()
            self.update_vector_embeddings(batch_size=100)

    def extract_text(self):
        return extract_text_from_path(self.path)

    def split_into_chunks(self, chunk_size=1200, chunk_overlap=100, pages=20):
        text_splitter = NLTKTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        chunks = text_splitter.split_text(self.text)
        print("Split text into {} chunks of size: {}".format(len(chunks), chunk_size))
        return chunks

    def create_vectors(self):
        data = []
        for i, chunk in enumerate(self.chunks):
            content = to_clean_text(chunk)
            metadata = MetaData(self.path, i, content)
            vector = Vector(content, metadata, None)
            data.append(vector)
        return data

    def update_vector_embeddings(self, batch_size):
        embeddings_model = get_embeddings()
        for i in range(0, len(self.data), batch_size):
            batch = self.data[i:i + batch_size]
            contents = [item.content for item in batch]
            embeddings = embeddings_model.embed_documents(contents)
            for j, item in enumerate(batch):
                item.embedding = embeddings[j]
        return self.data


if __name__ == '__main__':
    helper = VectorStoreHelper(__file__)
    print(helper.path)
    print(helper.text)
    print(helper.chunks)
    print(helper.data)
