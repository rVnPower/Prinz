import discord
import time
import traceback
from datetime import datetime, timezone, timedelta


def responsible(target, reason):
    responsible = f"{target} -"
    if reason is None:
        return f"{responsible} no reason."
    return f"{responsible} {reason}"
