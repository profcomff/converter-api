import pytest
from starlette import status

from file_converter.settings import get_settings


url = '/convert'
settings = get_settings()


@pytest.mark.authenticated()
def test_dock_success(client):
    data = {'to_ext': 'pdf'}
    fileName = 'tests/files/test.docx'
    files = {
        'file': (
            f"{fileName}",
            open(f"{fileName}", 'rb'),
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )
    }
    res = client.post(url, data=data, files=files)
    assert res.status_code == status.HTTP_200_OK


@pytest.mark.authenticated()
def test_doc_success(client):
    data = {'to_ext': 'pdf'}
    fileName = 'tests/files/test.doc'
    files = {
        'file': (
            f"{fileName}",
            open(f"{fileName}", 'rb'),
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )
    }
    res = client.post(url, data=data, files=files)
    assert res.status_code == status.HTTP_200_OK


@pytest.mark.authenticated()
def test_post_broken(client):
    data = {'to_ext': 'pdf'}
    fileName = 'tests/files/test_broken.docx'
    files = {
        'file': (
            f"{fileName}",
            open(f"{fileName}", 'rb'),
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )
    }

    res = client.post(url, data=data, files=files)
    assert res.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.authenticated()
def test_post_unsupported_convert_type(client):
    data = {'to_ext': 'xls'}
    fileName = 'tests/files/test.docx'
    files = {
        'file': (
            f"{fileName}",
            open(f"{fileName}", 'rb'),
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )
    }
    res = client.post(url, data=data, files=files)
    assert res.status_code == status.HTTP_415_UNSUPPORTED_MEDIA_TYPE


@pytest.mark.authenticated()
def test_post_broken_ext(client):
    data = {'to_ext': 'pdf'}
    fileName = 'tests/files/test'
    files = {
        'file': (
            f"{fileName}",
            open(f"{fileName}", 'rb'),
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )
    }
    res = client.post(url, data=data, files=files)
    assert res.status_code == status.HTTP_415_UNSUPPORTED_MEDIA_TYPE


def test_extensions(client):
    req = client.get("/extensions")
    assert req.status_code == 200
    assert req.json() == {"in": settings.CONVERT_TYPES, "out": settings.EXTENTIONS}
