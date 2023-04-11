from os.path import exists


async def check_pdf_ok(full_file: str):
    return exists(full_file)
