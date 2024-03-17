import logging
from paqlang.utils import aio_reads

from .aio_gitlab import git_pool as gitlab_pool
from .aio_github import git_pool as github_pool

# Установить текущи логгер
logger = logging.getLogger(__name__)


def get_attr(attr, elem, is_raise: bool = True):
    if attr:
        if attr and isinstance(elem, dict) and (attr in elem):
            return elem[attr]
        else:
            if is_raise:
                raise Exception(
                    f'Не найден атрибут "{attr}" в элементе "{elem}"'
                )
            else:
                return None
    return elem


def coalesce(plist: list):
    for elem in plist:
        if elem is not None:
            return elem
    return None


def get_condition(test_value, param):
    """Проверить условие

    test_value:float:int:str - проверяемое значение
    param:dict - словарь заданных условий
    return bool - результат проверки
    """
    if isinstance(test_value, (float, int)):
        where = True
        conditions_float = {
            "lt": lambda x, y: x < y,
            "le": lambda x, y: x <= y,
            "eq": lambda x, y: x == y if y is not None else x is None,
            "ne": lambda x, y: x != y if y is not None else x is not None,
            "gt": lambda x, y: x > y,
            "ge": lambda x, y: x >= y,
        }
        for key, function in conditions_float.items():
            if key in param.dict:
                where = where and function(test_value, param.get_float(key))
                logger.debug(
                    f"{key=} {test_value=} {param.get_float(key)=} {where=}"
                )
        return where
    elif isinstance(test_value, str):
        where = True
        conditions_str = {
            "lt": lambda x, y: x < y,
            "le": lambda x, y: x <= y,
            "eq": lambda x, y: x == y if y is not None else x is None,
            "ne": lambda x, y: x != y if y is not None else x is not None,
            "gt": lambda x, y: x > y,
            "ge": lambda x, y: x >= y,
            # Входит строка
            "instr": lambda x, y: x in y,
            # Не входит строка
            "notinstr": lambda x, y: x not in y,
        }
        for key, function in conditions_str.items():
            if key in param.dict:
                where = where and function(test_value, param.get_string(key))
                logger.debug(
                    f"{key=} {test_value=} {param.get_string(key)=} {where=}"
                )
        return where
    return False


async def get_sql_text(file_name, param):
    if "path" in param.dict:
        path = param.get_string("path")
        # Если path содержит, то сделать подстановку,
        # иначе подставить имя файла как есть в очереди
        fname = (
            path.replace(":1", file_name)
            if path and (":1" in path)
            else file_name
        )
    else:
        fname = file_name
    if "git_url" in param.dict:
        gl = await gitlab_pool.get_project(param=param)
    elif "git_owner" in param.dict:
        gl = await github_pool.get_project(param=param)
    else:
        gl = None
    if gl:
        # Работаем с gitlab
        try:
            # Прочитать файл из git, передаем имя файла
            file = await gl.get_file(param, fname)
        except Exception as e:
            logger.error(f"get file: {fname} - {e}")
            raise
        # Содержимое файла
        sql = file["text"]
    else:
        # Если задана атрибут path,
        # то прочитать файл с локального диска
        if "path" in param.dict:
            # Возможность задать кодировку файла
            encoding = param.get_string("encoding") or "utf-8"
            # Прочитать содержимое файла
            sql = await aio_reads(file_name=fname, encoding=encoding)
        else:
            # Запрос из потока, не из файла данных
            fname = None
            # В данном случае пришел текст
            sql = file_name
    return (fname, sql)
