# Django project

## Trello

## Референс (что делаем)

https://trello.com

### Настройки проекта:

- config для SSH-ключей

```
Host github.com-back-31
    HostName github.com
    User git
    IdentityFile ~/.ssh/you_name_key
```

- Команда для клонирования репы с GitHub

```
git clone git@github.com-back-31:Ilya616/back-group31.git
```

- Волшебные команды для подтягивания и обновления веток репы на локальном компе

```
git branch -r | grep -v '\->' | while read remote; do git branch --track "${remote#origin/}" "$remote"; done
```

```
git fetch --all
```

```
git pull --all
```

- Создание виртуального окружения
  Windows, MacOS/Unix

```
python -m venv .venv
```

- Активация виртуального окружение
  Windows \* Bash:

```
source .venv/Scripts/activate
```

    * Windows Shell:

```
.venv\Scripts\Activate.ps1
```

MacOS/Unix \* Bash/Zsh:

```
source .venv/bin/activate
```

### Команды для Django:

- Сохранение зависимостей(установленных пакетов) в файл requirements.txt
  Команда подается из директории back-group31

```
pip freeze > requirements.txt
```

- Установка зависимостей из файла requirements.txt

```
pip install -r requirements.txt
```

- Запуск встроенного сервера Django
  Команда подается из директории trello

```
python manage.py runserver
```

- Работа с миграциями
  Проверяем модели и таблицы в БД, подготавливаем скрипты миграций

```
python manage.py makemigrations
```

_если команда не сработала введите_

```
python manage.py makemigrations trello
```

Запускаем миграции

```
python manage.py migrate
```

Очистка таблиц БД:
```
python manage.py clear_DB
```

Засеять БазуДанных фейковыми данными для теста:
```
python manage.py seeds
```

- Создание Супер Пользователя для доступа к Админке Django:
  Команда

```
python manage.py createsuperuser
```

Поочередно ответьте на запросы:

```
Username (leave blank to use 'user'): // Придумайте логин (например, admin)
Email address: // Введите любой email (например, admin@mail.com)
Password: // Введите пароль (например, 123)
Password (again): // повторите пароль
Если вы укажете слишком простой пароль (например, 123), Django предложит усложнить его:
This password is too short. It must contain at least 8 characters.
This password is too common.
This password is entirely numeric.
Bypass password validation and create user anyway? [y/N]: // Введит  'y' для подтсверждения простого пароля
Superuser created successfully. // Финальное сообщение о создании Супер Пользователя
```

Для доступа к Админке введите в адресную строку браузера:

```
http://127.0.0.1:8000/admin
```

и в форму регистрации введите данные созданные для Супер Пользователя
