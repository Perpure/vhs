[![pipeline status](https://gitlab.informatics.ru/pp17-53/HoE/badges/develop/pipeline.svg)](https://gitlab.informatics.ru/pp17-53/HoE/commits/develop)

<h1>Установка и развертывание web-приложения HoE</h1>

1. Инициализировать git
```
git init
```
2. Склонировать репозиторий по HTTP или SSH
```
git clone https://gitlab.informatics.ru/pp17-53/HoE
```
3. Перейти в склонированный репозиторий
```
cd HoE
```
4. Создать виртуальное окружение
```
virtualenv --python=python3 venv
```
5. Активировать виртуальное окружение
```
source venv/bin/activate
```
6. Установить зависимости
```
pip install -r requirements.txt
```
7. Выполнить миграцию
```
python3 migrate.py
```
8. Запустить приложение
```
python3 run.py
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
