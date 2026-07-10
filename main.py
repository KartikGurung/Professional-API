from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

books = [
    {
        "id" : 1,
        "title" : "Digital Forensics",
        "author" : "David Bombal",
        "genre" : "Cybersecurity",
        "language" : "English"
    }
]
#Input Model for FastAPI
class BookCreate(BaseModel):
    title : str
    author : str
    genre : str
    language : str
#Response Model for GET
class BookResponse(BaseModel):
    id : int
    title : str
    author : str
    genre: str
    language: str
# Response Model for POST, PUT, PATCH, DELETE
class BookActionResponse(BaseModel):
    message : str
    book : BookResponse

@app.get('/books', response_model=list[BookResponse])
def get_books():
    return books

@app.get('/books/{book_id}', response_model=BookResponse)
def get_books_by_book_id(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book Not Found")
    
@app.post('/books', response_model=BookActionResponse)
def create_book(book: BookCreate):
    new_id = max((book["id"] for book in books), default=0) + 1
    new_book = {
        "id" : new_id,
        "title" : book.title,
        "author" : book.author,
        "genre" : book.genre,
        "language" : book.language
    }
    books.append(new_book)
    return {"message": "Book created successfully", "book": new_book}



