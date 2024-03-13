from ..utils import *
import zlib


class FileProxy:

    def __init__(self, access_token):
        self.access_token = access_token

    def get_file(self, institution: str, collection: str, asset_guid: str, file_name: str):
        res = send_request_to_file_proxy(
            RequestMethod.GET,
            self.access_token,
            f"/assetfiles/{institution}/{collection}/{asset_guid}/{file_name}")
        return res

    def upload(self, file_path, institution: str, collection: str, asset_guid: str):
        file = open(file_path, 'rb')

        file_data = file.read()

        file.close()

        # Calculate checksum
        crc = zlib.crc32(file_data)

        res = send_request_to_file_proxy(
            RequestMethod.PUT,
            self.access_token,
            f"/assetfiles/{institution}/{collection}/{asset_guid}/{file.name}?crc={crc}&file_size_mb=1",
            data=file_data)
        return res

    def list_available_files(self, asset_guid):
        res = send_request_to_file_proxy(
            RequestMethod.GET,
            self.access_token,
            f"/assetfiles/test-institution/test-collection/{asset_guid}")
        return res

    def list_file_info(self, asset_guid: str):
        res = send_request_to_file_proxy(
            RequestMethod.DELETE,
            self.access_token,
            f"/assets/{asset_guid}/files")
        return res

    def delete_file(self, institution: str, collection: str, asset_guid: str, file_name: str):
        res = send_request_to_file_proxy(
            RequestMethod.DELETE,
            self.access_token,
            f"/assetfiles/{institution}/{collection}/{asset_guid}/{file_name}")
        return res

    def synchronize_erda(self, asset_guid):
        res = send_request_to_file_proxy(
            RequestMethod.POST,
            self.access_token,
            f"/shares/assets/{asset_guid}/synchronize"
        )
        return res

    def open_share(self, institution, collection, asset_guid, users: list, allocation_mb: int):
        body = {
            "assets": [{
                "asset_guid": asset_guid,
                "institution": institution,
                "collection": collection
            }],
            "users": users,
            "allocation_mb": allocation_mb
        }
        res = send_request_to_file_proxy(
            RequestMethod.POST,
            self.access_token,
            f"/shares/assets/{asset_guid}/createShare",
            body
        )
        return res

    def delete_share(self, institution, collection, asset_guid, users: list, allocation_mb: int):
        body = {
            "assets": [{
                "asset_guid": asset_guid,
                "institution": institution,
                "collection": collection
            }],
            "users": users,
            "allocation_mb": allocation_mb
        }
        res = send_request_to_file_proxy(
            RequestMethod.DELETE,
            self.access_token,
            f"/shares/assets/{asset_guid}/deleteShare",
            body
        )
        return res

    def change_allocation(self, asset_guid: str, new_allocation_mb: int):
        body = {
            "asset_guid": asset_guid,
            "new_allocation_mb": new_allocation_mb
        }

        res = send_request_to_file_proxy(
            RequestMethod.POST,
            self.access_token,
            f"/shares/assets/{asset_guid}/changeAllocation",
            data=body
        )
        return res
