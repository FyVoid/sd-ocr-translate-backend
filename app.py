from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from log import logger
from PIL import Image
import io

from ocr import ocr
from translator import translate_text

app = FastAPI(
    title="SD-OCR-Translate-Server",
    description="A server for OCR and translation.",
    version="0.1.0",
)

@app.get("/")
async def root():
    return {
        "message": "SD-OCR-Translate-Server is running!",
        "usage": "TODO: Add usage instructions here."
    }
    
@app.post("/ocr")
async def ocr_from_image(file: UploadFile = File(...)):
    if file is None or file.content_type is None:
        raise HTTPException(
            status_code=400, 
            detail="Please upload a file"
        )
        
    if not file.content_type.startswith('image/'):
        raise HTTPException(
            status_code=400, 
            detail="Uploaded file is not an image"
        )
    
    try:
        logger.info(f"Processing: {file.filename}")
        
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data))
        
        blocks = ocr(image)
        input_text = []
        for block in blocks:
            text = " ".join(line['text'] for line in block['lines'])
            input_text.append(text)
            
        translated_text = translate_text(input_text, "chi")
        
        print(translated_text)
        
        return JSONResponse(
            status_code=200,
            content={
                
            }
        )
        
    except Exception as e:
        logger.error(f"OCR Error: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"OCR Error: {str(e)}"
        )