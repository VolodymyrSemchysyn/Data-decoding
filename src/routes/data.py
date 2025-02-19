router = APIRouter()

file_storage = {}

@router.post("/uploadFile",)
async def upload_file(data: UploadFile = File(...)):
    content = await data.read()
    file_storage[data] = content
    return {"message": "File uploaded successfully"}