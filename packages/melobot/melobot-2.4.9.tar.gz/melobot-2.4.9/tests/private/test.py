import structlog


processors = [
    structlog.stdlib.add_logger_name,
    structlog.stdlib.add_log_level,
    structlog.stdlib.PositionalArgumentsFormatter(),
    structlog.processors.TimeStamper(
        fmt='%Y-%m-%d %H:%M:%S' if log_console else 'iso'),
    structlog.processors.StackInfoRenderer(),
    structlog.processors.format_exc_info,
]
if log_console:
    processors.append(structlog.dev.ConsoleRenderer())
else:
    processors.append(structlog.processors.JSONRenderer())
structlog.configure(
    processors=processors,
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

# Lib logger to info level.
logger = structlog.get_logger('mylibrary')
logger.setLevel(logging._nameToLevel.get(
    self.config['log_level'], logging.INFO))

# Set handler and level to root logger.
logging.root.setLevel(logging.WARNING)
if log_console:
    logging.root.addHandler(logging.StreamHandler(sys.stdout))
else:
    logging.root.addHandler(
        logging.handlers.TimedRotatingFileHandler(
            self.config['logfile'], encoding='utf-8',
            # Rotate logfiles weekly on Monday, keep last 10 weeks.
            when='W0', atTime=datetime.time(0, 0, 0), backupCount=10))