from fastapi import APIRouter, File, UploadFile, Request
from file_converter.settings import Settings, get_settings
from fastapi.params import Depends
from fastapi.exceptions import HTTPException
from file_converter.utils import converter
from file_converter.utils.converter import check_pdf_ok
from os.path import exists
import aiofiles.os
import requests

router = APIRouter()


@router.post("/")
async def upload_file(to_ext: str, file: UploadFile = File(...), settings: Settings = Depends(get_settings), request: Request = None):
    """Upload file to server. Takes extention to wich the file will be converted and the file"""
    if file == ...:
        raise HTTPException(400, 'No file recieved')
    if not to_ext in settings.CONVERT_TYPES:
        raise HTTPException(415, 'unsupported to_ext')
    
    length = 0#int(request.headers.get('Content-Length'))
    print(length)
    if length > settings.MAX_SIZE:
            raise HTTPException(415, f'File too large, {settings.MAX_SIZE} bytes allowed')

    if file.content_type not in settings.CONTENT_TYPES:
        raise HTTPException(
            415,
            f'Only {", ".join(settings.CONTENT_TYPES)} files allowed, but {file.content_type} recieved',
        )
    result = await converter.convert(file, to_ext, settings)
    if (not await check_pdf_ok(result[1])) or (not exists(result[1])):
        await aiofiles.os.remove(result[1])
        raise (HTTPException(415, "file corrupted"))
    try:
        requests.post(settings.PRINTER_URL, data={"file_link": result[1]})
    except requests.ConnectionError:
        pass
    return {'status': "ok", 'link': f"static/{result[0]}"}
