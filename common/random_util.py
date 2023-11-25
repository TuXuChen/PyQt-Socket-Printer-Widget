import datetime
import random


def getCode() -> str:
    current_date = datetime.datetime.now().strftime("%Y%m%d")
    random_number = getRandom()
    return current_date + random_number


def getRandom(length: int = 5):
    return ''.join(random.choices('0123456789', k=length))
