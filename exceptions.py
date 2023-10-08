class GetApiAnswerError(Exception):
    """Сбой при запросе к API."""

    ...


class ParseStatusError(Exception):
    """Ошибка при извлечении статуса домашней работы."""

    ...


class SendMessageError(Exception):
    """Сбой при отправке сообщения."""

    ...
