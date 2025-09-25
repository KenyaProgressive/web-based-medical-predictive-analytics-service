import app.config
from loguru import logger
from app.const import (
    DB_LOG_PATH,
    COMMON_LOG_PATH,
    COMMON_LOG_LEVEL, 
    COMMON_LOG_FORMAT,
    ROTATION_LIMITER,
    RETENTION_COUNT,
    COMPRESSION_FORMAT
    
)

## Консольное логирование остается активным для удобства


## БД-логгер -- записывает в app/logs

logger.add(
    sink=DB_LOG_PATH,
    level=COMMON_LOG_LEVEL,
    format=COMMON_LOG_FORMAT,
    rotation=ROTATION_LIMITER,
    retention=RETENTION_COUNT,
    compression=COMPRESSION_FORMAT,
    filter=lambda log: log["extra"].get("component") == "db"
)

DbLogger = logger.bind(component="db")

## Главный логгер -- логирует общие операции и main

logger.add(
    sink=COMMON_LOG_PATH,
    level=COMMON_LOG_LEVEL,
    format=COMMON_LOG_FORMAT,
    rotation=ROTATION_LIMITER,
    retention=RETENTION_COUNT,
    compression=COMPRESSION_FORMAT,
    filter=lambda log: log["extra"].get("component") == "common"
)

CommonLogger = logger.bind(component="common")
