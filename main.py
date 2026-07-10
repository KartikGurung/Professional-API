from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import  Optional

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
    raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail="Book Not Found")
    

@app.post('/books', response_model=BookActionResponse, status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreate):
    for existing_book in books:
        if existing_book["title"].lower() == book.title.lower():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Title with this book already exists")
        

    new_id = max((book["id"] for book in books), default=0) + 1
    new_book = {
        "id" : new_id,
        "title" : book.title,
        "author" : book.author,
        "genre" : book.genre,
        "language" : book.language,
        "internal_note" : "Added by admin",
        "created_by" : "Kartik"
    }
    books.append(new_book)
    return {"message": "Book created successfully", "book": new_book}



@app.put('/books/{book_id}', response_model=BookActionResponse, status_code=status.HTTP_201_CREATED)
def update_book(book_id: int, book: BookCreate):
    for exsisting_book in books:
        if exsisting_book["id"] == book_id:
            exsisting_book.update(book.model_dump())
        return {
            "message" : "book uodated sucessfully",
            "book" : exsisting_book
        }

# Input Model for Patch
class BookPatch(BaseModel):
    title : Optional[str] = None
    author : Optional[str] = None
    genre : Optional[str] = None
    language : Optional[str] = None

@app.patch('/books/{book_id}', response_model=BookActionResponse, status_code=status.HTTP_201_CREATED)
def book_patch(book_id: int, book: BookPatch):
    for existing_book in books:
        if existing_book["id"] == book_id:
            if book.author is not None:
                existing_book["author"] = book.author
            if book.title is not None:
                existing_book["title"] = book.title
            if book.genre is not None:
                existing_book["genre"] = book.genre
            if book.language is not None:
                existing_book["language"] = book.language
            return {
                "message" : "Book Patched Sucessfully",
                "book" : existing_book
            }
    raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Not Found")

@app.delete('/book/{book_id}', response_model=BookActionResponse, status_code=status.HTTP_200_OK)
def book_delete(book_id: int):
    for existing_book in books:
        if existing_book["id"] == book_id:
            existing_book.remove(existing_book)
        return {
            "message" : "Book Deleted Sucessfully"
        }
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")


