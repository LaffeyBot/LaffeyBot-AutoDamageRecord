from apscheduler.schedulers.asyncio import AsyncIOScheduler
from do_fetch import do_fetch
from scheduler import record_task
import config
import logging
import asyncio
from report.login import login
from scheduler import load_all
import apscheduler
import pytesseract
import os

scheduler = AsyncIOScheduler()
header = login(config.USERNAME, config.PASSWORD)
global is_loading
is_loading = True


@scheduler.scheduled_job('interval', seconds=config.FETCH_INTERVAL)
async def scheduled():
    log.log(1, '开始任务')
    if is_loading and do_fetch():
        await load_all(header=header)
        is_loading = False
        return
    if do_fetch():
        await record_task(header=header)


log = logging.getLogger('apscheduler.executors.default')
log.setLevel(logging.INFO)  # DEBUG

fmt = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
h = logging.StreamHandler()
h.setFormatter(fmt)
log.addHandler(h)

scheduler.start()

try:
    asyncio.get_event_loop().run_forever()
except (KeyboardInterrupt, SystemExit):
    pass
