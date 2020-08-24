"""
Redis queue for manage background proccess.
"""

from datetime import datetime, timedelta

import redis
from rq import Queue, Connection, Retry, Worker

from config import settings  # pylint: disable-msg=E0611


def create_job(function: callable, time_delta: timedelta = None, date_time: datetime = None) -> str:
    """
    Add a new Job to Queue.

    Params:
    ------
    function: callable - The job function
    date_time: datetime - The specific time when the job must be executed
    time_delta: timedelta - The time to excecute the job

    Return:
    ------
    job_id: str - The specifc job id
    """

    with Connection(redis.from_url(settings.REDIS_URL)):
        redis_queue = Queue("email")

        if date_time:
            job = redis_queue.enqueue_at(
                date_time,
                function,
                retry=Retry(max=3, interval=[10, 30, 60])
            )
        elif time_delta:
            job = redis_queue.enqueue_in(
                time_delta,
                function,
                retry=Retry(max=3, interval=[10, 30, 60])
            )
        else:
            raise AttributeError("Some time specification id needed")

    return str(job.get_id())


def __run_worker():
    """
    Start a worker to manage the enqueue jobs.
    """
    redis_url = "redis://redis:6379/0"
    redis_connection = redis.from_url(redis_url)
    with Connection(redis_connection):
        worker = Worker(settings.QUEUES, name="unu-worker")
        worker.work(with_scheduler=True)


if __name__ == "__main__":
    print(" -- Redis Worker starting -- ")
    __run_worker()
