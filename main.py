from apscheduler.schedulers.asyncio import AsyncIOScheduler
from do_fetch import do_fetch
from scheduler import record_task
import config

scheduler = AsyncIOScheduler()


@scheduler.scheduled_job('interval', seconds=config.FETCH_INTERVAL)
async def _():
    if do_fetch():
        await record_task()

scheduler.start()
