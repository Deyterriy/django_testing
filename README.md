# Тестирование Веб-приложения при помощи Pytest и Unit-тестов

## Используемые технологии

[![Python](https://img.shields.io/badge/-Python-464646?style=flat&logo=Python&logoColor=56C0C0&color=008080)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat&logo=Django&logoColor=56C0C0&color=008080)](https://www.djangoproject.com/)
[![Pytest](https://img.shields.io/badge/-Pytest-464646?style=flat&logo=Pytest&logoColor=56C0C0&color=008080)](https://docs.pytest.org/en/7.4.x/)
[![Unittest](https://img.shields.io/badge/-Unittest-464646?style=flat&logo=Unittest&logoColor=56C0C0&color=008080)](https://docs.python.org/3/library/unittest.html)



* В даном проекте тестируются:
    - Логика приложений
    - Правильность выдачи контента
    - Маршрутизация приложений 

* В проекте присутсвуют два независящих друг от друга Веб-приложения:

    * ya_news - тестирование проводится при помощи Pytest
    * ya_note - тестирование проводится при помощи Unit-тестов

### Как запустить проект:

* Клонировать репозиторий и перейти в его директорию
    ```bash
    git clone git@github.com:Deyterriy/django_testing.git
    ```

* Cоздать и активировать виртуальное окружение:

    * Windows
    ```bash
    python -m venv venv
    ```
    ```bash
    source venv/Scripts/activate
    ```

    * Linux/macOS
    ```bash
    python3 -m venv venv
    ```
    ```bash
    source venv/bin/activate
    ```


* Обновить PIP

    ```bash
    python -m pip install --upgrade pip
    ```

* Установить зависимости из файла requirements.txt:

    ```bash
    pip install -r requirements.txt
    ```

* Выполнить миграции:

    ```bash
    python manage.py makemigrations
    ```
    ```bash
    python manage.py migrate
    ```

* Перейти в директорию ya_news и выполнить команду для начала тестирования
    ```bash
    # /django_testing/ya_news/
    pytest
    ```

* Перейти в директорию ya_news и выполнить команду для начала тестирования
    ```bash
    # /django_testing/ya_note/
    python manage.py test
    ```

### Автор:  
_Козлов Кирилл_<br>
**email**: _d3yterriy@yandex.ru_<br>
