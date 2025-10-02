import os
from dotenv import load_dotenv

load_dotenv()

## ENV VARS

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")

## COMMON

LOCALHOST_ADDRESS: str = "127.0.0.1"
CSV_PATH_1: str = "app/emulator/20250908-07500001_1.csv"
CSV_PATH_2: str = "app/emulator/20250908-07500001_2.csv"

## UVICORN

PORT: int = 8080
APP_PATH: str = "app.backend.app:app"



## TODO: впоследствии DB VARS перенести в .env 
## DB VARS
DB_PORT: int = 5433
NO_ARGS: tuple = () ## Пустой кортеж для передачи в db_master при отсутствии аргументов

DB_CONNECTION_LINK: str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{LOCALHOST_ADDRESS}:{DB_PORT}/{POSTGRES_DB}"
## LOGGERS CONF

DB_LOG_PATH: str = "app/logs/db_logs/db_log.log" ## Путь для сохранения логов ДБ-логгера
COMMON_LOG_PATH: str = "app/logs/common/common_log.log" ## Путь для сохранения логов main-логгера
BACKEND_LOG_PATH: str = "app/logs/backend_logs/backend_log.log"
COMMON_LOG_LEVEL: str = "DEBUG" ## Минимальный лог-левел для всех логгеров
COMMON_LOG_FORMAT: str = "{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}" ## Формат вывода логов для всех логгеров
RETENTION_COUNT: int = 10 ## Хранится последних 10 лог файлов
ROTATION_LIMITER: str = "5MB" ## При достижении 5 МБ логов в одном файле, создастся новый
COMPRESSION_FORMAT: str = "zip" ## Сжатие логов в .zip после ротации

## MESSAGES

SUCCESS_CLOSE_POOL_MESSAGE: str = "Пул соединений успешно закрыт"
POOL_DOESNT_EXIST_OR_CLOSED: str = "Пул не существует или уже был закрыт"

## ML

MIN_TIME: int = 60 * 28
MAX_TIME: int = 60 * 32
