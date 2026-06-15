import PyPDF2
from io import BytesIO
from typing import Optional

def extract_text_from_pdf(pdf_bytes: bytes) -> Optional[str]:
    """
    Extract text from a PDF file using text extraction and OCR fallback.
    
    Args:
        pdf_bytes: PDF file content as bytes
        
    Returns:
        Extracted text or None if extraction fails
    """
    # First attempt: Direct text extraction
    try:
        pdf_reader = PyPDF2.PdfReader(BytesIO(pdf_bytes))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        
        # If we got substantial text, return it
        if text.strip() and len(text) > 100:
            return text
    except Exception as e:
        print(f"Error in direct PDF extraction: {e}")
    
    # Second attempt: OCR for scanned PDFs
    try:
        from pdf2image import convert_from_bytes
        import pytesseract
        
        images = convert_from_bytes(pdf_bytes, dpi=200)
        ocr_text = ""
        
        for i, image in enumerate(images):
            ocr_text += pytesseract.image_to_string(image)
            ocr_text += "\n"
        
        return ocr_text if ocr_text.strip() else None
    except ImportError:
        print("OCR libraries not available. Please install: pytesseract, pdf2image, pillow")
        return None
    except Exception as e:
        print(f"Error in OCR extraction: {e}")
        return None

def extract_text_from_docx(docx_bytes: bytes) -> Optional[str]:
    """
    Extract text from a DOCX file.
    
    Args:
        docx_bytes: DOCX file content as bytes
        
    Returns:
        Extracted text or None if extraction fails
    """
    try:
        from docx import Document
        doc = Document(BytesIO(docx_bytes))
        text = "\n".join([para.text for para in doc.paragraphs])
        return text if text.strip() else None
    except Exception as e:
        print(f"Error extracting DOCX: {e}")
        return None
