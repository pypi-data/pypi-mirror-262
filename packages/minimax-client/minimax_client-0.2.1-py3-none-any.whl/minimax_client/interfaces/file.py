"""file.py"""

from minimax_client.entities.file import (
    FileCreateResponse,
    FileDeleteResponse,
    FileListResponse,
    FileRetrieveContentResponse,
    FileRetriveResponse,
)
from minimax_client.interfaces.base import BaseAsyncInterface, BaseSyncInterface


class Files(BaseSyncInterface):
    """Files interface"""

    url_path: str = "files"

    def create(
        self,
        *,
        file: bytes,
        filename: str,
        purpose: str = "retrieval",
    ) -> FileCreateResponse:
        """Create a file

        Args:
            file (bytes): The file to upload
            filename (str): The name of the file
            purpose (str, optional): The purpose of the file. Defaults to "fine-tune".

        Returns:
            FileCreateResponse: The response from the API
        """
        resp = self.client.post(
            url=f"{self.url_path}/upload",
            files={"file": (filename, file, "application/octet-stream")},  # to be confirmed
            params={"purpose": purpose},
        )

        return FileCreateResponse(**resp.json())

    def list(self, purpose: str = "retrieval") -> FileListResponse:
        """List files

        Returns:
            FileListResponse: The response from the API
        """
        resp = self.client.get(url=f"{self.url_path}/list", params={"purpose": purpose})

        return FileListResponse(**resp.json())

    def retrieve(self, file_id: int) -> FileRetriveResponse:
        """Retrieve a file

        Args:
            file_id (int): The ID of the file to retrieve

        Returns:
            FileRetriveResponse: The response from the API
        """
        resp = self.client.get(
            url=f"{self.url_path}/retrieve", params={"file_id": file_id}
        )

        return FileRetriveResponse(**resp.json())

    def retrieve_content(self, file_id: int) -> FileRetrieveContentResponse:
        """Retrieve the content of a file

        Args:
            file_id (int): The ID of the file to retrieve the content of

        Returns:
            FileRetrieveContentResponse: The response from the API
        """
        resp = self.client.get(
            url=f"{self.url_path}/retrieve_content", params={"file_id": file_id}
        )

        return FileRetrieveContentResponse(**resp.json())  # to be confirmed

    def delete(self, file_id: int) -> FileDeleteResponse:
        """Delete a file

        Args:
            file_id (int): The ID of the file to delete

        Returns:
            FileDeleteResponse: The response from the API
        """
        resp = self.client.post(f"{self.url_path}/delete", json={"file_id": file_id})

        return FileDeleteResponse(**resp.json())


class AsyncFiles(BaseAsyncInterface, Files):
    """Asynchronous Files interface"""

    async def create(
        self, *, file: bytes, filename: str, purpose: str = "fine-tune"
    ) -> FileCreateResponse:
        """Create a file"""
        return super().create(file=file, filename=filename, purpose=purpose)

    async def list(self) -> FileListResponse:
        """List files"""
        return super().list()

    async def retrieve(self, file_id: int) -> FileRetriveResponse:
        """Retrieve a file"""
        return super().retrieve(file_id=file_id)

    async def retrieve_content(self, file_id: int) -> FileRetrieveContentResponse:
        """Retrieve the content of a file"""
        return super().retrieve_content(file_id=file_id)

    async def delete(self, file_id: int) -> FileDeleteResponse:
        """Delete a file"""
        return super().delete(file_id=file_id)
