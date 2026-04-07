import json

def load_books():
    with open("data.json","r") as file:
       return json.load(file)

def save_books(books):
    with open("data.json","w") as file:
        json.dump(books,file,indent=4)