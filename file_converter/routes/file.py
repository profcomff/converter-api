from fastapi import APIRouter, File, UploadFile
from file_converter.settings import Settings, get_settings
from fastapi.params import Depends
from fastapi.exceptions import HTTPException
from file_converter.utils import converter
from fastapi.responses import FileResponse
from file_converter.utils.converter import check_pdf_ok
from os.path import exists
import aiofiles.os
import requests

router = APIRouter()


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
    if (not await check_pdf_ok(result[1])) or (not exists(result[1])):
        await aiofiles.os.remove(result[1])
        raise (HTTPException(415, "file corrupted"))
    try:
        requests.post(settings.PRINTER_URL, data={"file_link": result[1]})
    except requests.ConnectionError:
        pass
    return {'status': "ok", 'link': f"static/{result[0]}"}
