router = APIRouter()

file_storage = {}


@router.post("/uploadFile", )
async def upload_file(data: UploadFile = File(...)):
    content = await data.read()
    file_storage[data] = content
    return {"message": "File uploaded successfully"}


@router.post("/edit")
async def edit_file(data: dict):
    if "binary_file" not in file_storage:
        raise HTTPException(status_code=400, detail="No file uploaded")

    parsed_data = decode_binary_file(file_storage["binary_file"])

    if "temperature" in data:
        parsed_data["temperature"] = data["temperature"]

    for test in parsed_data["tests"]:
        if test["type"] == "PTR" and test["test_name"] == data["test_name"]:
            test["test_value"] = data["value"]
            test["low"] = data["low_limit"]
            test["high"] = data["high_limit"]
            test["pass_fail"] = data["status"]

    file_storage["binary_file"] = encode_binary_file(parsed_data)

    return {"message": "File updated successfully"}


