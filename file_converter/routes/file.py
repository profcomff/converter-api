from fastapi import APIRouter, File, UploadFile, Request
from file_converter.settings import Settings, get_settings
from fastapi.params import Depends
from fastapi.exceptions import HTTPException
from file_converter.utils.convertable import check_pdf_ok, convert
import requests
from file_converter.utils.commands import run

router = APIRouter()


@router.post("/")
async def upload_file(
    to_ext: str, file: UploadFile = File(...), settings: Settings = Depends(get_settings), request: Request = None
):
    """Upload file to server. Takes extention to wich the file will be converted and the file"""
    if not to_ext in settings.CONVERT_TYPES:
        raise HTTPException(415, 'unsupported to_ext')
    if file.filename.split(".")[1] not in settings.EXTENTIONS:
        raise HTTPException(
            415,
            f'Only {", ".join(settings.EXTENTIONS)} files allowed, but {file.content_type} recieved',
        )

    result = await convert(file, to_ext, settings.STATIC_FOLDER)
    if not await check_pdf_ok(result):
        await run(f"rm {result}")
        raise (HTTPException(415, "file corrupted"))
    try:
        requests.post(settings.PRINTER_URL, data={"file_link": result})
    except requests.ConnectionError:
        pass
    return {'status': "ok", 'link': result}
