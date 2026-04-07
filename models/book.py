from pydantic import BaseModel, field_validator,model_validator
from typing import ClassVar


class Book(BaseModel):
    name: str
    author: str
    category: str
    price: int
    allowed_categories: ClassVar[list[str]] = ["Adventure","Self-help","Sci-Fi","Finance","Action"]

    @field_validator("author")
    @classmethod
    def validate_author(cls, value):
        if len(value) < 3:
            raise ValueError("Author Name Must be atleast 3 Charcters long")
        return value
    
    # cls -> class [same like self to access current object variables]
    @field_validator("category")
    @classmethod
    def validate_category(cls, value):
        print(cls)
        if value not in cls.allowed_categories:
            raise ValueError("Not Valid Category !!")
        return value
    
    @model_validator(mode="before")
    @classmethod # dictionary : values
    def validate_and_fix_price(cls,values):
        category = values.get("category")
        price = values.get("price")
        if category == "Finance":
           # If price is missing or < 1000 -> fix it
           if price is None or price < 1000:
             values["price"] = 1100
        return values

    @model_validator(mode="after")
    def validate_price_catgeory(self):
        if self.category == "Finance" and self.price < 1000:
            raise ValueError("Price of the Finance Book can not be below 1000 !!")
        return self    

# Order of execution
# Type check (str, int, etc.)
# Then your validator runs
'''
[In Pydantic : Validation]
1. ValueError : raise valueError("Price must be positive")
2. TypeError: Wrong data type :raise TypeError("Author must be a string")
3. AssertionError : assert: len(value) > 3, "Too Short"

# custom : HTTPException [for API-level errors] [inside route functions ]
from fastapi import HTTPException

raise HTTPException(status_code=404, detail="Book Not Found")
'''