[![pipeline status](https://gitlab.com/multiscreen/vhs/badges/master/pipeline.svg)](https://gitlab.com/multiscreen/vhs/commits/master) [![coverage report](https://gitlab.com/multiscreen/vhs/badges/master/coverage.svg)](https://gitlab.com/multiscreen/vhs/commits/master)


<h1>Установка и развертывание web-приложения</h1>

1. Инициализировать git <br>
```git init```
2. Склонировать репозиторий по HTTP или SSH <br>
```git clone git@gitlab.com:multiscreen/vhs.git```
3. Перейти в склонированный репозиторий <br>
```cd vhs```
4. Создать виртуальное окружение <br>
```virtualenv --python=python3 venv```
5. Активировать виртуальное окружение <br>
```source venv/bin/activate```
6. Установить зависимости <br>
```pip install -r requirements.txt```
7. Выполнить миграцию <br>
```python3 migrate.py```
8. Запустить приложение<br>
```python3 run.py```

<h1>Отправка Merge Request</h1>

Проверка кода на соответствие стандарту PEP-8 выполняется следующим образом:
```
pycodestyle web --max-line-length=120 --ignore=E402 --show-source --show-pep8
```

Запуск юнит-тестов производится с помощью:
```
nose2 -v
```

Перед снятием WIP статуса с Merge Request удостоверьтесь, что все тесты пройдены без ошибок.

Запросы на слияние с ошибками pipeline будут отклонены.
