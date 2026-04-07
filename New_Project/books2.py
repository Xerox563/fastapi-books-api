from fastapi import FastAPI,Body,Path,Query,HTTPException
from pydantic import BaseModel,Field
from typing import Optional
from starlette import status

app = FastAPI() 


class Book:
    id:int
    title:str
    author:str
    description:str
    rating:int
    price :int
    

    def __init__(self,id,title,author,description,rating,price):
        self.id = id
        self.title = title
        self.description = description
        self.author = author
        self.rating = rating
        self.price = price


# Pydantic Object
class BookRequest(BaseModel):
    id: Optional[int] = Field(default=None, description="id is not needed") 
    title:str = Field(min_length=3,max_length=50)
    author:str 
    description:str
    rating:int = Field(gt = -1 ,lt = 11) # rating must be [0,10]
    price :int

    model_config = {
        "json_schema_extra":{
            "example":{
                "title":"A new Book",
                "author":"Code with Amit",
                "description":"A new descripiton of a book",
                "rating":5,
                "price":500
            }
        }
    }


BOOKS = [
    Book(1, "Rich Dad Poor Dad", "Robert Kiyosaki", "A very good book about financial literacy and wealth mindset", 8, 900),
    Book(2, "Atomic Habits", "James Clear", "A powerful guide to building good habits and breaking bad ones", 9, 750),
    Book(3, "The Alchemist", "Paulo Coelho", "A philosophical story about following your dreams and destiny", 9, 600),
    Book(4, "Think and Grow Rich", "Napoleon Hill", "Classic book on success principles and financial achievement", 8, 850),
    Book(5, "Deep Work", "Cal Newport", "Focuses on productivity and the power of deep concentration", 8, 700),
    Book(6, "Ikigai", "Héctor García", "Explains the Japanese concept of purpose and meaningful living", 9, 650),
    Book(7, "The Power of Now", "Eckhart Tolle", "Spiritual guide to living in the present moment", 8, 800),
    Book(8, "Zero to One", "Peter Thiel", "Insights on startups and building innovative businesses", 8, 900),
    Book(9, "Start With Why", "Simon Sinek", "Explains how great leaders inspire action through purpose", 9, 780),
    Book(10, "The 4-Hour Workweek", "Timothy Ferriss", "Guide to escaping the 9-5 and designing a lifestyle", 8, 850)
]


@app.get("/books",status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS



@app.post("/create-book")
# async def create_book(book_request = Body()):
async def create_book(book_request :BookRequest):
    print(type(BookRequest))
    new_book = Book(**book_request.model_dump())
    print(type(new_book))
    # BOOKS.append(new_book)
    BOOKS.append(find_book_id(new_book))
    return {"message": "Book added successfully", "book": new_book}


def find_book_id(book : Book):

    # if len(BOOKS) > 0:
    #     book.id = BOOKS[-1].id + 1
    # else:
    #     book.id = 1

    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book

@app.get("/books/{book_id}",status_code=status.HTTP_200_OK)
def read_single_book(book_id :int = Path(gt = 0 , lt = 6)): # here Path : allows to put validation over the dynamic path variable.[either path parameter is valid or not !!]
    for book in BOOKS:
        if book.id == book_id:
            return book
        


    raise HTTPException(status_code=404,detail="Item not Found")

# HTTP Exception : It’s a way to send error responses with proper status codes