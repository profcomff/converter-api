from starlette import status
from file_converter.settings import get_settings


url = '/'
settings = get_settings()


def test_dock_success(client):
    fileName = 'tests/test_routes/test_files/test.docx'
    files = {
        'file': (
            f"{fileName}",
            open(f"{fileName}", 'rb'),
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ),
        "to_ext": "pdf"
    }
    res = client.post(url, files=files)
    assert res.status_code == status.HTTP_200_OK


def test_doc_success(client):
    fileName = 'tests/test_routes/test_files/test.doc'
    files = {
        'file': (
            f"{fileName}",
            open(f"{fileName}", 'rb'),
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ),
        "to_ext": "pdf"
    }
    res = client.post(url, files=files)
    assert res.status_code == status.HTTP_200_OK


def test_post_broken(client):
    fileName = 'tests/test_routes/test_files/test_broken.docx'
    files = {
        'file': (
            f"{fileName}",
            open(f"{fileName}", 'rb'),
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ),
        "to_ext": "pdf"

    }
    res = client.post(url, files=files)
    assert res.status_code == status.HTTP_413_REQUEST_ENTITY_TOO_LARGE


def test_post_unsupported_convert_type(client):
    fileName = 'tests/test_routes/test_files/test.docx'
    files = {
        'file': (
            f"{fileName}",
            open(f"{fileName}", 'rb'),
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ),
        "to_ext": "pdf"
    }
    res = client.post(url,  files=files)
    assert res.status_code == status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
