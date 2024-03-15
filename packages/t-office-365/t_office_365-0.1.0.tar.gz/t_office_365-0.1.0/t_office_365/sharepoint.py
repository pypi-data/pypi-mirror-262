"""SharePoint class."""
import json
import os

import requests
from O365 import Account
from retry import retry

from t_office_365.endpoints import SharepointEndpoints
from t_office_365.exceptions import (
    UnexpectedError,
    ServiceUnavailableError,
    AssetLockedError,
    AssetNotFoundError,
    BadRequestError,
    AuthenticationGraphError,
)


class SharepointSite:
    """Represents a SharePoint site in Microsoft Office 365."""

    def __init__(self, account: Account, site_name: str) -> None:
        """
        Initializes instance of the SharepointService class.

        :param:
        - account: The account object containing the authentication information.
        - site_name: The name of microsoft office site.
        """
        self.endpoints = SharepointEndpoints(account)
        self.__set_drive_id(site_name)

    def download_file_by_path(self, file_path: str, target_folder: str) -> str or bytes:
        """
        Download a file from SharePoint to the specified target folder.

        :param:
        - file_path (str): The path to the file to be downloaded.
        - target_folder (str): The path to the folder where the file should be downloaded.

        :return:
        - str: The path to the file to be downloaded

        :raise:
        - If there is an issue with file path which is downloaded.
        """
        self.__check_path(target_folder)
        folder_id = self.__get_folder_id(os.path.dirname(file_path))
        return self.__get_folder_contents(
            self.endpoints.folder_items_endpoint.format(folder_id=folder_id), os.path.basename(file_path), target_folder
        )

    def download_file_by_id(self, file_id: str, file_name: str, target_folder: str) -> str or bytes:
        """
        Download a file from SharePoint with file ID and save it to the target folder.

        :param:
        - file_id: The ID of file which want to download.
        - file_name : The name to be used which saving the downloaded file.
        - target_folder : The folder where the file should be saved.

        :return:
        - The file path of the to be downloaded.

        :return:
        The full path to the downloaded file.
        """
        self.__check_path(target_folder)
        result = requests.get(self.endpoints.file_id_endpoint.format(file_id=file_id), headers=self.endpoints.headers)
        self.__check_result(result, f"{file_id}")
        file_path = os.path.join(target_folder, file_name)
        with open(file_path, "wb") as w:
            w.write(result.content)
        return file_path

    def does_file_exists_by_path(self, file_path: str) -> bool:
        """
        Check if a file exists in SharePoint.

        :param:
        - file_path (str): The path to the file which should be checked.

        :return:
        - bool: True if the file exists, False otherwise..
        """
        try:
            folder_id = self.__get_folder_id(os.path.dirname(file_path))
            self.__check_file_exist(
                self.endpoints.folder_items_endpoint.format(folder_id=folder_id), os.path.basename(file_path)
            )
        except AssetNotFoundError:
            return False
        return True

    def does_file_exists_by_id(self, file_id: str) -> bool:
        """
        Check if a file exists in SharePoint based on file ID.

        :param:
         - file_id (str):The ID of the file.

        :return: bool
            True if the file exists, False otherwise.

        :raises BadRequestError:
            If there is an issue with the request.
        """
        result = requests.get(self.endpoints.file_id_endpoint.format(file_id=file_id), headers=self.endpoints.headers)
        try:
            self.__check_result(result, file_id)
        except BadRequestError:
            return False
        return True

    def upload_file(self, file_path: str, folder_path: str) -> None:
        """
        Uploads a file to SharePoint, with handling both small and large uploads.

        :param:
        - file_path (str): The file path to be uploaded.
                - folder_path (str): The SharePoint folder path where the file should be uploaded.

        :raises:
            - AssetNotFoundError: If the file does not exist in SharePoint.
        """
        st = os.stat(file_path)
        size = st.st_size
        folder_id = self.__get_folder_id(folder_path)
        path_url = self.endpoints.encode_url(f"{folder_path}") + f"/{os.path.basename(file_path)}"
        if size / (1024 * 1024) < 4:
            result = requests.get(
                self.endpoints.file_info_endpoint.format(file_path=path_url), headers=self.endpoints.headers
            )
            try:
                self.__check_result(result, file_path)
                file_info = result.json()
                self.__upload_existing_file_by_id(file_path, file_info["id"])
            except AssetNotFoundError:
                # file does not exist, create a new item
                self.__upload_not_existing_file_by_folder_id(file_path, os.path.basename(file_path), folder_id)
        else:
            self.__upload_large_file(file_path, os.path.basename(file_path), folder_id, size)

    def delete_file(self, file_id: str) -> None:
        """
        Delete a file from the drive by file id.

        :param
        - file_id (str): The ID of the file to be deleted.

        :raises:
        - BadRequestError: If there is an issue with the request.
        """
        result = requests.delete(
            self.endpoints.file_id_endpoint.format(file_id=file_id), headers=self.endpoints.headers
        )
        self.__check_result(result, file_id)

    def get_or_create_folder(self, file_path: str, folder_name: str):
        """
         Get or create a folder on SharePoint.

        :param:
        - file_path: The file path used to derive the SharePoint folder path.
        - folder_name:The name of the folder to be created.

        :return:
        - The ID of the existing or newly created folder.

        :raises:
        - AssetNotFoundError: If there is an error during the folder retrieval.
        """
        try:
            folder_id = self.__get_folder_id(os.path.dirname(file_path))
            return folder_id
        except AssetNotFoundError:
            folder_data = {
                "name": folder_name,
                "folder": {"description": "This is a new folder"},
                "@microsoft.graph.conflictBehavior": "rename",
            }

            result = requests.put(
                self.endpoints.folder_id_endpoint.format(folder_path=folder_name),
                headers=self.endpoints.headers,
                data=json.dumps(folder_data),
            )
            self.__check_result(result, folder_name)

    @retry(exceptions=(BadRequestError, UnexpectedError), tries=3, delay=3, backoff=2)
    def __set_drive_id(self, site_name) -> None:
        """
        Set the Drive ID for SharePoint.

        :param:
        - site_name (str): The name of the site.

        :return:
        - str: The ID of the SharePoint Drive.
        """
        endpoint = self.endpoints.drive_id_endpoint(site_name)
        result = requests.get(endpoint, headers=self.endpoints.headers)
        self.__check_result(result, endpoint)
        self.endpoints.drive_id = result.json()["id"]

    @retry(exceptions=(BadRequestError, UnexpectedError), tries=3, delay=3, backoff=2)
    def __get_folder_id(self, folder_path: str) -> str:
        """
        Get the Folder ID from SharePoint.

        :param:
        - folder_path (str): The folder path for retrieving folder information.

        :return:
        - str: The ID of the SharePoint folder.

        :raise:
        - If there is an error during the Folder ID retrieval.
        """
        folder_endpoint = self.endpoints.folder_id_endpoint.format(folder_path=self.endpoints.encode_url(folder_path))
        result = requests.get(folder_endpoint, headers=self.endpoints.headers)
        self.__check_result(result, f"{folder_path}")
        return result.json()["id"]

    @retry(exceptions=(BadRequestError, UnexpectedError), tries=3, delay=3, backoff=2)
    def __get_folder_contents(self, folder_items_endpoint: str, file_name: str, target_folder: str) -> str or bytes:
        """
        Get folder contents from SharePoint and download a specific file if found.

        :param:
        - folder_items_endpoint (str): The endpoint for retrieving folder items.
        - file_name (str): The name of the file to be searched and downloaded.
        - target_folder (str): The local directory where the file should be downloaded.

        :return:
        - The downloaded file content if the file is found.

        :raise:
        - If the specified file is not found within the folder.
        """
        self.__check_path(target_folder)
        result = requests.get(folder_items_endpoint, headers=self.endpoints.headers)
        result.raise_for_status()
        children = result.json()["value"]
        for item in children:
            if str(item["name"]).lower() == file_name.lower():
                return self.__download_file(item["id"], file_name, target_folder)
        else:
            raise AssetNotFoundError(f"'{file_name}' not found!")

    def __download_file(self, file_id: str, file_name: str, target_folder: str) -> str:
        """
        Download a file from SharePoint.

        :param:
        - file_id (str): The ID of the file to be downloaded.
        - file_name(str): The name of the file to be used when saving locally.
        - target_folder(str): The local directory where the file should be downloaded.

        :return:
        - The local file path where the downloaded file is saved.
        """
        self.__check_path(target_folder)
        result = requests.get(
            self.endpoints.file_content_endpoint.format(file_id=file_id), headers=self.endpoints.headers
        )
        result.raise_for_status()
        file_path = os.path.join(target_folder, file_name)
        with open(file_path, "wb") as w:
            w.write(result.content)
        return file_path

    def __check_file_exist(self, folder_items_endpoint: str, file_name: str) -> None:
        """
        Check if a file exists in a SharePoint folder.

        :param:
        - folder_items_endpoint (str): The endpoint URL for retrieving folder items in SharePoint.
        - file_name (str): The name of the file to check for existence.

        :return:
        - bool: True if the file exists, False otherwise.

        :raise:
        - AssetNotFoundError: if the file does not exist on SharePoint.
        """
        result = requests.get(folder_items_endpoint, headers=self.endpoints.headers)
        self.__check_result(result, file_name)
        children = result.json()["value"]
        for item in children:
            if str(item["name"]).lower() == file_name.lower():
                return
        else:
            raise AssetNotFoundError(f"'{file_name}' not found!")

    def __upload_existing_file_by_id(self, file_path: str, file_id: str) -> None:
        """
        Uploads an existing file to SharePoint with file id.

        :param:
        - file_path (str): The file path of the existing file to be uploaded.
        - file_id (str): The SharePoint file to which the upload will be performed.

        :raise:
        - If the file is locked on the SharePoint.
        """
        result = requests.put(
            self.endpoints.file_content_endpoint.format(file_id=file_id),
            headers={"Authorization": "Bearer " + self.endpoints.access_token, "Content-type": "application/binary"},
            data=open(file_path, "rb").read(),
        )
        self.__check_result(result, f"{file_path}/{file_id}")

    def __upload_not_existing_file_by_folder_id(self, file_path: str, file_name: str, folder_id: str) -> None:
        """
        Uploads a file to SharePoint within a specified folder using the folder.

        :param:
        - file_path (str): The  file path of the file to be uploaded.
        - file_name (str): The name of the file to be uploaded.
        - folder_id (str): The SharePoint  folder where the file will be uploaded.

        :raise:
        - If there is an error uploading the file to the SharePoint
        """
        result = requests.put(
            self.endpoints.file_content_by_url_endpoint.format(
                folder_id=folder_id, file_url=self.endpoints.encode_url(file_name)
            ),
            headers={"Authorization": "Bearer " + self.endpoints.access_token, "Content-type": "application/binary"},
            data=open(file_path, "rb").read(),
        )
        self.__check_result(result, file_name)

    def __upload_large_file(self, file_path: str, file_name: str, folder_id: str, size: int) -> None:
        """
        Uploads a large file to SharePoint using the Microsoft Graph api resumable upload session.

        :param:
        - file_path (str): The file path of the large file to be uploaded.
        - file_name (str): The name to be assigned to the file on SharePoint.
        - folder_id (str): The SharePoint folder where the file will be uploaded.
        - size (int): The size of the file in bytes.

        :raise:
        - If there is an error while Uploading the large file.
        """
        result = requests.post(
            self.endpoints.file_upload_session_endpoint.format(
                folder_id=folder_id, file_url=self.endpoints.encode_url(file_name)
            ),
            headers=self.endpoints.headers,
            json={
                "@microsoft.graph.conflictBehavior": "replace",
                "description": "A large file",
                "fileSystemInfo": {"@odata.type": "microsoft.graph.fileSystemInfo"},
                "name": file_path,
            },
        )
        self.__check_result(result)
        upload_url = result.json()["uploadUrl"]

        chunks = int(size / self.endpoints.file_chunk_size) + 1 if size % self.endpoints.file_chunk_size > 0 else 0
        with open(file_path, "rb") as fd:
            start = 0
            for chunk_num in range(chunks):
                chunk = fd.read(self.endpoints.file_chunk_size)
                bytes_read = len(chunk)
                upload_range = f"bytes {start}-{start + bytes_read - 1}/{size}"
                upload_result = requests.put(
                    upload_url, headers={"Content-Length": str(bytes_read), "Content-Range": upload_range}, data=chunk
                )
                self.__check_result(upload_result, upload_url)
                start += bytes_read

    @staticmethod
    def __check_result(result, asset: str = ""):
        """
        Checks the HTTP status code of a request result and raises specific exceptions based on common error codes.

        :param:
        - result: The result of an HTTP request (response object).
        - asset: Optional. The asset associated with the request, used for error messages.

        :raises:
         - AuthenticationGraphError: If the status code is 401.
         - AssetLockedError: If the status code is 423, with a message indicating the asset is locked.
         - BadRequestError: If the status code is 400, with a message indicating processing failure for the asset.
         - AssetNotFoundError: If the status code is 404, with a message indicating the asset was not found.
         - ServiceUnavailableError: If the status code is 503.
         - UnexpectedError: If the status code is not 200, with a generic error message.
        """
        status_code = result.status_code

        status_code_exceptions_map = {
            401: AuthenticationGraphError,
            423: AssetLockedError(f"Asset '{asset}' locked!"),
            400: BadRequestError(f"Unable to process: '{asset}'"),
            404: AssetNotFoundError(f"Asset '{asset}' not found!"),
            503: ServiceUnavailableError,
        }
        ex = status_code_exceptions_map.get(status_code, None)
        if ex:
            raise ex
        if status_code != 200:
            raise UnexpectedError(f'An unexpected error while processing asset "{asset}". (Status code {status_code})')

        result.raise_for_status()

    @staticmethod
    def __check_path(path):
        """
        Check if the given path exists as a directory.

        :param:
            - path (str): The path to be checked.

        :raise:
            AssetNotFoundError: If the path does not exist as a directory.
        """
        if not os.path.isdir(path):
            raise AssetNotFoundError(f"No such directory: '{path}'")


class Sharepoint:
    """SharePoint class is used for API calls to SharePoint."""

    def __init__(self, account: Account) -> None:
        """
        Initializes an instance of the Sharepoint class.

        :param:
         - account: The account object containing the authentication information.
        """
        self.account = account

    def site(self, site_name: str) -> SharepointSite:
        """
        Get a SharePoint site by its name.

        :param:
        - site_name: The name of the SharePoint site.

        :return:
        - A SharepointSite object representing the specified SharePoint site.
        """
        return SharepointSite(self.account, site_name)
