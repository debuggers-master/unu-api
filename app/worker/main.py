"""
Redis Queue Module - For manage background proccess.
"""

from datetime import datetime, timedelta

import redis
from rq import Queue, Connection, Retry, Worker

from config import settings  # pylint: disable-msg=E0611


###########################################
##         Job Queue (schedule)          ##
###########################################

def create_job(
        function: callable,
        date_time: datetime,
        utc_hours: int = 0,
        queue_name: str = "email",
        **kwargs,
) -> str:
    """
    Add a new Job to Queue.

    Params:
    ------
    function: callable - The job function
    date_time: datetime - The specific time when the job must be executed
    utc_hours: int - Eg: -5 or +2 The specific GTM.
    queue_name: str - The name of the task queue.

    Return:
    ------
    job_id: str - The specifc job id
    """

    with Connection(redis.from_url(settings.REDIS_URL)):
        redis_queue = Queue(queue_name)

        # Fix the correct time to execute.
        utc_to_place_time = datetime.utcnow() + timedelta(hours=utc_hours)
        seconds = date_time - utc_to_place_time
        minutes = seconds.seconds / 60

        # Enqueue the job.
        job = redis_queue.enqueue_in(
            time_delta=timedelta(minutes=minutes),
            func=function,
            kwargs=kwargs,
            retry=Retry(max=3, interval=[10, 30, 60])
        )

        return job.get_id()


###########################################
##          Queue Worker Setup           ##
###########################################

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
