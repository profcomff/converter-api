from os.path import exists


async def check_pdf_ok(full_file: str):
    if not exists(full_file):
        return False
    else:
        return True
