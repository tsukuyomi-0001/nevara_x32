from fastapi.responses import StreamingResponse
from nevara import agent_invoke, agent_stream
from collections.abc import AsyncIterator
from fastapi import FastAPI, File, UploadFile, HTTPException
from nevara.globalOp import document_retriever
from pathlib import Path
import json
import os

app = FastAPI()
UPLOAD_DIR = Path('./res').resolve()

## following is legacy static invoke, no streaming...
@app.get('/invoke')
def invoke(message: str) -> str:
    message = agent_invoke(message)
    return message

async def _sse_stream(message: str) -> AsyncIterator[str]:
    async for chunk in agent_stream(message):
        yield f"data: {json.dumps(chunk)}\n\n"


@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename or "temp.cache")

    try:
        with open(file_path, 'wb') as buffer:
            while chunk := await file.read(1024*1024):
                buffer.write(chunk)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"could not save file: {e}")
    finally:
        await file.close()

    document_retriever.remake_vector_db()

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "saved_path": file_path,
        "status": "success"
    }

@app.get("/get_uploads")
async def get_uploads():
    files = [file.name for file in UPLOAD_DIR.glob("*")]
    return files

@app.post("/remove_upload")
async def remove_upload(file: str):
    target_file = (UPLOAD_DIR / file).resolve()
    if UPLOAD_DIR.resolve() not in target_file.parents:
        raise HTTPException(status_code=400, detail="Invalid file path.")
    
    if target_file.exists() and target_file.is_file():
        target_file.unlink()

    document_retriever.remake_vector_db()
            
    return {"status": "success", "message": "Files processed successfully."}

@app.post("/invoke_v2")
async def invoke_v2(message: str) -> StreamingResponse:
    return StreamingResponse(
        _sse_stream(message),
        media_type="text/event-stream",
        headers={
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no'
        }
    )