# Обновленная версия

## Продьюсер
- Ходит в облако, сканит файлы
- Если файл подходит под правила, то создает запись для консьюмера:
  - PNG файл: [удаление](#"Удаление")
  - [Переименование](#Переименование)
  - HEIC/heif: Конвертировать.

Для каждого файла должна быть очередность действий. PNG это только удаление.
Делает json запись что делать с каждым файлом.


## Консьюмер
Исполнитель. Ходит в БД и получает от туда все данные для работы. Для каждого задания назначает своего воркера.


## "Удаление"
Под удалением понимается перемещение в спецпапку
- `.PNG`: `/png_trash`
- `.HEIC`: `/heic_trash`
Эти папки я буду вручную проверять и сам удалять.

Удаление можно реализовать средствами `webdavclient`. Конвертацию либо через `PIL` либо через консоль.

## Переименование
Неправильное имя: переименовать в формат `YYYMMDD_HHmmss`

## Конвертация


## Resources:
- [Python WebDAV Client 3](https://github.com/ezhov-evgeny/webdav-client-python-3)
