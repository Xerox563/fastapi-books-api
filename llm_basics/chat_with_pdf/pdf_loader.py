"""Updated PDF loader with text cleaning."""

import PyPDF2
import re
from typing import Tuple

class PDFLoader:
    """Load and clean PDF text."""
    
    @staticmethod
    def clean_text(text: str) -> str:
        """
        Clean extracted text from PDF.
        
        WHY: PDFs have formatting artifacts we don't need
        HOW: Remove extra spaces, fix line breaks
        RESULT: Clean text ready for processing
        """
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters (keep alphanumeric, spaces, punctuation)
        text = re.sub(r'[^\w\s.,!?-]', '', text)
        
        # Fix sentence spacing
        text = re.sub(r'(\w)\. (\w)', r'\1. \2', text)
        
        return text.strip()
    
    @staticmethod
    def load_pdf(pdf_path: str) -> Tuple[str, int]:
        """
        Load PDF and extract clean text.
        
        Returns:
            Tuple of (extracted_text, num_pages)
        """
        full_text = ""
        num_pages = 0
        
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                num_pages = len(pdf_reader.pages)
                
                print(f"📄 PDF has {num_pages} pages")
                
                for page_num in range(num_pages):
                    page = pdf_reader.pages[page_num]
                    text = page.extract_text()
                    
                    # Clean the text
                    cleaned = PDFLoader.clean_text(text)
                    
                    # Add page number
                    full_text += f"\n[PAGE {page_num + 1}]\n{cleaned}\n"
                    
                    print(f"  ✓ Page {page_num + 1}: {len(cleaned)} chars")
            
            print(f"✓ Extracted {len(full_text)} characters total\n")
            return full_text, num_pages
        
        except FileNotFoundError:
            print(f"❌ PDF file not found: {pdf_path}")
            return "", 0
        except Exception as e:
            print(f"❌ Error: {e}")
            return "", 0


# Test the cleaner
if __name__ == "__main__":
    # Test text cleaning
    messy = "This   is   text with\n\n\nstrange    spacing"
    clean = PDFLoader.clean_text(messy)
    print(f"Original: {messy}")
    print(f"Cleaned: {clean}")