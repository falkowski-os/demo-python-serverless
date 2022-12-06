import logging
import os
from ...base.db import get_session
from src.handlers.commons.response import Response
from http import HTTPStatus

logging.basicConfig(encoding='utf-8', level=os.getenv('LOG_LEVEL', logging.INFO))
log = logging.getLogger()


def abstract_handler(event, context, function):
    try:
        log.debug("Received function event: %s", event)
        session = get_session()
        response = function(event, context, session)
        session.commit()
        log.debug("Returning response: %s", response.result())

    except ValueError:
        log.exception("Value exception during the execution of the function due to wrong arguments")
        response = Response(HTTPStatus.BAD_REQUEST, "Invalid arguments")

    except Exception:
        log.exception("Exception during the execution of the function")
        response = Response(HTTPStatus.INTERNAL_SERVER_ERROR,
                            "Internal Server problem during the execution, try later again.")

    return response.result()
