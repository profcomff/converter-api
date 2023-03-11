from fastapi import APIRouter, File, UploadFile, Request, Body
from pydantic import BaseModel

from file_converter.settings import Settings, get_settings
from fastapi.params import Depends
from fastapi.exceptions import HTTPException
from file_converter.utils.convertable import check_pdf_ok, convert
from file_converter.utils.commands import run
import aiohttp

router = APIRouter(prefix="/file")
settings = get_settings()

async def main(url: str, data: dict):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, data=data) as response:
            pass


class Input(BaseModel):
    toext: str | None

    class Config:
        orm_mode = True


@router.post("", response_model=dict)
async def upload_file(inp: Input = Depends(), file: UploadFile = File(...)):
    """Upload file to server. Takes extention to wich the file will be converted and the file"""
    if not inp.to_ext in settings.CONVERT_TYPES:
        raise HTTPException(415, 'unsupported to_ext')
    if file.filename.split(".")[-1] not in settings.EXTENTIONS:
        raise HTTPException(
            415,
            f'Only {", ".join(settings.EXTENTIONS)} files allowed, but {file.content_type} recieved',
        )

    result = await convert(file, inp.to_ext, settings.STATIC_PATH)
    if not await check_pdf_ok(result):
        await run(f"rm {result}")
        raise (HTTPException(413, "file corrupted"))
    await (main(settings.PRINTER_URL, data={"file_link": result}))
    return {'status': "ok", 'link': result}
