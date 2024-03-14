# https://gist.github.com/mariocj89/73824162a3e35d50db8e758a42e39aab

import logging
import logging.config
import json

ATTR_TO_JSON = ['created', 'filename', 'funcName', 'levelname', 'lineno', 'module', 'msecs', 'msg', 'name', 'pathname', 'process', 'processName', 'relativeCreated', 'thread', 'threadName']

class JsonFormatter:
    def format(self, record):
        obj = {attr: getattr(record, attr)
                  for attr in ATTR_TO_JSON}
        return json.dumps(obj, indent=4)

handler = logging.StreamHandler()
handler.formatter = JsonFormatter()
logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.error("Hello")
