from script_house.utils import JsonUtils
import requests

from ..common.base import BaseAPICall
from ..common.entity import Archive, Category


class ArchiveAPI(BaseAPICall):
    def get_archive_metadata(self, id: str) -> Archive:
        """
        Get Metadata (title, tags) for a given Archive.
        :param id: ID of the Archive to process.
        :return:
        """
        resp = requests.get(f"{self.server}/api/archives/{id}/metadata", params={'key': self.key},
                            headers=self.build_headers())
        return JsonUtils.to_obj(resp.text, Archive)

    def get_all_archives(self) -> list[Archive]:
        resp = requests.get(f"{self.server}/api/archives", params={'key': self.key}, headers=self.build_headers())
        list = JsonUtils.to_obj(resp.text)
        return [JsonUtils.to_obj(JsonUtils.to_str(o), Archive) for o in list]

    def get_archive_categories(self, id: str) -> list[Category]:
        """
        Get all the Categories which currently refer to this Archive ID.
        :param id: ID of the Archive to process.
        :return:
        """
        resp = requests.get(f"{self.server}/api/archives/{id}/categories", params={'key': self.key},
                            headers=self.build_headers())
        clist = JsonUtils.to_obj(resp.text)["categories"]
        return [JsonUtils.to_obj(JsonUtils.to_str(c), Category) for c in clist]

    def update_archive_metadata(self, id: str, archive: Archive) -> bool:
        """
        Update tags and title for the given Archive. Data supplied to the server through
        this method will <b>overwrite</b> the previous data.
        :param archive: the Archive whose tags and title will be updated
        :param id: ID of the Archive to process.
        :return: whether update succeeds
        """
        resp = requests.put(f"{self.server}/api/archives/{id}/metadata", params={
            'key': self.key,
            'title': archive.title,
            'tags': archive.tags
        }, headers=self.build_headers())
        return resp.status_code == 200
