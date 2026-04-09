from fastapi import FastAPI,Depends,HTTPException,status,Path
from sqlalchemy.orm import Session
import models
from models import Todos
from database import engine,SessionLocal
from typing import Annotated
from pydantic import BaseModel

app = FastAPI()

models.Base.metadata.create_all(bind=engine) # create table in DB if they dont exist

def get_db(): # It gives your API a database session (connection) and safely closes it after use [Create DB session → Use it → Close it]
    db = SessionLocal() # creates a db connection
    try:
        yield db # [Gives db to your api , pauses function here]
    finally:
        db.close() # Always runs (even if error occurs) and Closes DB connection

'''
Request → get_db() called
        → db created
        → yield db to API
        → API uses db
        → after response → db.close()
'''

'''
1. API request [GET /]
2. FastAPI sees dependency [db: db_dependency] : i need to run get_db() first
3. get_db() runs : Creates DB session
4. FastAPI injects db : Your function recieves db
5. Your code runs : db.query(Todos).all() which Fetch all data
6. After Response, Fastapi goes back to the 
 finally:
    db.close()
# closes DB connection    

'''

db_dependency = Annotated[Session,Depends(get_db)] # depends means : “Before running my function, execute get_db() and give its result”
# Hey FastAPI, Whenever i need a DB[db will be a database session] , call get_db and give me a session



# Fetch all Todos
@app.get("/")
async def read_all(db:db_dependency,status_code=status.HTTP_200_OK):
   return db.query(Todos).all()

# Fetch todo by id
@app.get("/todo/{todo_id}",status_code=status.HTTP_200_OK)
async def read_all(db:db_dependency,todo_id:int = Path(gt = 0)):
   todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
   if todo_model is not None:
       return todo_model
   raise HTTPException(status_code=404,detail="This Todo id Does not maps with any Todo , So does not exist !!")



























# SQLite[db stored in a single file] commands 
# columns : id(primary key) | title | description | priority | complete
'''
Inserting db table [todos]:
insert into todos(title,description,priority,complete)
values ('Go to Store','To Pick up eggs',4,False)
'''

# Select all Todos [Retreive data from db]
'''
select * from todos;  # * : all rows + columns
select title from todos;  # * : all column
select title,description from todos;  # * : all column of title and desscription
'''

# Where clause [To filter data]
'''
select * from todos 
where priority = 4 AND complete = False;

select * from todos
where priority = 1 OR priority = 2;

select * from todos
where id = 2;

# LIKE (search text)
select * from todos
where title LIKE '%store%';

# IN (multiple values)
select * from todos 
where priority in (1,2,3,4,5);

# BETWEEN
select * from todos
where priority BETWEEN 1 AND 3;
'''

# UPDATE = modify existing data in a table
# syntax
'''
-- update table_name # Which table to update
-- set column = value # What to change
-- where condition # Which row to update

update todos
set complete = true
where id = 5

UPDATE todos
SET title = 'Buy Milk',
    priority = 2,
    complete = True
WHERE id = 1;

'''

# DELETE [use id]
'''
delete from table_name 
where condition;

DELETE FROM todos
WHERE title = 'Go to Store';

DELETE FROM todos; [Deletes all rows] 
'''