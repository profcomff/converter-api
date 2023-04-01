from fastapi import APIRouter, File, UploadFile, Request
from pydantic import BaseModel

from file_converter.settings import Settings, get_settings
from fastapi.params import Depends, Form
from fastapi.exceptions import HTTPException
from file_converter.utils.convertable import check_pdf_ok, convert
from file_converter.utils.commands import run
import aiohttp

router = APIRouter()


async def main(url: str, data: dict):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, data=data) as response:
            pass


class Input(BaseModel):
    to_ext: str


@router.post("/")
async def upload_file(file: UploadFile = File(), to_ext : str = Form(default=None), settings: Settings = Depends(get_settings)):
    """Upload file to server. Takes extention to wich the file will be converted and the file"""
    if not to_ext in settings.CONVERT_TYPES:
        raise HTTPException(415, 'unsupported to_ext')
    if file.filename.split(".")[-1] not in settings.EXTENTIONS:
        raise HTTPException(
            415,
            f'Only {", ".join(settings.EXTENTIONS)} files allowed, but {file.content_type} recieved',
        )

    result = await convert(file, to_ext, settings.STATIC_FOLDER)
    if not await check_pdf_ok(result):
        await run(f"rm {result}")
        raise (HTTPException(413, "file corrupted"))
    await (main(settings.PRINTER_URL, data={"file_link": result}))
    return {'status': "ok", 'link': result}
