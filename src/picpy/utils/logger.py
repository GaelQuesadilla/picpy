from loguru import logger

logger.add("logs.log", rotation="1 week")

if __name__ == "__main__":
    logger.info("Logger OK")
