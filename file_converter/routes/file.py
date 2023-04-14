from fastapi import APIRouter, File, UploadFile
from file_converter.settings import Settings, get_settings
from fastapi.params import Depends, Form
from fastapi.exceptions import HTTPException
from file_converter.converters.convert import convert
from pydantic import BaseModel
from file_converter.exceptions import ForbiddenExt, ConvertError, Unsupported_to_ext

router = APIRouter()


class ConvertRespSchema(BaseModel):
    status: str
    file_url: str


@router.post("/", response_model=ConvertRespSchema)
async def upload_file(file: UploadFile = File(),
                      to_ext: str = Form(default=None),
                      settings: Settings = Depends(get_settings)
                      ):
    """Upload file to server. Takes extension to which the file will be converted and the file"""

    if to_ext not in settings.CONVERT_TYPES:
        raise HTTPException(415, 'unsupported to_ext')

    try:
        result = await convert(file, to_ext)

    except Unsupported_to_ext:
        raise HTTPException(status_code=415,
                            detail=f'Files are allowed to be converted only to {settings.CONVERT_TYPES[0]}'
                            )

    except ConvertError:
        raise HTTPException(status_code=400, detail='Posted file is corrupted')

    except ForbiddenExt:
        raise HTTPException(status_code=415,
                            detail=f'Only {", ".join(settings.EXTENTIONS)} files are allowed.'
                            )

    root_path = settings.ROOT_PATH.removesuffix('/')
    return {"status": "Success", "file_url": f'{root_path}/{settings.STATIC_FOLDER}/{result}'}  # Отдает URL на файл
