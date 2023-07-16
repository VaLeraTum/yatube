# Yatube

### Описание

Проект Yatube - это социальная сеть, где можно вести свой дневник, подписываться на понравившихся авторов, комментировать их посты и создавать тематические группы.

### Стек технологий

* Python 3.9.10,
* Django 2.0.5

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/ValeraTum/yatube.git
```

```
cd yatube
```

Создать и активировать виртуальное окружение:

```
python3 -m venv venv
```
* Если у вас Linux/macOS

```
source venv/bin/activate
```
* Если у вас windows

```
source venv/scripts/activate
```

Установить зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```

Выполнить миграции:
```
python3 manage.py migrate
```
Запустить проект:
```
python3 manage.py runserver
```