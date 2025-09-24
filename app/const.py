LOCALHOST_ADDRESS: str = '127.0.0.1'

DB_LOG_PATH: str = "app/logs" ## Путь для сохранения логов ДБ-логгера
COMMON_LOG_LEVEL: str = "DEBUG" ## Минимальный лог-левел для всех логгеров
COMMON_LOG_FORMAT: str = "{time} | {level} | {name}:{function}:{line} | {message}" ## Формат вывода логов для всех логгеров
RETENTION_COUNT: int = 10 ## Хранится последних 10 лог файлов
ROTATION_LIMITER: str = "5MB" ## При достижении 5 МБ логов в одном файле, создастся новый
COMPRESSION_FORMAT: str = "zip" ## Сжатие логов в .zip после ротации



## MESSAGES

SUCCESS_CLOSE_POOL_MESSAGE: str = "Пул соединений успешно закрыт"
POOL_DOESNT_EXIST_OR_CLOSED: str = "Пул не существует или уже был закрыт"