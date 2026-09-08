from dataclasses import dataclass
import os
from typing import Optional

import yaml


__ALLOWED_EXTENSIONS = {'yml', 'yaml'}


@dataclass
class ReleaseVersion:
    version: str
    title: str
    url_prefix: str
    columns: list[str]
    artifacts: list[str]

    def __post_init__(self):
        if isinstance(self.columns, str):
            # PyChram says the code is unreachable, but it always hits...
            self.columns = self.columns.split(";")


def _load_downloads_file(file_path: str, ignore_errors: bool = False) -> list[ReleaseVersion]:
    loaded_releases = list()

    with open(file_path, 'r') as f:
        if file_path.split(".")[-1] in __ALLOWED_EXTENSIONS:
            raw_release_data = yaml.safe_load(f)["downloads"]
        else:
            return loaded_releases

    for raw_release_entry in raw_release_data:
        # noinspection PyBroadException
        try:
            loaded_releases.append(ReleaseVersion(**raw_release_entry))
        except Exception:
            if not ignore_errors:
                raise

    return loaded_releases


def _load_downloads_folder(folder_path, ignore_errors: bool = False) -> dict[str, list[ReleaseVersion]]:
    loaded_releases = dict()

    for downloads_file in os.listdir(folder_path):
        if downloads_file.split(".")[-1] not in __ALLOWED_EXTENSIONS:
            continue

        _downloads_list = _load_downloads_file(os.path.join(folder_path, downloads_file), ignore_errors=ignore_errors)

        loaded_releases[downloads_file.split(".")[0]] = _downloads_list

    return loaded_releases


class ReleaseVersionRepository:
    __downloads_data: dict[str, list[ReleaseVersion]]

    def __init__(self):
        self.__downloads_data = dict()

    def load_folder(self, folder_path, ignore_errors: bool = False, overwrite: bool = False):
        self.__downloads_data = _load_downloads_folder(folder_path=folder_path, ignore_errors=ignore_errors)

    def get_all_releases(self) -> dict[str, list[ReleaseVersion]]:
        return self.__downloads_data

    def get_releases_for(self, product: str) -> Optional[list[ReleaseVersion]]:
        """

        :rtype: Optional[list[ReleaseVersion]]
        """
        return self.__downloads_data[product]

    def get_latest_releases_for(self, product: str) -> Optional[ReleaseVersion]:
        return self.__downloads_data[product][0]
