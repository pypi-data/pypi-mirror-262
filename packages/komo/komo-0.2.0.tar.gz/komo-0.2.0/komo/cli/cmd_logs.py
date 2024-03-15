import time

import click

from komo import printing
from komo.core import get_job, print_job_logs
from komo.types import JobStatus


@click.command("logs")
@click.option("--follow", "-f", is_flag=True, default=False)
@click.argument(
    "job_id",
    type=str,
)
def cmd_logs(
    follow: bool,
    job_id: str,
):
    print_job_logs(job_id, follow)
