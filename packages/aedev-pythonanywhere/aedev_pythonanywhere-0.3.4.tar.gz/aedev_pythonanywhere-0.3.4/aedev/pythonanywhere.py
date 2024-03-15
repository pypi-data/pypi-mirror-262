""" web api for www.pyanywhere.com and eu.pyanywhere.com


a similar package can be found at `https://gitlab.com/texperience/pythonanywhereapiclient`__
"""
import os
import time
from fnmatch import fnmatchcase
from functools import partial

import requests

from typing import Any, Callable, Optional, Sequence, Union, cast

from ae.base import DOCS_FOLDER, PY_CACHE_FOLDER, PY_INIT, TESTS_FOLDER                 # type: ignore
from ae.paths import Collector, SearcherRetType, coll_items                             # type: ignore
from aedev.setup_project import code_version                                            # type: ignore


__version__ = '0.3.4'


SKIP_ROOT_FOLDERS = (DOCS_FOLDER, '.git', '.idea', 'media', 'media_ini', 'static', TESTS_FOLDER)
""" root folders on the web server that will skipped on search of deployed project package files. """


class PythonanywhereApi:
    """ remote host api to a project package on the web hosts eu.pythonanywhere.com and pythonanywhere.com. """

    def __init__(self, web_domain: str, web_user: str, web_token: str, project_name: str):
        """ initialize web host api and the deployed project package name.

        :param web_domain:      remote web host domain.
        :param web_user:        remote connection username.
        :param web_token:       personal user credential token string on remote host.
        :param project_name:    name of the web project package.
        """
        self.base_url = f"https://{web_domain}/api/v0/user/{web_user}/"
        self.consoles_url_part = "consoles/"
        self.protocol_headers = {'Authorization': f"Token {web_token}"}

        # self.web_domain = web_domain
        self.web_user = web_user
        # self.web_token = web_token

        self._err_msg = ""
        self.project_name = self._project_name = project_name
        self.skip_enter_folder = lambda item_info: False

    @property
    def error_message(self) -> str:
        """ error message string if an error occurred or an empty string if not.

        :getter:                return the accumulated error message of the recently occurred error(s).
        :setter:                any assigned error message will be accumulated to the recently error messages.
                                pass an empty string to reset the error message.
        """
        return self._err_msg

    @error_message.setter
    def error_message(self, next_err_msg: str):
        if next_err_msg:
            self._err_msg = (self._err_msg + '\n\n' if self._err_msg else "") + next_err_msg
        else:
            self._err_msg = ""

    @property
    def project_name(self) -> str:
        """ project main package name string property.

        :getter:                return the currently connected/configured project package name of the web host server.
        :setter:                set/change the currently connected/configured project name of the web host server.
        """
        return self._project_name

    @project_name.setter
    def project_name(self, project_name: str):
        self.pkg_files_url_part = f"files/path/home/{self.web_user}/{project_name}/"
        self._project_name = project_name

    def _folder_items(self, folder_path: str) -> Optional[list[dict[str, str]]]:
        url_path = self.pkg_files_url_part
        if folder_path:
            url_path += folder_path + '/'

        response = self._request(url_path, f"fetching files in folder {folder_path}")
        if not self.error_message:
            found_file_infos = cast(Optional[dict[str, dict[str, Any]]], self._from_json(response))
            if found_file_infos is not None:        # == not self.error_message:
                return [{'file_path': os.path.join(folder_path, _name), 'type': _info['type']}
                        for _name, _info in found_file_infos.items()]

        if response.status_code == 404:
            self.error_message = ""         # if folder not exists, do not propagate 404:Not Found errors

        return None

    def _from_json(self, response: requests.Response) -> Optional[Union[list[dict[str, Any]],
                                                                        dict[str, dict[str, Any]]]]:
        """ convert json in response to python type (list/dict).

        :param response:        response from requests to convert into python data type.
        :return:                [list of] dictionaries converted from the response content or None on error.
        """
        try:
            return response.json()
        except Exception as exc:  # requests.exceptions.JSONDecodeError
            self.error_message = f"{exc} in response.json() call on response content '{response.content!r}'"
            return None

    def _prepare_collector(self, skipper):
        def _sel(file_path: str):
            return not skipper(file_path)

        def _det(file_path: str):
            return os.path.splitext(file_path)[1]

        self.skip_enter_folder = lambda file_path: skipper(file_path)

        return partial(coll_items, searcher=self.files_iterator, selector=_sel, type_detector=_det)

    def _request(self, url_path: str, task: str, method: Callable = requests.get, success_codes: Sequence = (200, 201),
                 **request_kwargs) -> requests.Response:
        """ send a https request specified via :paramref:`.method` and return the response.

        :param url_path:        sub url path to send request to.
        :param task:            string describing the task to archive (used to compile an error message).
        :param method:          requests method (get, post, push, delete, patch, ...).
        :param success_codes:   sequence of response.status_code success codes
        :param request_kwargs:  additional request method arguments.
        :return:                request response. if on error occurred then the instance string attribute
                                :attr:`.error_message` contains an error message. if the caller is not checking for
                                errors and not resetting the error message string, then this function will accumulate
                                further errors to :attr:`.error_message`, separated by two new line characters.
        """
        while True:
            response = method(f"{self.base_url}{url_path}", headers=self.protocol_headers, **request_kwargs)
            if response.status_code != 429:     # too many requests per minute against host api
                break
            time.sleep(12)

        if response.status_code in success_codes:
            self.error_message = ""
        else:
            self.error_message = (f"request error '{response.status_code}:{response.reason}'"
                                  f" {task} via '{self.base_url}{url_path}'")

        return response

    def available_consoles(self) -> Optional[list[dict[str, Any]]]:
        """ determine the available consoles.

        :return:                python dictionary with available consoles or None if an error occurred.
        """
        response = self._request(self.consoles_url_part, "get list of consoles")
        if self.error_message:
            return None
        return cast(Optional[list[dict[str, Any]]], self._from_json(response))

    def deployed_code_files(self, root_item_masks: Sequence[str], lean: bool = False) -> Optional[set[str]]:
        """ determine all deployed code files of given package name deployed to the pythonanywhere server.

        :param root_item_masks: root package paths with glob wildcards to collect deployed code files from.
        :param lean:            pass True to additionally exclude repository files that are not needed on the web
                                production server like e.g. the gettext '.po' files, the 'media_ini' root folder,
                                and the 'static' sub-folder with the initial static files of the web project.
        :return:                set of file paths of the package deployed on the web, relative to the project root
                                or None if an error occurred.
        """
        skip_file_path = self.web_lean_file_exclude if lean else self.web_file_exclude
        collector = Collector(item_collector=self._prepare_collector(skip_file_path))
        for item_mask in root_item_masks:
            if self.find_project_files(item_mask, collector=collector, skip_file_path=skip_file_path) is None:
                return None
        return set(collector.files)

    def deployed_file_content(self, file_path: str) -> Optional[bytes]:
        """ determine the file content of a file deployed to a web server.

        :param file_path:       path of a deployed file relative to the project root.
        :return:                file content as bytes or None if error occurred (check self.error_message).
        """
        response = self._request(self.pkg_files_url_part + file_path, "fetching file content")
        if self.error_message:
            return None
        return response.content

    def deployed_version(self) -> str:
        """ determine the version of a deployed django project package.

        :return:                version string of the package deployed to the web host/server
                                or empty string if package version file or version-in-file not found.
        """
        init_file_content = self.deployed_file_content(os.path.join(self.project_name, PY_INIT))
        return "" if init_file_content is None else code_version(init_file_content)

    def deploy_file(self, file_path: str, file_content: bytes) -> str:
        """ add or update a project file to the web server.

        :param file_path:       path relative to the project root of the file to be deployed (added or updated).
        :param file_content:    file content to deploy/upload.
        :return:                error message if update/add failed else on success an empty string.
        """
        self._request(self.pkg_files_url_part + file_path, f"deploy file {file_path}", method=requests.post,
                      files={'content': file_content})
        return self.error_message

    def delete_file_or_folder(self, file_path: str) -> str:
        """ delete a file or folder on the web server.

        :param file_path:       path relative to the project root of the file to be deleted.
        :return:                error message if deletion failed else on success an empty string.
        """
        self._request(self.pkg_files_url_part + file_path, f"deleting file {file_path}", method=requests.delete,
                      success_codes=(204, ))
        return self.error_message

    def files_iterator(self, file_mask: str, level_index: int = 0) -> SearcherRetType:
        """ find files matching the path mask string passed as the paramref:`.file_mask` argument.

        :param file_mask:       file path pattern/mask with optional wildcards. passing an empty string will return
                                the files of the project/package root directory, as well as passing '.' or '*'.
                                also absolute path masks will be relative to the project root directory. file path mask
                                matches are case-sensitive (done with the function :func:`fnmatch.fnmatchcase`).
        :param level_index:     folder level depth in :paramref:`passed file path mask <files_iterator.file_mask>`
                                to start searching (only specified in recursive call).
        :return:                iterator/generator yielding dicts. each dict has a `file_path` key containing the
                                path string of the found file relative to the project root folder and a `type` key
                                containing the string `'directory'` or `'file'
        """
        if file_mask.startswith('/'):
            file_mask = file_mask[1:]
        if file_mask in ('', '.') or file_mask.endswith('/.'):
            file_mask = file_mask[:-1] + '*'    # ae_paths.normalize() is converting empty mask string into '-'
        mask_parts = file_mask.split('/')
        level_count = len(mask_parts)

        while level_index < level_count and '*' not in mask_parts[level_index] and '?' not in mask_parts[level_index]:
            level_index += 1
        if level_index == level_count:          # no wildcards found
            match_index = level_count - 1
            deep_search = False
            file_pattern = mask_parts[-1]
        else:
            match_index = level_index
            deep_search = mask_parts[level_index] == '**'
            if deep_search:
                level_index += 1
            file_pattern = mask_parts[level_index] if level_index < level_count else '*'

        file_infos = self._folder_items('/'.join(mask_parts[:match_index]))
        for file_info in file_infos or ():
            item_path, is_folder = file_info['file_path'], file_info['type'] == 'directory'
            item_name = os.path.basename(item_path)
            matched = fnmatchcase(item_name, file_pattern)
            assert not matched or item_path == '/'.join(mask_parts[:match_index] + [item_name])

            if matched and not is_folder and level_index + 1 >= level_count:
                yield item_path

            elif (matched or deep_search) and is_folder and match_index + int(matched) - int(deep_search) < level_count:
                if not self.skip_enter_folder(item_path + '/.'):
                    deep_parts = (mask_parts[:match_index] + [item_name]     # == file_path == only-folders-path
                                  + (['**'] if deep_search and (not matched or file_pattern in ('*', '**')) else [])
                                  + mask_parts[level_index + int(matched):])
                    yield from self.files_iterator('/'.join(deep_parts), level_index=match_index + 1)
        return None

    def find_project_files(self, file_mask: str = '',
                           skip_file_path: Callable[[str], bool] = lambda _: False,
                           collector: Optional[Collector] = None,
                           ) -> Optional[set[str]]:
        """ determine the files matching the glob pattern provided in :paramref:`.file_mask` at the app/web server.

        not using the files tree api endpoints/function (f"files/tree/?path=/home/{self.web_user}/{project_name}")
        because their response is limited to 1000 files
        (see https://help.pythonanywhere.com/pages/API#apiv0userusernamefilestreepathpath) and e.g. kairos has more
        than 5300 files in its package folder (mainly for django filer and the static files).

        :param file_mask:       file mask including relative path to the package project root to be searched.
                                passing an empty string (the default) returns all files in the package root directory.
        :param collector:       file collector callable.
        :param skip_file_path:  called for each found file with the file_mask relative to the package root folder
                                as argument, returning True to exclude the specified file from the returned result set.
                                you may use :meth:`.web_file_exclude` and :meth:`.web_lean_file_exclude` or an extended
                                callable from these two methods.
        :return:                set of file paths of the package deployed on the web, relative to the project root
                                or None if an error occurred. all files underneath a
        """
        if not collector:
            collector = Collector(item_collector=self._prepare_collector(skip_file_path))

        collector.collect(file_mask)
        return None if self.error_message else set(collector.files)

    def web_file_exclude(self, file_path: str) -> bool:
        """ default file exclude callback used by `meth:`.deployed_code_files` to call :meth:`.find_project_files`.

        :param file_path:       path to file to check for exclusion, relative to the project root folder.
        :return:                True if the file specified in :paramref:`.rel_file_path` has to excluded, else False.
        """
        parts = file_path.split('/')
        return (
                PY_CACHE_FOLDER in parts
                or 'migrations' in parts
                or parts[0] in SKIP_ROOT_FOLDERS
                or parts[0] == self.project_name and len(parts) > 1 and parts[1] == 'static'
                )

    def web_lean_file_exclude(self, file_path: str) -> bool:
        """ lean file exclude callback used by `meth:`.deployed_code_files` to call :meth:`.find_project_files`.

        :param file_path:       path to file to check for exclusion, relative to the project root folder.
        :return:                True if the file specified in :paramref:`.rel_file_path` has to excluded, else False.
        """
        return (self.web_file_exclude(file_path)
                or os.path.splitext(file_path)[1] == '.po'
                or '/' not in file_path and ('db' in file_path.split('.')        # 'db.sqlite', 'project.db', ...
                                             or file_path != 'manage.py')
                )
