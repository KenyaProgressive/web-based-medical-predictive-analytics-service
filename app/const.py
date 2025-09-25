import os
from dotenv import load_dotenv

load_dotenv()

## ENV VARS

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")


## TODO: впоследствии DB VARS перенести в .env 
## DB VARS
LOCALHOST_ADDRESS: str = "127.0.0.1"
PORT: int = 5433

DB_CONNECTION_LINK: str = f"postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{LOCALHOST_ADDRESS}:{PORT}/{POSTGRES_DB}"

## LOGGERS CONF

DB_LOG_PATH: str = "app/logs/db_logs/db_log.log" ## Путь для сохранения логов ДБ-логгера
COMMON_LOG_PATH: str = "app/logs/common/common_log.log" ## Путь для сохранения логов main-логгера
COMMON_LOG_LEVEL: str = "DEBUG" ## Минимальный лог-левел для всех логгеров
COMMON_LOG_FORMAT: str = "{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}" ## Формат вывода логов для всех логгеров
RETENTION_COUNT: int = 10 ## Хранится последних 10 лог файлов
ROTATION_LIMITER: str = "5MB" ## При достижении 5 МБ логов в одном файле, создастся новый
COMPRESSION_FORMAT: str = "zip" ## Сжатие логов в .zip после ротации

## MESSAGES

SUCCESS_CLOSE_POOL_MESSAGE: str = "Пул соединений успешно закрыт"
POOL_DOESNT_EXIST_OR_CLOSED: str = "Пул не существует или уже был закрыт"


NO_ARGS: tuple = () ## Пустой кортеж для передачи в db_master при отсутствии аргументов




