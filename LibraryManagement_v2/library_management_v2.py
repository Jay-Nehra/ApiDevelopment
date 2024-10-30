from typing import Optional, List
from fastapi import FastAPI, Path, Query, HTTPException, status
from pydantic import BaseModel, Field
from utils.logger_config import logger

logger.info("Starting Books API...")

app = FastAPI()

class Book:
    def __init__(self, id: int, title: str, author: str, description: str, 
                 rating: int, pages: int, year: int, genre: str, 
                 publisher: str, language: str, price: float, location: str):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.pages = pages
        self.year = year
        self.genre = genre
        self.publisher = publisher
        self.language = language
        self.price = price
        self.location = location

class BookCreateRequest(BaseModel):
    title: str = Field(min_length=3)
    author: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=1000)
    rating: int = Field(gt=0, lt=6)
    pages: int = Field(gt=0)
    year: int = Field(gt=0, lt=2025)
    genre: str = Field(min_length=3)
    publisher: str = Field(min_length=3)
    language: str = Field(min_length=3)
    price: float = Field(gt=0)
    location: str = Field(min_length=3)

    class Config:
        schema_extra = {
            "example": {
                "title": "Book Title",
                "author": "Book Author",
                "description": "Book Description",
                "rating": 5,
                "pages": 300,
                "year": 2000,
                "genre": "Book Genre",
                "publisher": "Book Publisher",
                "language": "Book Language",
                "price": 19.99,
                "location": "Author's Location",
            }
        }

class BookUpdateRequest(BookCreateRequest):
    id: int = Field(description="The ID of the book to update")

class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    description: str
    rating: int
    pages: int
    year: int
    genre: str
    publisher: str
    language: str
    price: float
    location: str

BOOKS = [
    Book(1, "Book 1", "Author 1", "Description 1", 4, 300, 2000, "Genre 1", "Publisher 1", "Language 1", 19.99, "Location 1"),
    Book(2, "Book 2", "Author 2", "Description 2", 3, 250, 2001, "Genre 2", "Publisher 2", "Language 2", 24.99, "Location 2"),
    # Add other books as needed
]

def generate_next_book_id() -> int:
    return 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1

@app.get("/books", response_model=List[BookResponse], status_code=status.HTTP_200_OK)
async def retrieve_all_books():
    logger.info("Retrieving all books")
    return BOOKS

@app.post("/create-book", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookCreateRequest):
    logger.info(f"Creating new book with details: {book_request}")
    new_book = Book(id=generate_next_book_id(), **book_request.dict())
    BOOKS.append(new_book)
    logger.info(f"Successfully created book with ID: {new_book.id}")
    return new_book

@app.get("/books/title/{book_title}", response_model=BookResponse, status_code=status.HTTP_200_OK)
async def find_book_by_title(book_title: str = Path(min_length=3, description="The title of the book you'd like to find")):
    logger.info(f"Finding book with title: {book_title}")
    for book in BOOKS:
        if book.title == book_title:
            logger.info(f"Found book with title: {book_title}")
            return book
    logger.error(f"Book with title: {book_title} not found")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with title: {book_title} not found")

@app.get("/books/location/{location}", response_model=List[BookResponse], status_code=status.HTTP_200_OK)
async def find_book_by_location(location: str = Path(min_length=3, description="The location of the book you'd like to find")):
    logger.info(f"Finding books with location: {location}")
    books_by_location = [book for book in BOOKS if book.location == location]
    if books_by_location:
        logger.info(f"Found {len(books_by_location)} books with location: {location}")
        return books_by_location
    logger.error(f"No books found with location: {location}")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No books found with location: {location}")

@app.get("/books/{book_id}", response_model=BookResponse, status_code=status.HTTP_200_OK)
async def find_book_by_id(book_id: int = Path(gt=0, description="The ID of the book you'd like to find")):
    logger.info(f"Finding book with ID: {book_id}")
    for book in BOOKS:
        if book.id == book_id:
            logger.info(f"Found book with ID: {book_id}")
            return book
    logger.error(f"Book with ID: {book_id} not found")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with ID: {book_id} not found")

@app.get("/books/filter", response_model=List[BookResponse], status_code=status.HTTP_200_OK)
async def find_book_by_rating(min_rating: Optional[int] = Query(None, gt=0, lt=6), max_rating: Optional[int] = Query(None, gt=0, lt=6)):
    logger.info(f"Finding books with rating parameters: min={min_rating}, max={max_rating}")
    if min_rating is None and max_rating is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="At least one of min_rating or max_rating must be provided.")
    books = [
        book for book in BOOKS
        if (min_rating is None or book.rating >= min_rating) and (max_rating is None or book.rating <= max_rating)
    ]
    logger.info(f"Found {len(books)} books matching rating criteria")
    return books

@app.put("/books/update_book", status_code=status.HTTP_200_OK)
async def update_book(book: BookUpdateRequest):
    logger.info(f"Updating book with ID: {book.id}")
    for i, existing_book in enumerate(BOOKS):
        if existing_book.id == book.id:
            BOOKS[i] = Book(**book.dict())
            logger.info(f"Successfully updated book with ID: {book.id}")
            return {"message": f"Successfully updated book with ID: {book.id}"}
    logger.error(f"Book with ID: {book.id} not found")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with ID: {book.id} not found")

@app.delete("/books/{book_id}", status_code=status.HTTP_200_OK)
async def delete_book(book_id: int = Path(gt=0, description="The ID of the book you'd like to delete")):
    logger.info(f"Deleting book with ID: {book_id}")
    for book in BOOKS:
        if book.id == book_id:
            BOOKS.remove(book)
            logger.info(f"Successfully deleted book with ID: {book_id}")
            return {"message": f"Successfully deleted book with ID: {book_id}"}
    logger.error(f"Book with ID: {book_id} not found")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with ID: {book_id} not found")
