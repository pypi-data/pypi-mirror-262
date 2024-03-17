import logging

from .util_opers import coalesce, get_condition

# Установить текущи логгер
logger = logging.getLogger(__name__)


class ControlOpers:
    """Управление выполнением"""

    async def single_exit(pgm, param, p_queue, in_queue=None, out_queue=None):
        """Завершить выполнение программы"""
        return ["exit"]

    async def single_when(pgm, param, p_queue, in_queue=None, out_queue=None):
        """Если условие истино, ты выполнить stage.
        Проверяется входная очередь.
        Если указан атрибут **in**, то прверяется его значение.
        Условия объединяются по **and**.
        Если условие не задано, то выполняется код дальше,
        если входная очередь не пустая
        * **in** - сравниваемые данные
        * **lt** - меньше
        * **le** - Меньше или равно
        * **eq** - равно
        * **ne** - не равно
        * **gt** - больше
        * **ge** - больше или равно
        * **instr** - входит в строку
        * **notinstr** - не входит в строку"""
        # Скопировать очередь
        out_queue.extend(in_queue)
        if len(param.list) == 0:
            result = len(in_queue) != 0
        else:
            test_value = coalesce(
                [
                    param.get_float("in"),
                    param.get_string("in"),
                    p_queue.get_float(),
                    p_queue.get_string(),
                ]
            )
            result = get_condition(test_value, param)
        if result:
            return ["success"]
        else:
            # Откатить стайдж
            return ["when"]

    async def single_break(pgm, param, p_queue, in_queue=None, out_queue=None):
        """Если условие истино, ты прервать цикл while (break).
        Проверяется входная очередь.
        Если указан атрибут **in**, то прверяется его значение.
        Условия объединяются по **and**.
        * **in** - сравниваемые данные
        * **lt** - меньше
        * **le** - Меньше или равно
        * **eq** - равно
        * **ne** - не равно
        * **gt** - больше
        * **ge** - больше или равно
        * **instr** - входит в строку
        * **notinstr** - не входит в строку"""
        # Скопировать очередь
        out_queue.extend(in_queue)
        if len(param.list) == 0:
            result = len(in_queue) == 0
        else:
            test_value = coalesce(
                [
                    param.get_float("in"),
                    param.get_string("in"),
                    p_queue.get_float(),
                    p_queue.get_string(),
                ]
            )
            result = get_condition(test_value, param)
        if result:
            return ["break"]
        else:
            return ["success"]

    async def single_continue(
        pgm, param, p_queue, in_queue=None, out_queue=None
    ):
        """Если условие истино, ты прервать цикл while (continue).
        Проверяется входная очередь.
        Если указан атрибут **in**, то прверяется его значение.
        Условия объединяются по **and**.
        * **in** - сравниваемые данные
        * **lt** - меньше
        * **le** - Меньше или равно
        * **eq** - равно
        * **ne** - не равно
        * **gt** - больше
        * **ge** - больше или равно
        * **instr** - входит в строку
        * **notinstr** - не входит в строку"""
        # Скопировать очередь
        out_queue.extend(in_queue)
        test_value = coalesce(
            [
                param.get_float("in"),
                param.get_string("in"),
                p_queue.get_float(),
                p_queue.get_string(),
            ]
        )
        if get_condition(test_value, param):
            return ["continue"]
        else:
            return ["success"]
