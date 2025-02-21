import os

from fastapi import APIRouter, HTTPException, UploadFile, File
from starlette.responses import FileResponse

from src.schemas.data import EditFileRequest
from src.utils.decode import decode_binary_file
from src.utils.encode import encode_binary_file

router = APIRouter()


@router.post("/upload_file")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()

    with open(file.filename, "wb") as f:
        f.write(content)
    try:
        decoded_data = decode_binary_file(file.filename)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Decoding error: {str(e)}")

    return {"filename": file.filename, "decoded_data": decoded_data}


@router.post("/edit")
async def edit_file(data: EditFileRequest):
    if not os.path.isfile(data.filename):
        raise HTTPException(status_code=404, detail="File not found")

    content = encode_binary_file(data)

    with open(data.filename, "wb") as f:
        f.write(content)

    return {"message": "File updated successfully"}


@router.get("/download")
async def download_file(filename: str):
    return FileResponse(
        filename, filename=filename, media_type="application/octet-stream"
    )


@router.get("/read")
async def read_file(filename: str):
    try:
        decoded_data = decode_binary_file(filename)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Decoding error: {str(e)}")

    return {"filename": filename, "decoded_data": decoded_data}
