import logging
import asyncio
import aiofiles  # noqa

from ..utils import aio_get_json, send_message, abs_file_path
from ..utils import coalesce, get_condition

from ..param import Param

# Установить текущи логгер
logger = logging.getLogger(__name__)


def get_opers(opers: list, filter_groups: str) -> list:
    """Получить список всех функций по группе или всех групп,
    отсортированных по наименованию группы и имени функции"""
    # Получить список групп операций, с отбором по заданной группе
    group_docs = [
        oper["group_doc"]
        for oper in opers.values()
        if oper["group_doc"]
        and filter_groups is None
        or oper["group"] in filter_groups
    ]
    # Получить уникальный и отсортированный массив
    groups = []
    for group_name in sorted(list(set(group_docs))):
        # Получить отсортированный список операций
        group = {"name": group_name}
        group["opers"] = list()
        for oper_name in sorted(
            [
                oper["name"]
                for oper in opers.values()
                if oper["group_doc"] == group_name
            ]
        ):
            oper = opers[oper_name]
            group["id"] = oper["group"]
            group["opers"].append(oper["name"])
        groups.append(group)
    return groups


class Files:

    files = None

    def __init__(self):
        self.files = {}

    def add(self, fname, line: str = None):
        _fname = fname.lower()
        if _fname not in self.files:
            self.files[_fname] = list()
        self.files[_fname].append(line or "")

    def print(self, path: str):
        # Получить все сформированные файлы
        if path:
            for file_name, lines in self.files.items():
                with open(
                    abs_file_path(f"{file_name}.md", path),
                    mode="w",
                    encoding="utf-8",
                ) as f:
                    for line in lines:
                        f.write(f"{line}\n")


class OtherOpers:
    """Сервисные операции"""

    async def single_opers(pgm, param, p_queue, in_queue=None, out_queue=None):
        """Вывести словарь функций.
        * **param**:str=None - по заданной группе функций"""
        group = param.get_string()
        for oper in {**pgm.single_opers, **pgm.multiple_opers}.values():
            if group is None or group == oper["group"]:
                out_queue.append(oper)
        return ["success"]

    async def single_popers(
        pgm, param, p_queue, in_queue=None, out_queue=None
    ):
        """Подготовить документацию по функциям.
        * **groups**:[str|list] или param:str или None -
        вывеcти только данные заданной группы функций
        * **path**:str - вывести в файлы по данному маршруту"""
        if param.get_list("groups"):
            filter_groups = param.get_list("groups")
        elif param.get_string("groups"):
            filter_groups = [param.get_string("groups")]
        elif param.get_string():
            filter_groups = [param.get_string()]
        else:
            filter_groups = None
        # Получить параметр вывода в файл
        path = param.get_string("path")
        # Получить список всех операций
        opers = {**pgm.single_opers, **pgm.multiple_opers}
        groups = get_opers(opers, filter_groups)
        # Файлы
        files = Files()
        # Под файл оглавления
        files.add("topic", "# Functions")
        files.add("topic")
        # Перебрать группы
        for group in groups:
            # Файл группы функций
            id = group["id"].lower()
            # Оглавление группы функций
            files.add("topic", f'- [{group["name"]}]({id}.md)')
            files.add(id, f'# {group["name"]} ({group["id"]})')
            files.add(id)
            # Перебрать функции для оглавления
            for oper_name in group["opers"]:
                oper = opers[oper_name]
                # Оглавление функции в topic
                files.add(
                    "topic",
                    f'  - [{oper_name}: {oper["title"]}]({id}.md#{oper_name})'
                )
                # Оглавление функции в группе
                files.add(
                    id,
                    f'- [{oper_name}: {oper["title"]}](#{oper_name.lower()})'
                )

            # Перебрать функции для формирования текста
            for oper_name in group["opers"]:
                oper = opers[oper_name]
                # Сформировать описание функции
                files.add(id)
                files.add(id, "---")
                files.add(id)
                files.add(id, f"## **{oper['name']}**")
                files.add(id)
                # Убрать все лидирующие пробелы
                lines_strip = [
                    line.strip() for line in (oper["doc"] or "").split("\n")
                ]
                # Join длинные строки через пробел
                lines = []
                for line in lines_strip:
                    if line[0:1] == "*":
                        # Описание параметра
                        lines.append(line)
                    elif line == "":
                        lines.append("")
                    else:
                        lines.append(
                            (lines.pop() + " " if lines else "") + line
                        )
                # Сформировать описание
                files.add(id, ">")
                is_param_title = True
                for line in lines:
                    if line[0:1] == "*":
                        # Описание параметра
                        if is_param_title:
                            is_param_title = False
                            files.add(id, ">")
                            files.add(id, "> **Parameters**:")
                        files.add(id, ">")
                        files.add(id, f"> - {line[2:]}")
                    else:
                        if is_param_title:
                            # Описание функции
                            files.add(id, f"> {line}")
                        else:
                            files.add(id, f"> _{line.strip()}_")

                test_name = f"test code: {oper_name}"
                if id == "oracleopers":
                    path2 = "oracle"
                elif id == "gitlabopers":
                    path2 = "gitlab"
                elif id == "githubopers":
                    path2 = "github"
                else:
                    path2 = "main"
                test_path = f"/tests/{path2}/test_{oper_name}.py"
                files.add(id)
                files.add(id, f"[{test_name}]({test_path})")

        files.print(path)

        return ["success"]

    async def _print_message(pgm, param, p_queue, in_queue, out_queue, tp):
        """Отправить сообщение об ошибке или успешное"""
        out_queue.extend(in_queue)
        # Получить наименование тестируемого атрибута
        test_attr = param.get_string("test-attr")
        send_attr = param.get_string("send-attr")
        # Очередь ошибок
        errors = []
        for elem in in_queue:
            result = True
            if test_attr:
                pelem = Param(elem)
                test_value = coalesce(
                    [pelem.get_float(test_attr), pelem.get_string(test_attr)]
                )
                result = get_condition(test_value, param)
            if result:
                if send_attr:
                    if send_attr in elem:
                        errors.append(f"{elem[send_attr]}")
                else:
                    errors.append(f"{elem}")
        if len(errors):
            name = param.get_string("name") or param.get_string()
            if tp:
                logger.info(f' {name}{": " if name else ""}{errors}')
            else:
                logger.error(f' {name}{": " if name else ""}{errors}')
        return ["success"]

    async def single_info(pgm, param, p_queue, in_queue=None, out_queue=None):
        """Вывести очередь в info поток.
        Входная очередь сообщений.
        * **name**:str=None or **param**:str = None - заголовок
        * **test-attr**:str=None - тестируемый аттрибут
        * **send-attr**:str=None - отправляемый атрибут,
        * **lt** - меньше
        * **le** - Меньше или равно
        * **eq** - равно
        * **ne** - не равно
        * **gt** - больше
        * **ge** - больше или равно
        * **instr** - входит в строку
        * **notinstr** - не входит в строку
        иначе печатаем весь элемент"""
        return await OtherOpers._print_message(
            pgm, param, p_queue, in_queue, out_queue, 1
        )

    async def single_error(pgm, param, p_queue, in_queue=None, out_queue=None):
        """Вывести очередь в error поток.
        Входная очередь сообщений.
        * **name**:str=None or **param**:str = None - заголовок
        * **test-attr**:str=None - тестируемый аттрибут
        * **lt** - меньше
        * **le** - Меньше или равно
        * **eq** - равно
        * **ne** - не равно
        * **gt** - больше
        * **ge** - больше или равно
        * **instr** - входит в строку
        * **notinstr** - не входит в строку
        * **send-attr**:str=None - отправляемый атрибут,
        иначе печатаем весь элемент"""
        return await OtherOpers._print_message(
            pgm, param, p_queue, in_queue, out_queue, 0
        )

    async def single_sleep(pgm, param, p_queue, in_queue=None, out_queue=None):
        """Асинхронно заснуть на заданное кол-во секунд.
        * **param**:float - кол-во секунд, если не задано,
        то 1 секунда"""
        sleep_sec = param.get_float() or 1
        logger.info(f"sleep: {sleep_sec}")
        await asyncio.sleep(sleep_sec)
        out_queue.extend(in_queue)
        return ["success"]

    async def multiple_msleep(
        pgm, param, p_queue, in_queue=None, out_queue=None
    ):
        """Асинхронно заснуть на заданное кол-во секунд.
        Запустить несколько потоков, в зависимости от входной очереди.
        Для отладки асинхронности.
        * **Входная очередь**:list - очередь задержек"""
        while len(in_queue):
            # Вычислить время засыпания
            sleep_sec = Param(in_queue.pop(0)).get_float()
            if sleep_sec:
                logger.info(f"msleep: {sleep_sec}")
                await asyncio.sleep(sleep_sec)
        return ["success"]

    async def multiple_include(
        pgm, param, p_queue, in_queue=None, out_queue=None
    ):
        """Загрузить подпрограммы.
        * **Входная очередь** - имена json и yaml файлов"""
        while len(in_queue):
            # Получить имя файла
            file_name = in_queue.pop(0)
            if isinstance(file_name, str):
                subroutines = await aio_get_json(file_name=file_name)
                for key, item in subroutines.items():
                    pgm.macros[key] = item
                    logger.info(f"include: {key}")
        return ["success"]

    async def _send_message(pgm, param, p_queue, in_queue, out_queue, tp):
        """Отправить сообщение об ошибке или успешное"""
        out_queue.extend(in_queue)
        # Получить наименование тестируемого атрибута
        test_attr = param.get_string("test-attr")
        send_attr = param.get_string("send-attr")
        # Очередь ошибок
        errors = []
        for elem in in_queue:
            result = True
            if test_attr:
                pelem = Param(elem)
                test_value = coalesce(
                    [pelem.get_float(test_attr), pelem.get_string(test_attr)]
                )
                result = get_condition(test_value, param)
            if result:
                if send_attr:
                    if send_attr in elem:
                        errors.append(f"{elem[send_attr]}")
                else:
                    errors.append(f"{elem}")
        if len(errors):
            await send_message(
                message="\n".join(errors),
                success=tp,
                service=param.get_string("name")
                or param.get_string()
                or "PAQLang",
            )
        return ["success"]

    async def single_send_errors(
        pgm, param, p_queue, in_queue=None, out_queue=None
    ):
        """Отправить сообщение об ошибке.
        Входная очередь сообщение.
        * **name**:str = None or **param**:str = None - сообщение в заголовке,
        по умолчанию PAQLang
        * **test-attr**:str = None - тестируемый аттрибут
        * **send-attr**:str = None - отправляемый атрибут,
        иначе печатаем весь элемент
        * **lt** - меньше
        * **le** - Меньше или равно
        * **eq** - равно
        * **ne** - не равно
        * **gt** - больше
        * **ge** - больше или равно
        * **instr** - входит в строку
        * **notinstr** - не входит в строку"""
        return await OtherOpers._send_message(
            pgm=pgm,
            param=param,
            p_queue=p_queue,
            in_queue=in_queue,
            out_queue=out_queue,
            tp=0,
        )

    async def single_send_success(
        pgm, param, p_queue, in_queue=None, out_queue=None
    ):
        """Отправить успешное сообщение.
        Входная очередь сообщение.
        * **name**:str = None or **param**:str = None - сообщение в заголовке,
        по умолчанию PAQLang
        * **test-attr**:str = None - тестируемый аттрибут
        * **send-attr**:str = None - отправляемый атрибут,
        иначе печатаем весь элемент
        * **lt** - меньше
        * **le** - Меньше или равно
        * **eq** - равно
        * **ne** - не равно
        * **gt** - больше
        * **ge** - больше или равно
        * **instr** - входит в строку
        * **notinstr** - не входит в строку"""
        return await OtherOpers._send_message(
            pgm=pgm,
            param=param,
            p_queue=p_queue,
            in_queue=in_queue,
            out_queue=out_queue,
            tp=1,
        )
