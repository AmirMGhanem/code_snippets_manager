from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from urllib.parse import unquote

from core import list_snippets, add_snippet, table_exists, create_table, delete_snippet, update_snippet

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/snippets")
def read_snippets(tag: str = None, language: str = None, created_by: str = None):
    filters = {}
    if tag:
        filters['tags'] = unquote(tag)
    if language:
        filters['language'] = unquote(language)
    if created_by:
        filters['created_by'] = unquote(created_by)
    return list_snippets(filters)

@app.post("/snippets")
def create_snippet(title: str, code: str, language: str, tags: str, created_by: str):
    add_snippet(unquote(title), unquote(code), unquote(language), unquote(tags), unquote(created_by))
    return {"status": "success"}

@app.put("/snippets/{snippet_id}")
def update_snippets(snippet_id: int, title: str, code: str, language: str, tags: str, created_by: str):
    res = update_snippet(snippet_id, unquote(title), unquote(code), unquote(language), unquote(tags), unquote(created_by))
    if res:
        return {"status": "success"}
    else:
        return {"status": "failed"}

@app.delete("/snippets/{snippet_id}")
def delete_snippets(snippet_id: int):
    res = delete_snippet(snippet_id)
    if res:
        return {"status": "success"}
    else:
        return {"status": "failed"}

if __name__ == '__main__':
    if table_exists('snippets'):
        print('Table exists')
    else:
        print('Table does not exist, creating now...')
        create_table()
    uvicorn.run(app, host="0.0.0.0", port=8000)