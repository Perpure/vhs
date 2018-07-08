[![pipeline status](https://gitlab.com/multiscreen/vhs/badges/master/pipeline.svg)](https://gitlab.com/multiscreen/vhs/commits/master) [![coverage report](https://gitlab.com/multiscreen/vhs/badges/master/coverage.svg)](https://gitlab.com/multiscreen/vhs/commits/master)


## Установка и развертывание web-приложения

1. Склонировать репозиторий и перейти в его папку

    ```
    git clone git@gitlab.com:multiscreen/vhs.git
    cd vhs
    ```

2. Провести подготовку файла с переменными среды. Пример этих переменных описан в файле `.env.example`, поэтому нужно произвести его копию в файл `.env`. Затем отредактировать копию в соответствии с параметрами своей системы (подробнее в разделе "Переменные среды")

    ```
    cp .env.example .env
    # редактируем .env
    ```

3. Создать виртуальное окружение и активировать его

    ```
    virtualenv --python=python3 venv
    source venv/bin/activate
    ```

4. Установить зависимости

    ```
    pip install -r requirements.txt
    ```

5. Активировать переменные среды

    ```
    source .env
    ```

6. Выполнить миграцию базы данных

    ```
    python migrate.py
    ```

7. Выполнить действия по установки инструментов для _frontend_

8. Запустить приложение

    ```
    python run.py
    ```


## Отправка Merge Request

Проверка кода на соответствие стандарту **PEP-8** выполняется следующим образом:

```
pycodestyle web --max-line-length=120 --ignore=E402 --show-source --show-pep8
```

Запуск юнит-тестов производится с помощью:

```
nose2 web -C
```

Перед снятием WIP статуса с Merge Request удостоверьтесь, что все тесты пройдены без ошибок.

Запросы на слияние с ошибками в _CI_ будут отклонены.


## Переменные среды

Среди переменных среды важна `DATABASE_URL`, содержимое которой определяет местонахожение и параметры доступа к базе данных приложения. Проект поддерживает два типа СУБД: _SQLite_ и _PostgreSQL_.

Чтобы использовать _SQLite_ нужно указать **полный абсолютный** путь до файла с БД. Например, файл БД располагается в `/tmp/db.sqlite`. Тогда необходимо записать в переменную следующий _URI_:

```
export DATABASE_URL=sqlite:////tmp/db.sqlite
```

При использовании СУБД _PostgreSQL_ формат переменной будет следующий: 

```
export DATABASE_URL=postgres://username:password@host:port/datbase_name
```

## Установка инструментов для _frontend_

1. Установить _NodeJS_ (_LST version_): https://nodejs.org/en/download/
2. Установить `yarn`: https://yarnpkg.com/en/docs/install
3. Установить зависимости:

    ```
    yarn
    ```

4. Запустить сборщик:

    ```
    # одноразовая сборка
    yarn build
    # сборка по мере изменения файлов frontend
    yarn watch
    ```
