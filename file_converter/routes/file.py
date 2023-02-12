from fastapi import APIRouter, File, UploadFile, Response
from pydantic import Field
from file_converter.schema import BaseModel
from file_converter.settings import Settings, get_settings
from fastapi.params import Depends
from fastapi.exceptions import HTTPException
from file_converter.utils import converter


router = APIRouter()


class SendInput(BaseModel):
    to_ext: str = Field(
        description="extention to we are going to convert",
        example='pdf',
    )

    
@router.post("/")
async def upload_file(
   inp: SendInput, file: UploadFile = File(...), settings: Settings = Depends(get_settings)
):
    """Upload file to server. Takes extention to wich the file will be converted and the file
    """
    if file == ...:
        raise HTTPException(400, 'No file recieved')

    if file.content_type not in settings.CONTENT_TYPES:
        raise HTTPException(
            415,
            f'Only {", ".join(settings.CONTENT_TYPES)} files allowed, but {file.content_type} recieved',
        )
    result = await converter.convert(file, inp.to_ext)
    '''
    path =  path = abspath(settings.STATIC_FOLDER) + '/' + "test"

    async with aiofiles.open(path, 'wb') as saved_file:
        memory_file = await file.read()
        if len(memory_file) > settings.MAX_SIZE:
            raise HTTPException(415, f'File too large, {settings.MAX_SIZE} bytes allowed')
        await saved_file.write(memory_file)
    await file.close()
    '''
    return Response(content=result[0], media_type=result[1])

