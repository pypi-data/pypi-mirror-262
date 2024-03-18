"""file.py"""

from typing import List, Optional

from pydantic import BaseModel

from minimax_client.entities.common import BaseResp


class File(BaseModel):
    file_id: int
    bytes: int
    created_at: int
    filename: str
    purpose: str
    download_url: Optional[str] = None


class FileCreateResponse(BaseModel):
    file: File
    base_resp: BaseResp


class FileListResponse(BaseModel):
    files: List[File]
    base_resp: BaseResp


class FileRetriveResponse(BaseModel):
    file: File
    base_resp: BaseResp


class FileRetrieveContentResponse(BaseModel):
    content: bytes
    base_resp: BaseResp  # to be confirmed


class FileDeleteResponse(BaseModel):
    file_id: int
    base_resp: BaseResp
