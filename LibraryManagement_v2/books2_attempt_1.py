from typing import Optional
from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from utils.logger_config import logger
from starlette import status

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

class BookRequest(BaseModel):
    id: Optional[int] = Field(description='ID is not needed to create a Book Entry...', default= None) 
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

    model_config = {
        "json_schema_extra": {
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
    }


BOOKS = [
    Book(1, "Book 1", "Author 1", "Description 1", 4, 300, 2000, "Genre 1", "Publisher 1", "Language 1", 19.99, "Location 1"),
    Book(2, "Book 2", "Author 2", "Description 2", 3, 250, 2001, "Genre 2", "Publisher 2", "Language 2", 24.99, "Location 2"),
    Book(3, "Book 3", "Author 3", "Description 3", 5, 400, 2002, "Genre 3", "Publisher 3", "Language 3", 29.99, "Location 3"),
    Book(4, "Book 4", "Author 4", "Description 4", 2, 200, 2003, "Genre 4", "Publisher 4", "Language 4", 14.99, "Location 4"),
    Book(5, "Book 5", "Author 5", "Description 5", 1, 150, 2004, "Genre 5", "Publisher 5", "Language 5", 9.99, "Location 5"),
    Book(6, "Book 6", "Author 6", "Description 6", 4, 350, 2005, "Genre 6", "Publisher 6", "Language 6", 29.99, "Location 6"),
    Book(7, "Book 7", "Author 7", "Description 7", 3, 220, 2006, "Genre 7", "Publisher 7", "Language 7", 24.99, "Location 7"),
    Book(8, "Book 8", "Author 8", "Description 8", 5, 450, 2007, "Genre 8", "Publisher 8", "Language 8", 39.99, "Location 8"),
    Book(9, "Book 9", "Author 9", "Description 9", 2, 210, 2008, "Genre 9", "Publisher 9", "Language 9", 19.99, "Location 9"),
    Book(10, "Book 10", "Author 10", "Description 10", 1, 160, 2009, "Genre 10", "Publisher 10", "Language 10", 14.99, "Location 10"),]

# Use this function to find the next available ID for a new book.
def generate_next_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book

@app.get("/books", status_code=status.HTTP_200_OK)
async def retrieve_all_books():
    logger.info("Retrieving all books")
    return BOOKS

@app.post("/create-book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request : BookRequest):
    logger.info(f"Creating new book with details: {book_request}")
    # Convert the BookRequest object to a Book object so that the BOOKS list contains all the Book Objects and not the BookRequest objects.
    new_book = Book(**book_request.model_dump())
    BOOKS.append(generate_next_book_id(new_book))
    logger.info(f"Successfully created book with ID: {new_book.id}")
    return f"Successfully created book with ID: {new_book.id}"

@app.get("/books/title/{book_title}", status_code=status.HTTP_200_OK)
async def find_book_by_title(book_title: str = Path(min_length=3, description="The title of the book you'd like to find")):
    logger.info(f"Finding book with title: {book_title}")
    for book in BOOKS:
        if book.title == book_title:
            logger.info(f"Found book with title: {book_title}")
            return book
    logger.info(f"Book with title: {book_title} not found")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with title `{book_title}` not found")


@app.get("/books/location/{location}", status_code=status.HTTP_200_OK)
async def find_book_by_location(location: str = Path(min_length=3, description="The location of the book you'd like to find")):
    logger.info(f"Finding the books with loction: {location}")
    books_by_location = [book for book in BOOKS if book.location == location]
    if books_by_location:
        logger.info(f"Found {len(books_by_location)} books with location: {location}")
        return books_by_location
    logger.info(f"No books found with location: {location}")
    return []

@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def find_book_by_id(book_id: int = Path(gt=0, description="The ID of the book you'd like to find")):
    logger.info(f"Finding book with ID: {book_id}")
    for book in BOOKS:
        if book.id == book_id:
            logger.info(f"Found book with ID: {book_id}")
            return book
    logger.info(f"Book with ID: {book_id} not found")
    raise HTTPException(status_code=404, detail=f"Book with ID: {book_id} not found")

@app.get("/books/", status_code=status.HTTP_200_OK)
async def find_book_by_rating(min_rating: int = Query(gt=0, lt=6, default=None), max_rating: int = Query(gt=0, lt=6, default=None)):
    logger.info(f"Finding books with rating parameters: min={min_rating}, max={max_rating}")
    if min_rating is None and max_rating is None:
        return BOOKS
    elif min_rating is None:
        books = [book for book in BOOKS if book.rating <= max_rating]
    elif max_rating is None:
        books = [book for book in BOOKS if book.rating >= min_rating]
    else:
        books = [book for book in BOOKS if min_rating <= book.rating <= max_rating]
    logger.info(f"Found {len(books)} books matching rating criteria")
    return books


@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    logger.info(f"Updating book with ID: {book.id}")
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = Book(**book.model_dump())
            logger.info(f"Successfully updated book with ID: {book.id}")
            return
    logger.info(f"Book with ID: {book.id} not found")
    raise HTTPException(status_code=404, detail=f"Book with ID: {book.id} not found")


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0, description="The ID of the book you'd like to delete")):
    logger.info(f"Deleting book with ID: {book_id}")
    book_deleted = False
    for book in BOOKS:
        if book.id == book_id:
            BOOKS.remove(book)
            logger.info(f"Successfully deleted book with ID: {book_id}")
            book_deleted = True
            break
    if not book_deleted:
        logger.info(f"Book with ID: {book_id} not found")
        raise HTTPException(status_code=404, detail=f"Book with ID: {book_id} not found")