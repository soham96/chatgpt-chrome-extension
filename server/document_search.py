from fastapi import APIRouter
from pydantic import BaseModel

from langchain.indexes import VectorstoreIndexCreator
from langchain.document_loaders import UnstructuredURLLoader

router=APIRouter()

class Summarize(BaseModel):
    text: str


def url_loader(url):
    from langchain.document_loaders import UnstructuredURLLoader
    loader = UnstructuredURLLoader(urls=[url])
    data = loader.load()

    index = VectorstoreIndexCreator().from_loaders([loader])

@router.post("/ask")
def summarize_document(data: dict = Body()):
    loader = UnstructuredURLLoader(urls=data.urls)
    text=loader.laod()
    index = VectorstoreIndexCreator().from_texts([text])
    result=index.query(data.query)
    print(result)

