from fastapi import APIRouter, File, UploadFile
from file_converter.settings import Settings, get_settings
from fastapi.params import Depends, Form
from fastapi.exceptions import HTTPException
from file_converter.utils.convertable import convert
from file_converter.utils.check_pdf import check_pdf_ok
from pydantic import BaseModel

router = APIRouter()


class ConvertRespSchema(BaseModel):
    status: str
    file_dir: str


@router.post("/")
async def upload_file(file: UploadFile = File(),
                      to_ext: str = Form(default=None),
                      settings: Settings = Depends(get_settings),
                      response_model=ConvertRespSchema):
    """Upload file to server. Takes extension to which the file will be converted and the file"""

    if not to_ext in settings.CONVERT_TYPES:
        raise HTTPException(415, 'unsupported to_ext')
    if file.filename.split(".")[-1] not in settings.EXTENTIONS:
        raise HTTPException(
            415,
            f'Only {", ".join(settings.EXTENTIONS)} files are allowed.',
        )

    result = await convert(file, to_ext)
    if not await check_pdf_ok(result):
        raise (HTTPException(413, "file corrupted"))
    root_path = settings.ROOT_PATH.removesuffix('/')
    return {"status": "okay", "file_url": f'{root_path}/{settings.STATIC_FOLDER}/{result}'}  #Отдает URL на файл
