# hello_airflow.py
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.contrib.hooks.slack_webhook_hook import SlackWebhookHook

import utils.slack_monkey_patch

utils.slack_monkey_patch.apply_monkey_patch_if_needed()


def notify_error(context):

    SlackWebhookHook(
      http_conn_id='slack_playing_ml',
      channel='ml',
      icon_emoji=':cat:',
      message=''' Task: {task_id} failed '''.format(task_id=context.get('task_instance').task_id)
    ).execute()


def notify_success(context):
    SlackWebhookHook(
        http_conn_id='slack_playing_ml',
        message=''' Task: {task_id} successed '''.format(task_id=context.get('task_instance').task_id),
        channel='ml',
        icon_emoji=':dog:'
    ).execute()


default_args = {
    'owner': 'duan',
    'depends_on_past': False,
    'start_date': datetime(2019, 7, 24, 10, 0, 0),  # DAGの実行開始日時
    'schedule_interval': timedelta(days=1),  # 実行間隔
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
    'provide_context': True,
    'on_success_callback': notify_success,
    'on_failure_callback': notify_error,
}

# DAGのID指定
dag_id = 'first_dag'

with DAG(
        dag_id,
        default_args=default_args
) as dag:
    t1 = BashOperator(
        task_id='t1',
        bash_command='echo t1',
        dag=dag)

    t2 = BashOperator(
        task_id='t2',
        bash_command='exit 1',
        retries=3,
        dag=dag)

    t3 = BashOperator(
        task_id='t3',
        bash_command='echo "{{ params.greeting }}"',
        params={'greeting': 'Hello, AirFlow!'},
        dag=dag)

    t4 = BashOperator(
        task_id='t4',
        bash_command='echo t4',
        dag=dag)

# タスク間に依存関係を定義する
t2.set_upstream(t1)
t3.set_upstream(t1)
t4.set_upstream([t2, t3])
