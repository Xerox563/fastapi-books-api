from fastapi import FastAPI
from routes.books import router as books_router

app = FastAPI(title="Building Fast Api",description="This is to go from hero to ace", version="1.0.0")
# app = FastAPI(docs_url=None) # disabling swagger when deploying to prod

app.include_router(books_router) # It connects routes from another file to your main app
# “Attach all routes from books.router into my main app”