from typing import List

class TextChunker:
   def __init__(self,chunk_size:int = 500,overlap :int=50):
       self.chunk_size = chunk_size
       self.overlap = overlap

   def chunk_text(self,text:str) -> list[str]:
       chunks = []
       s = 0
       while s < len(text):
           e = min(len(text), s + self.chunk_size)
           chunk = text[s:e]

           if len(chunk) > self.overlap:
               chunks.append(chunk)    

           s = e - self.overlap
       return chunks        