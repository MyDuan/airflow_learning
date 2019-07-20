# hello_airflow.py
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

# DAGを作る
default_args = {
    'owner': 'ohke',
    'depends_on_past': False,
    # 最初のタスクの実行日時は、start_dateではなく、start_date+schedule_intervalとなる
    # イメージとしては、start_dateで指定した日時からデータが蓄積され始め、schedule_intervalが経過したらdailyであれば1日分のデータを処理を行う感じ
    'start_date': datetime(2018, 4, 21, 10, 0, 0), # DAGの実行開始日時
    'schedule_interval': timedelta(days=1), # 実行間隔
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# DAGのID指定
dag_id = 'first_dag'

dag = DAG(dag_id, default_args=default_args)

# DAGと紐づくタスクを作る
# BashOperator は シェルスクリプトが実行できるoperator
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
    dag=dag
)

# タスク間に依存関係を定義する
t2.set_upstream(t1)
t3.set_upstream(t1)
t4.set_upstream([t2, t3])
