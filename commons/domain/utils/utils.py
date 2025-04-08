import uuid
from datetime import datetime
from commons.domain.constants.domain_constants import DAYS_OF_WEEK, MONTHS

def generate_uuid() -> str:
    return f"{uuid.uuid4()}"

def get_current_str_datetime():
    current_datetime = datetime.now()
    str_current_datetime = (f"{DAYS_OF_WEEK[current_datetime.weekday()]}, "
                       f"{current_datetime.day} de "
                       f"{MONTHS[current_datetime.month - 1]} de "
                       f"{current_datetime.year}")

    return str_current_datetime

def generate_gcs_uri(bucket: str, folder: str) -> str:
    return f"gs://{bucket}/{folder}"