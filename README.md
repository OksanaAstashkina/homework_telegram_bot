# Бот-ассистент для проверки статуса домашней работы.

## Описание:
Telegram-бот для проверки статуса домашней работы на сервисе Практикум.Домашка.

## Функционал:
Telegram-бот раз в 10 минут опрашивает API сервиса Практикум.Домашка и проверяет статус отправленной на проверку домашней работы. Возможные статусы проверки работы: "работа принята на проверку", "работа возвращена для исправления ошибок", "работа принята". При обновлении статуса работы бот анализирует ответ API и отправляет соответствующее уведомление в Telegram-чат. Логирует свою работу в stdout и сообщает о важных проблемах сообщением в Telegram. Каждое сообщение в журнале логов состоит из даты и времени события, уровня важности события и описания события.

Бот работает как на ПК, так и на платформе PythonAnywhere, достаточно запустить бота, прописать токены. 

## Технологии
* Python 3.9
* python-telegram-bot
* python-dotenv
* requests

## Установка и запуск бота на локальном компьютере из репозитория GitHub

__Создаем Telegram-бота и получаем токен__:

* В мессенджере Telegram начните диалог с ботом @BotFather: нажмите кнопку Start («Запустить»). 

* Затем отправьте команду /newbot и укажите параметры бота. 

* После создания скопируйте полученный токен.

__Узнаем ID своего аккаунта в Telegram для получения сообщений__:

* В мессенджере Telegram начните диалог с ботом @userinfobot: нажмите кнопку Start («Запустить»). 

*  После получения сообщения от бота скопируйте полученный ID.

__Клонируем репозиторий себе на компьютер__: 
```
git clone git@github.com:OksanaAstashkina/homework_telegram_bot.git
```

__Переходим в директорию с клонированным репозиторием__:
```
cd homework_telegram_bot
```

__Разворачиваем в репозитории виртуальное окружение__:
```
python -m venv venv (для Linux и MacOS: python3 -m venv venv)
```

__Активируем виртуальное окружение__:
```
source venv/Scripts/activate (для Linux и MacOS: source venv/bin/activate)
```

__Установаем зависимости__:
```
pip install -r requirements.txt
```

__Создаем файл .env с переменными окружения__:
```
touch .env &&
echo PRACTICUM_TOKEN=YOUR_PRAKTIKUM_TOKEN > .env &&
echo TELEGRAM_TOKEN=YOUR_TELEGRAM_TOKEN >> .env &&
echo TELEGRAM_CHAT_ID=YOUR_CHAT_ID >> .env
```
Не забудьте заменить значения переменных на свои: 

*  YOUR_PRAKTIKUM_TOKEN - токен для взаимодействия с API сервиса проверки домашней работы,

*  YOUR_TELEGRAM_TOKEN - токен для Телеграмм-бота,

*  YOUR_CHAT_ID - ID вашего аккаунта в Телеграмм, куда будут приходить уведомления от бота.

__Запускаем бота__:
```
python homework.py
```
В данном случае бот будет непрерывно работать только на включенном компьюетере с запущенным скриптом в терминале.


## Деплой бота на PythonAnywhere:

* Зарегистрируйтесь на сайте [www.pythonanywhere.com](https://www.pythonanywhere.com/registration/register/beginner/). После регистрации вы окажетесь на странице Dashboard.
* Перейдите во вкладку Files и загрузите в текущую директорию файлы, необходимые для запуска и работы проекта (репозиторий homework_telegram_bot).
* Затем перейдите во вкладку Consoles и запустите новую консоль Bash.
* В открывшейся консоли выполните запуск бота, для чего при помощи команды cd перейдите в папку с файлом homework.py и выполните команды установки зависимостей и запуска проекта:
```
python -m venv venv (для Linux и MacOS: python3 -m venv venv)
source venv/Scripts/activate (для Linux и MacOS: source venv/bin/activate)
pip install -r requirements.txt
python homework.py
```
Бот начнёт работу, а вы можете вернуться к главной странице сервиса. Консоль будет работать в фоновом режиме. Консоль можно закрыть, при этом выполнение программы-бота прекратится.


***
## *Автор*
Оксана Асташкина - [GitHub](https://github.com/OksanaAstashkina)

### *Дата создания*
Апрель, 2023 г.
