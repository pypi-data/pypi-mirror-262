# PAQLang

Python Async Queue Language

[![Super-Linter](https://github.com/strukovsv/PAQLang/actions/workflows/lint-flake8.yml/badge.svg)](https://github.com/marketplace/actions/python-flake8-lint)
[![Pytest](https://github.com/strukovsv/PAQLang/actions/workflows/pytest.yml/badge.svg)](https://github.com/strukovsv/PAQLang/tree/master/tests/main)
[![Release](https://github.com/strukovsv/PAQLang/actions/workflows/release.yml/badge.svg)](https://github.com/strukovsv/PAQLang/tree/master/CHANGELOG.md)

## Содержание

- [PAQLang](#paqlang)
  - [Содержание](#содержание)
  - [Назначение](#назначение)
  - [Install](#install)
  - [Документация](#документация)
  - [Пример программы обработки текстов](#пример-программы-обработки-текстов)

## Назначение

- Пакет предназначен, для выполнения задач, с использованием асинхронных функций на языке Python.
- Пакет содержит встроенные функции работы с данными и возможность добавления новых функций
- Код задачи представляет собой или JSON объект в Python или Yaml текст.

## Install

- Установка только встроенных функций

  **pip install PAQLang**

- Установка с пакетами работы Gitlab и Oracle

  **pip install PAQLang[all]**

## Документация

Документацию по встроенным функциям системы можно получить по [этой ссылке](./docs/ru/functions.md).

## Пример программы обработки текстов

```text
# Пример обработки текстов
import logging

from paqlang import pgm

# Стандартное логирование
logging.getLogger().setLevel(logging.INFO)
logging.info("")

def main():
    pgm(pgm_code = """

# Прочитать файл /data/list-bugs.yaml и положить содержимое в очередь
# - line: 10001
#   name: test1
# - line: 4578
#   name: test2
# - line: 7898
#   name: test3

# Задать имя входного файла
- in: /data/list-bugs.yaml

# Прочитать файл и вернуть содержимое как объект, в данном случае список из 3 элементов
- freads:
    to_json:

# Каждый элемент массива, как словарь, заменить на значение атрибута "line"
- attr: line

# Распечатать результирующий список
- print
#INFO:print: 10001
#INFO:print: 4578
#INFO:print: 7898

""")

if __name__ == "__main__":
    main()
```
