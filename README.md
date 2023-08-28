#  Асинхронный неблокирующий HTTP-сервер на сокетах

## Краткое описание проекта

Сервер обрабатывает следующие передаваемые команды:
quit — закрытие соединения;
time — получение текущего времени в UTC;
info — получение информации о системе и версии интерпретатора;
find <file-name> <path> — поиск шаблона файла по указанному пути. При наличии такого файла, возвращает имя, дату создания, размер. Если под шаблон попадает более одного файла, то возвращает количество.


### Технологии

- Python 3.10
- selectors
- socket

### Как запустить проект

Клонировать репозиторий и перейти в него в командной строке:

```
git clone
```

```
cd server
```

Cоздать и активировать виртуальное окружение:

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

Запустить сервер:

```
python3 non_blocking_server.py
```

Подключиться к серверу:

```
telnet 127.0.0.1 8000
```

### Автор.
[Оксана Широкова](https://github.com/son13425)


## Лицензия
Проект выпущен под лицензией [MIT](https://github.com/son13425/server/blob/main/LICENSE)
