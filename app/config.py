from loguru import logger, Logger
from app.const import (
    DB_LOG_PATH, 
    DB_LOG_LEVEL, 
    COMMON_LOG_FORMAT,
    ROTATION_LIMITER,
    RETENTION_COUNT,
    COMPRESSION_FORMAT
    
)

## Консольный логгер остается активным для удобства

DbLogger: Logger = logger.add(
    sink=DB_LOG_PATH,
    level=DB_LOG_LEVEL,
    format=COMMON_LOG_FORMAT,
    rotation=ROTATION_LIMITER,
    retention=RETENTION_COUNT,
    compression=COMPRESSION_FORMAT
)

