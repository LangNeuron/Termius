# Выход от плагина

Словарь у которого 2 значения `status` и `message`. В первом идет 
закодированный код отработки плагина (**Смотреть справку о кодах в приложении 1**). 
В `message` хранится сообщение от модуля (чаще всего нужен для исключений), но
используется в базовых модулях (WWD, TTS, STT, LLM) или для озвучивания ответа.

# Приложения

## Приложение 1

0 - Успешное завершение работы, озвучить ответ.

1 - Успешное завершение работы, не озвучить ответ.

2 - Завершен без указания причины.

3 - Получена ошибка (в `message` хранится текст ошибки).
