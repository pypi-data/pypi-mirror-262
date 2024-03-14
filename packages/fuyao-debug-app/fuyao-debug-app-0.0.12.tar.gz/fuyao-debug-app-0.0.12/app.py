import click
from db.base_fuyao_db import get_job_info
from utils.fuyao_log_ali import get_fuyao_log, analyze_job_log


@click.group()
def cli():
    pass


@cli.command()
@click.option('--job_name', prompt='Job Name',
              help='The name of a job. Checkout a job name by "fuyao view" or "fuyao history".')
@click.option('--env', prompt='Environment', type=click.Choice(['prd', 'dev']),
              help='prd/dev. To determine which DB will be used.')
@click.option('--log_path', default='.',
              help='The path where tool will put the logs.')
# 1. 检查所有的node的log，是否有exception，分析exception
def check_log_exception(job_name, env, log_path):
    """Simple script to get & analyze job log, then return if there is an exception and corresponding details."""
    click.echo(f"Processing Job: {job_name}")

    # 1. get job info from db
    job_info, code = get_job_info(job_name, env)
    click.echo(f"Job Info: {job_info}, Code: {code}")
    if job_info is None:
        click.echo(f"Job {job_name} not found. Or DB error.")
        return

    # 2. get log data
    log_data = get_fuyao_log(job_info, log_path)

    # 3. analyze log data
    fail_info = analyze_job_log(log_data)
    click.echo(f"Fail Info: {fail_info}")


@cli.command()
# 2. 检查所有worker是否完成初始化
def check_workers_initiation():
    pass


@cli.command()
# 3. 检查是否有worker process 退出
def check_workers_exit():
    pass


@cli.command()
# 4. 自动收集所有rank的stack
def collect_ranks_stack():
    pass


@cli.command()
# 5. 自动收集火焰图
def collect_flame_graph():
    pass


@cli.command()
# 6. 自动检查设备是否出现异常；分析是否存在硬件告警及报错（syslog）
def check_device():
    pass


if __name__ == '__main__':
    cli()
