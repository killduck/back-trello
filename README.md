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
Windows
* Bash:
```
source venv/Scripts/activate
```
* Windows Shell:
```
.venv\Scripts\Activate.ps1
```
MacOS/Unix
* Bash/Zsh:
```
source .venv/bin/activate
```

### Команды для Django:
- Установка зависимостей из файла requirements.txt если версиия
```
pip install -r requirements.txt
```

- Запуск встроенного сервера Django
```
python manage.py runserver
```

- Работа с миграциями
* Проверяем модели и таблицы в БД, подготавливаем скрипты миграций
```
python manage.py makemigrations
```
* Запускаем миграции
```
python manage.py migrate
```
