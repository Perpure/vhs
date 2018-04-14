[![pipeline status](https://gitlab.informatics.ru/pp17-53/HoE/badges/develop/pipeline.svg)](https://gitlab.informatics.ru/pp17-53/HoE/commits/develop)

<h1>Установка и развертывание web-приложения HoE</h1>

1. Инициализировать git <br>
```git init
```
2. Склонировать репозиторий по HTTP или SSH <br>
```git clone https://gitlab.informatics.ru/pp17-53/HoE
```
3. Перейти в склонированный репозиторий <br>
```cd HoE
```
4. Создать виртуальное окружение <br>
```virtualenv --python=python3 venv
```
5. Активировать виртуальное окружение <br>
```source venv/bin/activate
```
6. Установить зависимости <br>
```pip install -r requirements.txt
```
7. Выполнить миграцию <br>
```python3 migrate.py
```
8. Запустить приложение
```python3 run.py
```

<h1>Запуск проведения статического и динамического анализа кода</h1>

Чтобы проверить код на соответствие стандарту PEP-8 выполняется следующая команда:
```
pycodestyle --max-line-length=120
```

Чтобы запустить unit-тесты надо воспользоваться командой:
```
nose2
```
Чтобы увидеть подробные результаты unit-тество надо выполнить команду:
```
nose2 -v
```
