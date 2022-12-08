from typing import Union
from couchbase_conn import get_rows_by_key

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/recommendations/{customer_id}")
def get_recommendations(customer_id: str, q: Union[str, None] = None):
    return get_rows_by_key(customer_id)