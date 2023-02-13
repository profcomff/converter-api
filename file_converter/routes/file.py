from fastapi import APIRouter, File, UploadFile
from file_converter.settings import Settings, get_settings
from fastapi.params import Depends
from fastapi.exceptions import HTTPException
from file_converter.utils import converter
from fastapi.responses import FileResponse
from file_converter.utils.converter import check_pdf_ok
from os.path import exists

router = APIRouter()

'''
class SendInput(BaseModel):
    to_ext: str = Field(
        description="extention to we are going to convert",
        example='pdf',
    )
'''


@router.post("/")
async def upload_file(to_ext: str, file: UploadFile = File(...), settings: Settings = Depends(get_settings)):
    """Upload file to server. Takes extention to wich the file will be converted and the file"""
    if file == ...:
        raise HTTPException(400, 'No file recieved')
    if not to_ext in settings.CONVERT_TYPES:
        raise HTTPException(415, 'unsupported convert_to type')

    if file.content_type not in settings.CONTENT_TYPES:
        raise HTTPException(
            415,
            f'Only {", ".join(settings.CONTENT_TYPES)} files allowed, but {file.content_type} recieved',
        )
    result = await converter.convert(file, to_ext, settings)
    print(check_pdf_ok(result[1]))
    if (not await check_pdf_ok(result[1])) or (not exists(result[1])):  #
        raise (HTTPException(415, "file corrupted"))
    return FileResponse(path=result[1], filename=result[0], media_type='multipart/form-data')
