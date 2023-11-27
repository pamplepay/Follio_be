import logging
from typing import List

from django.core.mail import send_mail as _send_mail


def send_email(_from: str, targets_email: List, title: str, body: str) -> bool:
    try:
        response = _send_mail(
            title,
            body,
            _from,
            targets_email,
        )

        if response == 1:
            return True
    except Exception:
        logging.critical(f'* FAIL TO SEND EMAIL')
    return False
