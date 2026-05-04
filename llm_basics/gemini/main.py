from fastapi import Fastapi,UploadFile,File,HTTPException
''' FastAPI: main app class
UploadFile: for handling file uploads
File: to declare file inputs in endpoints
HTTPException: for returning error responses'''
from fastapi.middleware.cors import CORSMiddleware
# Enables Cross-Origin Resource Sharing (CORS), allowing frontend apps (like React) to call your API.

from pydantic import BaseModel
import google.generativeai as genai
from PIL import Image
# Python Imaging Library (Pillow) to process uploaded images.
import io 
# Handles byte streams (used to convert uploaded file into an image).
import os # to access env variables 

app = Fastapi(title="Gemini Gateway")

# Allows requests from any frontend (* = all domains).
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_methods=["*"],
    allow_credentials=True
)

API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# request schema
class TextRequest(BaseModel):
    prompt:str

# Defines input format for /text endpoint. Expects JSON 


# Text generation endpoint
@app.post("/text")
async def text_gen(req : TextRequest):
    try:
      response = model.generate_content(req.prompt)
      print(response)
      print(response.text)
      return {"success":True, "response":response.text}
    except Exception as e:    
      raise HTTPException(status_code=500,detail=str(e))

@app.post("/image")
async def image_analysis(file:UploadFile = File(...)): # accepts file upload[... - required]      
    try:
       if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400,detail="Must be Image !")

       contents = await file.read()  # Reads file into memory as bytes.
       img = Image.open(io.BytesIO(contents)) # Converts bytes → image object using Pillow.
       response = model.generate_content(["Describe This",img]) # Sends prompt + image to Gemini for analysis.
       
       return {"success":True,"response":response.text}
    except Exception as e:  
       raise HTTPException(status_code=400,detail=str(e))

@app.get("/health")
async def health():
   return {"status":"OK"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

'''
GOOGLE_API_KEY="your-key" python app.py

# Health
curl http://localhost:8000/health

# Text
curl -X POST http://localhost:8000/text \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Hi"}'

# Image
curl -X POST http://localhost:8000/image \
  -F "file=@photo.jpg"

'''    