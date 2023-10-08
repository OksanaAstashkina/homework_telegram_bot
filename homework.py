import logging
import os
import requests
import sys
import time
import telegram

from dotenv import load_dotenv
from http import HTTPStatus
from pprint import pprint

from exceptions import (GetApiAnswerError,
                        ParseStatusError,
                        SendMessageError)

load_dotenv()

PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

RETRY_PERIOD = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}

HOMEWORK_VERDICTS = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def check_tokens():
    """Проверяет доступность переменных окружения."""
    tokens = {'PRACTICUM_TOKEN': PRACTICUM_TOKEN,
              'TELEGRAM_TOKEN': TELEGRAM_TOKEN,
              'TELEGRAM_CHAT_ID': TELEGRAM_CHAT_ID}
    for key, value in tokens.items():
        if not value or value is None:
            logger.critical(
                f'Отсутствует обязательная переменная окружения: "{key}"!')
    return all(tokens.values())


def get_api_answer(timestamp):
    """Делает запрос к эндпоинту API-сервиса Практикум.Домашка."""
    payload = {'from_date': timestamp}
    try:
        response = requests.get(ENDPOINT, headers=HEADERS, params=payload)
        if response.status_code != HTTPStatus.OK:
            raise GetApiAnswerError(
                f'Некорректный статус ответа API: код ответа'
                f'"{response.status_code}". Эндпоинт {ENDPOINT} недоступен.'
            )
        if response is None:
            raise GetApiAnswerError('Не удалось получить ответ от API!')
        response = response.json()
        pprint(response)
        return response
    except Exception as error:
        raise GetApiAnswerError(
            f'При запросе к API возникла ошибка: "{error}"!')


def check_response(response):
    """Проверяет ответ API на соответствие документации."""
    if not isinstance(response, dict):
        raise TypeError(
            'Некорректный формат ответ API: ответ не является словарем!')
    if 'current_date' not in response.keys():
        raise KeyError(
            'Некорректный формат ответа API:'
            'словарь не содержит ключа "current_date"!')
    if 'homeworks' not in response.keys():
        raise KeyError(
            'Некорректный формат ответа API:'
            'словарь не содержит ключа "homeworks"!')
    homeworks = response.get('homeworks')
    if not isinstance(homeworks, list):
        raise TypeError(
            'Некорректный формат ответа от API:'
            'значение ключа "homeworks" не является списком!')
    return homeworks


def parse_status(homework):
    """Извлекает статус из информации о конкретной домашней работе."""
    if not isinstance(homework, dict):
        raise TypeError('Переменная "homework" не является словарем!')
    homework_name = homework.get('homework_name')
    homework_status = homework.get('status')
    if homework_name is None:
        raise KeyError('Отсутствует ключ "homework_name"!')
    if homework_status is None:
        logger.debug('Новый статус домашних работ отсутствует.')
    if homework_status in HOMEWORK_VERDICTS:
        verdict = HOMEWORK_VERDICTS[homework_status]
        return f'Изменился статус проверки работы "{homework_name}". {verdict}'
    raise ParseStatusError(
        f'Неизвестный статус домашней работы "{homework_status}".')


def send_message(bot, message):
    """Отправляет сообщение в чат Telegram."""
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)
    except Exception as error:
        logger.error(f'Сбой при отправке сообщения: "{error}"!')
        raise SendMessageError(f'Сбой при отправке сообщения: "{error}"')
    else:
        logger.debug('Сообщение успешно отправлено в Telegram!')


def main():
    """Основная логика работы бота."""
    if not check_tokens():
        sys.exit('Программа принудительно остановлена!')

    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    timestamp = int(time.time())
    last_error_message = None

    while True:
        try:
            response = get_api_answer(timestamp)
            homeworks = check_response(response)
            if homeworks:
                homework = homeworks[0]
                message = parse_status(homework)
                send_message(bot, message)
            else:
                logger.debug('Новый статус домашних работ отсутствует.')
            timestamp = response['current_date']
            last_error_message = None
        except Exception as error:
            error_message = f'Сбой в работе программы Бота: "{error}"'
            logger.error(error_message)
            if error_message != last_error_message:
                send_message(bot, error_message)
                last_error_message = error_message
        finally:
            time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    main()
