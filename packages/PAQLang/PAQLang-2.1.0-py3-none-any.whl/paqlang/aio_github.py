import logging
import re
import urllib
import codecs
import os
import base64
import datetime

import httpx
import chardet

logger = logging.getLogger(__name__)


class GithubAsync:

    project = None

    async def httpx_get(self, url, raw=False):
        # logger.info(f'get: {url}')
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{url}", headers={"Authorization": f"Bearer {self.token}"}
                )
                # Если код возврата, ошибка, то поднять ошибку
                response.raise_for_status()
                if raw:
                    return response.content
                else:
                    return response.json()
            except httpx.HTTPError as exc:
                # Не поднимать ошибку, если нет доступа к teams
                logger.error(
                    f'HTTP Exception for "{exc.request.url}" - "{exc}"'
                )
                raise

    async def build_url(self, resources, **kwargs):
        url = []
        # Список проектов
        url += ["/users" if resources.get("users") else ""]
        url += ["/repos" if resources.get("repos") else ""]
        url += [f"/{resources.get('owner')}" if resources.get("owner") else ""]
        url += ["/repos" if resources.get("repos2") else ""]
        url += [f"/{resources.get('repo')}" if resources.get("repo") else ""]
        url += ["/branches" if resources.get("branches") else ""]
        url += [
            f"/{resources.get('search')}" if resources.get("search") else ""
        ]
        url += ["/git/trees" if resources.get("trees") else ""]
        url += [
            (
                f"/git/trees/{resources.get('tree')}"
                if resources.get("tree")
                else ""
            )
        ]
        url += [
            (
                f"/contents/{resources.get('contents')}"
                if resources.get("contents")
                else ""
            )
        ]
        url += ["/tags" if resources.get("tags") else ""]
        url += ["/commits" if resources.get("commits") else ""]
        url += [
            (
                f"/commits/{resources.get('commit_sha')}"
                if resources.get("commit_sha")
                else ""
            )
        ]
        # Получить параметры api, None не включать
        kwargs2 = urllib.parse.urlencode(
            {key: value for key, value in kwargs.items() if value is not None}
        )
        parameters = f"{kwargs2}"
        # Сформировать url строку запроса
        url_string = f"{self.url}{''.join(url)}"
        # Вернуть строку запроса с параметрами
        url = f"{url_string}?{parameters}" if parameters else url_string
        return url

    async def set_project(self, owner, token, name):
        """Найти проект в репозитории и запомнить в классе

        :param str url: путь к gitlab
        :param str token: токен
        :param str name: имя репозитория
        """
        self.url = "https://api.github.com"
        self.owner = owner
        self.token = token

    async def get_httpx(self, resources, **kwarg):
        return await self.httpx_get(
            await self.build_url(resources=resources, **kwarg), raw=False
        )

    async def get_pages(self, resources, **kwarg):
        page = 0
        per_page = 50
        result = []
        while 1:
            page += 1
            records = await self.httpx_get(
                await self.build_url(
                    resources=resources,
                    **kwarg,
                    page=page,
                    per_page=per_page,
                    # pagination="legacy",
                )
            )
            if records:
                if isinstance(records, list):
                    result.extend(records)
                else:
                    result.append(records)
            if len(records) < per_page:
                break
        return result

    async def get_branches(self, param):
        result = []
        regex = param.get_string("regex")
        for branch in await self.get_pages(
            resources={
                "repos": True,
                "owner": param.get_string("git_owner"),
                "repo": param.get_string("git_repo"),
                "search": param.get_string("search"),
                "branches": True,
            },
        ):
            if regex and not re.match(regex, branch["name"]):
                continue
            result.append(branch["name"])
        return result

    async def get_projects(self, param):
        result = []
        regex = param.get_string("regex")
        for project in await self.get_pages(
            resources={
                "users": True,
                "owner": param.get_string("git_owner"),
                "repos2": True,
            }
        ):
            if regex and not re.match(regex, project["name"]):
                continue
            result.append(project["name"])
        return result

    async def get_tags(self, param):
        result = []
        regex = param.get_string("regex")
        search = param.get_string("search")
        for tag in await self.get_pages(
            resources={
                "repos": True,
                "owner": param.get_string("git_owner"),
                "repo": param.get_string("git_repo"),
                "tags": True,
            },
        ):
            if search and tag["name"] != search:
                continue
            # search=param.get_string("search"),
            if regex and not re.match(regex, tag["name"]):
                continue
            result.append(tag["name"])
        return result

    async def get_tree(self, param, path):
        result = []
        regex = param.get_string("regex")
        for files in await self.get_pages(
            resources={
                "repos": True,
                "owner": param.get_string("git_owner"),
                "repo": param.get_string("git_repo"),
                "tree": param.get_string("git_branch"),
            },
            recursive="true",
        ):
            for file in files["tree"]:
                if file["type"] == "tree":
                    continue
                # Если пусть начинается с маршрута
                if file["path"].startswith("" if path == "/" else path):
                    if regex and not re.match(regex, file["path"]):
                        continue
                    result.append(
                        {
                            "path": file["path"],
                            "sha": file["sha"],
                            "name": os.path.basename(file["path"]),
                        }
                    )
        return result

    async def get_file(self, param, path):
        branch = param.get_string("git_branch")
        get_result = await self.get_httpx(
            resources={
                "repos": True,
                "owner": param.get_string("git_owner"),
                "repo": param.get_string("git_repo"),
                "contents": path.replace("/", "%2F").replace(".", "%2E"),
            },
            ref=branch,
        )
        file_bytes = base64.b64decode(get_result["content"])
        # Определить кодировку файла
        file_encoding = chardet.detect(file_bytes)["encoding"]
        file_encoding = file_encoding.upper() if file_encoding else None
        # Определение формата входного файла и BOM
        # Переменная для определения BOM для UTF8 фалов
        bom = 0
        # Формат входного файла
        encode = "cp1251"
        if file_encoding in ["UTF-8-SIG", "UTF-8", "MACROMAN"]:
            encode = "utf-8"
            if file_bytes[0] == 239:  # Первый байт BOM
                bom = 1
        # Раскодировать входную байтовую строку, во внутренний формат
        file_str = ""
        encoding = 0
        try:
            file_str = codecs.decode(file_bytes, encode)
            encoding = 1
        except Exception:
            pass
        return {
            "branch": branch,
            "path": path,
            "encode_detect": file_encoding,
            "encode": encode,
            "bom": bom,
            "encoding": encoding,
            "text": file_str,
        }

    async def get_commits(self, param, branch):
        result = []
        for commit in await self.get_pages(
            resources={
                "repos": True,
                "owner": param.get_string("git_owner"),
                "repo": param.get_string("git_repo"),
                "commits": True,
            },
            sha=branch,
            path=param.get_string("path"),
            since=(
                datetime.datetime.fromisoformat(
                    param.get_string("since")
                ).isoformat()
                if param.get_string("since")
                else None
            ),
            until=(
                datetime.datetime.fromisoformat(
                    param.get_string("until")
                ).isoformat()
                if param.get_string("until")
                else None
            ),
        ):
            result.append(commit)
        return result

    async def get_diff(self, param, sha):
        result = []
        for diff in await self.get_pages(
            resources={
                "repos": True,
                "owner": param.get_string("git_owner"),
                "repo": param.get_string("git_repo"),
                "commit_sha": sha,
            }
        ):
            for file in diff["files"]:
                result.append(file["filename"])
        return result


class Pool:

    pools = None

    def __init__(self):
        self.pools = {}

    async def get_project(self, param):
        owner = param.get_string("git_owner")
        token = param.get_string("git_token")
        repo = param.get_string("git_repo")
        key = f"{owner=}::{token=}::{repo=}"
        if key not in self.pools:
            # Подключиться к репозиторию
            gl = GithubAsync()
            await gl.set_project(owner=owner, token=token, name=repo)
            # Подключиться к проекту
            self.pools[key] = gl
        # logger.info(f'gitlab pool : {repo}@{url}')
        return self.pools[key]


git_pool = Pool()
