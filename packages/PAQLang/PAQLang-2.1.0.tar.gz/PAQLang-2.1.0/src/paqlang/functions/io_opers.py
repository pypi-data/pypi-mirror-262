import logging

from ..utils import get_json, get_json_data
from ..utils import get_attr, get_text, walk

from ..param import Param

# Установить текущи логгер
logger = logging.getLogger(__name__)


class IoOpers:
    """Операции ввода/вывода"""

    async def single_walk(pgm, param, p_queue, in_queue=None, out_queue=None):
        """Получить рекурсивно список файлов в директории.
        Входная очередь, содержит массив начальных маршрутов поиска.
        * **regex**:str=None - шаблон отбора файлов, если не задан,
        то найти все файлы
        * **git_owner**:str - Подключение к github
        * **git_url**:str - Подключение к gitlab
        * **git_token**:str
        * **git_repo**:str - проект репозитория
        * **git_branch**:str - ветка"""
        while len(in_queue):
            # Запросить список файлов
            out_queue.extend(await walk(path=in_queue.pop(0), param=param))
        return ["success"]

    async def multiple_freads(
        pgm, param, p_queue, in_queue=None, out_queue=None
    ):
        """Прочитать файл и положить содержимое в выходную очередь.
        Формат очереди {fname, text}.
        Кодировка для файлов windows cp1251.
        * **encoding**:str=None - кодировка файла
        * **to_json**=None, если указан атрибут,
          то файл преобразовать в объект и вернуть как массив
        * **split**:str=None, если указан атрибут,
          то разбить текстовый файл на строки.
          Если указан символ разбиения, то разбить соответственно ему.
        * **git_owner**:str - Подключение к gitlab.
        * **git_url**:str - Подключение к gitlab.
        * **git_token**:str - токен подключения.
        * **git_repo**:str - проект репозитория.
        * **git_branch**:str - ветка
        * **path**:str - если задан параметр,
        то значение :1 заменяется на значение из очереди,
        для получения имени файла"""
        while len(in_queue):
            # Получить имя файла
            file_name = in_queue.pop(0)
            if isinstance(file_name, str):
                # Асинхронно прочимтать файл с диска или git
                (fname, text) = await get_text(
                    file_name=file_name, param=param, is_file=1
                )
                if "to_json" in param.dict:
                    # Положить объект в очереь
                    out_queue.extend(Param(get_json_data(text)).as_list())
                elif "split" in param.dict and text:
                    # Разбить на строки
                    out_queue.extend(
                        [
                            x
                            for x in text.split(
                                param.get_string("split") or "\n"
                            )
                            if isinstance(x, str) and len(x) > 0
                        ]
                    )
                else:
                    out_queue.append({"path": file_name, "text": text})
        return ["success"]

    async def single_to_json(
        pgm, param, p_queue, in_queue=None, out_queue=None
    ):
        """Распарсить JSON или YAML строковый элемент и положить в очередь.
         Входная строка преобразуется в JSON, несколько массивов склеиваются.
        * **param**:str=None - задает имя атрибута,
        где содержится текст JSON или YAML
        * **attr**:str=None - задает имя атрибута"""
        # Если задан параметр атрибут
        attr = param.get_string("attr") or param.get_string()
        while len(in_queue):
            # Получить элемент из очереди, с начала списка
            text = in_queue.pop(0)
            js_text = (
                get_attr(attr=attr, elem=text, is_raise=False)
                if attr
                else text
            )
            if js_text:
                js = get_json(text=js_text)
                if isinstance(js, list):
                    for elem in js:
                        if elem:
                            out_queue.append(elem)
                else:
                    out_queue.append(js)
        return ["success"]
