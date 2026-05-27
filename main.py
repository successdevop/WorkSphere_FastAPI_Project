from fastapi import FastAPI, Header
from typing import Optional, List, Any
from pydantic import BaseModel

from data import data

app = FastAPI()

# @app.get("/")
# async def home():
#     return {"response":"Hello Fast API"}
#
# @app.get("/greet/")
# async def greet(name: Optional[str] = "User", age: int = 0) -> dict:
#     return {"response":f"Hello {name}", "age": age}
#
# class BookCreateModel(BaseModel):
#     title: str
#     author: str
# #
# @app.post("/create_book")
# async def create_book(book_data: BookCreateModel):
#     return {
#         "title": book_data.title,
#         "author": book_data.author
#     }
#
# @app.get("/get_headers")
# async def get_headers(accept: str = Header(None), content_type: str = Header(None),
#                       user_agent: str = Header(None), host: str = Header(None)):
#     req_headers = {}
#     req_headers['Accept'] = accept
#     req_headers["Content-Type"] = content_type
#     req_headers["User-Agent"] = user_agent
#     req_headers["Host"] = host
#     return req_headers

class BookModel(BaseModel):
    id: int
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str


@app.get("/books", response_model=List[BookModel])
async def get_all_books() -> dict:
    return data

@app.get("/books/{book_id}")
async def get_a_book(book_id: int) -> Optional[dict]:
    book = next((bk for bk in data if bk["id"] == book_id), None)
    if book is None:
        return {"error":"book not found"}
    return book

@app.patch("/book/{book_id}")
async def update_book(book_id: int, book_data: BookModel) -> dict:
    book = next((bk for bk in data if bk["id"] == book_id))
    if not book:
        return {"error":"book not found"}

    if "title" in book_data:
        book_data.title = book["title"]
    if "author" in book:
        book["author"] = book["author"]
    if "publisher" in book:
        book["publisher"] = book["publisher"]
    if "published_date" in book:
        book["published_date"] = book["published_date"]
    if "page_count" in book:
        book["page_count"] = book["page_count"]
    if "language" in book:
        book["language"] = book["language"]

    return book

@app.put("/book/{book_id}")
async def update_book_put(book_id: int, book_data: BookModel) -> dict:
    book = next((bk for bk in data if bk["id"] == book_id))
    if not book:
        return {"error":"book not found"}

    book = {"id": book_id,
            "author": book_data.author,
            "publisher": book_data.publisher,
            "published_date": book_data.published_date,
            "page_count": book_data.page_count,
            "language": book_data.language
            }
    return book

@app.delete("/books/{book_id}")
async def update_book_put(book_id: int) -> dict:
    book = next((bk for bk in data if bk["id"] == book_id), None)
    if not book:
        return {"error":"book not found"}
    return data.pop(book_id)

@app.post("/books")
async def add_book(book_data: BookModel):
    book = {"id": book_data.id,
            "author": book_data.author,
            "title": book_data.title,
            "publisher": book_data.publisher,
            "published_date": book_data.published_date,
            "page_count": book_data.page_count,
            "language": book_data.language
            }
    if any(bk["id"] == book["id"] for bk in data):
        return {"error": "book id already exist. Assign another ID"}
    data.append(book)
    return book