from starlette import status
from file_converter.settings import get_settings


url = '/'
settings = get_settings()


def test_dock_success(client):
    body = {
        "to_ext": "pdf",
    }
    fileName = 'tests/test_routes/test_files/test.docx'
    files = {
        'file': (
            f"{fileName}",
            open(f"{fileName}", 'rb'),
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )
    }
    res = client.post(url, params=body, files=files)
    assert res.status_code == status.HTTP_200_OK


def test_doc_success(client):
    body = {
        "to_ext": "pdf",
    }
    fileName = 'tests/test_routes/test_files/test.doc'
    files = {
        'file': (
            f"{fileName}",
            open(f"{fileName}", 'rb'),
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )
    }
    res = client.post(url, params=body, files=files)
    assert res.status_code == status.HTTP_200_OK


def test_post_broken(client):
    body = {
        "to_ext": "pdf",
    }
    fileName = 'tests/test_routes/test_files/test_broken.docx'
    files = {
        'file': (
            f"{fileName}",
            open(f"{fileName}", 'rb'),
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )
    }
    res = client.post(url, params=body, files=files)
    assert res.status_code == status.HTTP_415_UNSUPPORTED_MEDIA_TYPE


def test_post_unsupported_convert_type(client):
    body = {
        "to_ext": "asdfgh",
    }
    fileName = 'tests/test_routes/test_files/test.docx'
    files = {
        'file': (
            f"{fileName}",
            open(f"{fileName}", 'rb'),
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )
    }
    res = client.post(url, params=body, files=files)
    assert res.status_code == status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
