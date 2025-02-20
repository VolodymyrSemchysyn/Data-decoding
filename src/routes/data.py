import traceback

from fastapi import APIRouter, HTTPException, UploadFile, File
from starlette.responses import FileResponse

from src.utils.decode import decode_binary_file
from src.utils.encode import encode_binary_file

router = APIRouter()


@router.post("/uploadFile")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()

    with open(file.filename, "wb") as f:
        f.write(content)
    try:
        decoded_data = decode_binary_file(file.filename)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=f"Decoding error: {str(e)}")

    return {"filename": file.filename, "decoded_data": decoded_data}


@router.post("/edit")
async def edit_file(data: dict):
    parsed_data = decode_binary_file(data["filename"])

    if "temperature" in data:
        parsed_data["temperature"] = data["temperature"]

    for i, test in enumerate(data["tests"]):
        if i < len(parsed_data["tests"]):
            parsed_data["tests"][i]["type"] = test["type"]
            if test["type"] == "PRR":
                parsed_data["tests"][i]["part_number"] = test["part_number"]
                parsed_data["tests"][i]["pass_fail"] = test["pass_fail"]
            elif test["type"] == "PTR":
                parsed_data["tests"][i]["test_name"] = test["test_name"]
                parsed_data["tests"][i]["test_value"] = test["test_value"]
                parsed_data["tests"][i]["low"] = test["low"]
                parsed_data["tests"][i]["high"] = test["high"]
                parsed_data["tests"][i]["pass_fail"] = test["pass_fail"]

    content = encode_binary_file(parsed_data)

    with open(data["filename"], "wb") as f:
        f.write(content)

    return {"message": "File updated successfully"}


@router.get("/download")
async def download_file(filename: str):
    return FileResponse(filename, filename=filename, media_type="application/octet-stream")


@router.get("/read")
async def read_file(filename: str):
    try:
        decoded_data = decode_binary_file(filename)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=f"Decoding error: {str(e)}")

    return {"filename": filename, "decoded_data": decoded_data}
