from fastapi import APIRouter, UploadFile, File
import os
import shutil

router = APIRouter()

UPLOAD_DIR = "data/uploads"

# Ensure upload directory exists

os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/file")
async def upload_file(file: UploadFile = File(...)):
file_path = os.path.join(UPLOAD_DIR, file.filename)

```
with open(file_path, "wb") as buffer:
    shutil.copyfileobj(file.file, buffer)

return {
    "message": "File uploaded successfully",
    "filename": file.filename,
    "path": file_path
}
```
