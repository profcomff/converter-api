from auth_lib.fastapi import UnionAuth
from fastapi import APIRouter, File, UploadFile
from fastapi.exceptions import HTTPException
from fastapi.params import Depends, Form
from pydantic import BaseModel

from file_converter.converters.convert import convert
from file_converter.exceptions import ConvertError, EqualExtensions, ForbiddenExt, UnsupportedToExt
from file_converter.settings import Settings, get_settings


router = APIRouter()


class ConvertRespSchema(BaseModel):
    status: str
    file_url: str


@router.post("/convert", response_model=ConvertRespSchema)
async def process(
    file: UploadFile = File(),
    to_ext: str = Form(default=None),
    settings: Settings = Depends(get_settings),
    _=Depends(UnionAuth()),
):
    """Upload file to server. Takes extension to which the file will be converted and the file"""

    try:
        result = await convert(file, to_ext)
    except EqualExtensions:
        raise HTTPException(status_code=400, detail="File extension is equals to 'to_ext'")

    except UnsupportedToExt:
        raise HTTPException(
            status_code=415,
            detail=f'Files are allowed to be converted only to {", ".join(settings.CONVERT_TYPES)}',
        )

    except ConvertError:
        raise HTTPException(status_code=400, detail='Posted file is corrupted')

    except ForbiddenExt:
        raise HTTPException(status_code=415, detail=f'Only {", ".join(settings.EXTENTIONS)} files are allowed.')

    root_path = str(settings.ROOT_PATH).removesuffix('/')
    return {
        "status": "Success",
        "file_url": f'{root_path}/{str(settings.STATIC_FOLDER)}/{result}',
    }  # Отдает URL на файл
