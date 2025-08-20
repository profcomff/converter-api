import pytest
from starlette import status

from file_converter.settings import get_settings


url = '/convert'
settings = get_settings()


@pytest.mark.authenticated()
def test_pandoc_docx_to_html(client):
    """Test Pandoc conversion from DOCX to HTML"""
    data = {'to_ext': 'html'}
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
def test_pandoc_same_extension(client):
    """Test that same extension conversion throws EqualExtensions error"""
    data = {'to_ext': 'docx'}
    fileName = 'tests/files/test.docx'
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
def test_new_extensions_endpoint(client):
    """Test that extensions endpoint includes new formats"""
    req = client.get("/extensions")
    assert req.status_code == 200
    response_data = req.json()
    
    # Check that we have more input formats (what we accept)
    assert "odt" in response_data["out"]
    assert "rtf" in response_data["out"]
    
    # Check that we have more output formats (what we convert to)  
    assert "html" in response_data["in"]
    assert "docx" in response_data["in"]
    assert "odt" in response_data["in"]