from fastapi import FastAPI
from fastapi import APIRouter
from services.book_service import load_books, save_books
from fastapi import Request
from models.book import Book

router = APIRouter()

# ------------------- Get all books ----------------------
@router.get("/books")
def get_books():
    books = load_books()  
    return books  

# filter by category
@router.get("/books/category")
def get_books_by_category(category: str):
    all_books = load_books()
    
    res_books = []
    for book in all_books:
        if book["category"].lower() == category.lower():
            res_books.append(book)

    return res_books  

# flow : browser - uvicorn - fastapi - load_books() - Json file - uvicorn - response


# filter by author + category
@router.get("/books/filter")
def get_books_by_author_category(author: str, category: str):
    all_books = load_books()
    
    res_books = []
    for book in all_books:
        if book["author"].lower() == author.lower() and book["category"].lower() == category.lower():
            res_books.append(book)

    return res_books  


# get single book 
# @router.get("/books/{book_title}")
# def get_books(book_title: str):
#     all_books = load_books() 

#     for book in all_books:
#         if book["name"].lower() == book_title.lower(): 
#             return book
#     return {"error": "Book Not Found !!"} 


# Add Book to DB [Without Pydantic]
# @router.post("/Add_book")
# async def add_book(request: Request):
#     # Recieve
#     new_book = await request.json()

#     # validate
#     required_fields = ["name","author","category","price"]
#     for field in required_fields:
#         if field not in required_fields:
#             return {"error": f"{field} is required"}
    
#     # Process
#     books = load_books()
#     books.append(new_book)

#     # store
#     save_books(books)

#     # response
#     return {
#         "message":"Book added Successfully",
#         "book": new_book
#     }

# ------------------- POST API ----------------------
@router.post("/Add_book")
async def create_book(book: Book):

    # 1. Receive + Validate (AUTO by Pydantic)
    
    # Process
    books = load_books()
    new_book = book.dict()
    books.append(new_book)

    # store
    save_books(books)

    # response
    return {
        "message":"Book added Successfully",
        "book": new_book
    }
# ------------------- PUT API ----------------------
@router.put("/books/{book_name}")
def update_book(book_name: str, updated_book: Book):
    books = load_books()

    for i, book in enumerate(books):
        if book["name"].lower() == book_name.lower():
            books[i] = updated_book.dict()

            save_books(books)

            return {"message": "Book updated successfully"}

    return {"error": "Book not found"}

# ------------------- Delete API ----------------------
@router.delete("/delete_book/{book_title}",summary="This endpoint deletes a prticular book")
def delete_book(book_title:str):
  # Load data
  all_books = load_books()   

  # Find + remove 
  for i,book in enumerate(all_books):
      if book["name"].lower() == book_title.lower():
          
          # remove from all books list
          all_books.pop(i)

          # save updated books
          save_books(all_books)

          # return message
          return {"message":"Successfully deleted the book from DB !!"}
  # not found book case        
  return {"message":"Book not Found in the DB !!"}    

'''
@router.put("/resource/{id}")
def update_resource(id: str, new_data: Model):

    # 1. What am I updating? → resource
    # We are updating a specific resource (e.g., book, user, etc.)

    # 2. How do I find it? → id (path param)
    # "id" comes from URL and uniquely identifies the item

    # 3. Where is data? → load_data()
    # Load existing data from storage (JSON / DB)
    data = load_data()

    # 4. How to update? → replace item
    # Loop through data to find matching item
    for i, item in enumerate(data):
        if item["id"] == id:

            # Replace old item with new data (PUT = full replace)
            updated_item = new_data.dict()

            # Optional safety: ensure ID remains same
            updated_item["id"] = id

            data[i] = updated_item

            # 5. Where to save? → save_data()
            # Save updated data back to storage
            save_data(data)

            # 6. What to return? → success
            return {
                "message": "Updated successfully",
                "updated_item": updated_item
            }

    # 6. What to return? → error (if not found)
    return {"error": "Resource not found"}
'''    
