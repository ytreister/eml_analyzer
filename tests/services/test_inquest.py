from io import BytesIO

import pytest
import respx

from app.services.inquest import InQuest


@pytest.mark.asyncio
@respx.mock
async def test_dfi_details(inquest_dfi_details_response: str):
    sha256 = "e86c5988a3a6640fb90b90b9e9200e4cce0669594dbb5422622946208c124149"
    respx.get(
        f"https://labs.inquest.net/api/dfi/details?sha256={sha256}",
        content=inquest_dfi_details_response,
    )

    api = InQuest()
    res = await api.dfi_details(sha256)
    assert res is not None
    data = res.get("data", {})
    assert data.get("classification", "") == "MALICIOUS"


@pytest.mark.asyncio
@respx.mock
async def test_dfi_details_with_eicar():
    sha256 = "275a021bbfb6489e54d471899f7db9d1663fc695ec2fe2a2c4538aabf651fd0f"
    respx.get(
        f"https://labs.inquest.net/api/dfi/details?sha256={sha256}",
        content="",
        status_code=404,
    )

    api = InQuest()
    res = await api.dfi_details(sha256)
    assert res is None


@pytest.mark.asyncio
@respx.mock
async def test_dfi_upload(encrypted_docx: bytes, inquest_dfi_upload_response: str):
    respx.post(
        "https://labs.inquest.net/api/dfi/upload", content=inquest_dfi_upload_response
    )

    file_ = BytesIO(encrypted_docx)
    file_.name = "encrypted.docx"

    api = InQuest()
    res = await api.dfi_upload(file_)
    assert res is not None
    assert (
        res.get("data", "")
        == "539e4557975be726d0fc8d7813dba5470dd703272957b4476296f976b5678900"
    )
