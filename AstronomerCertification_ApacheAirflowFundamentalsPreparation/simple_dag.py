from airflow import DAG

from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.sensors.filesystem import FileSensor
from airflow.utils.dates import days_ago
from airflow.models.baseoperator import chain, cross_downstream

from datetime import datetime, timedelta

default_args = {
    'retry': 5
    ,'retry_delay': timedelta(minutes=5)
    ,'email_on_failure': True
    ,'email_on_retry': True
    ,'email': 'flavio10nb@hotmail.com'
}

def _downloading_data(ti, **kwargs):
#def _downloading_data(my_param, ds):
    #print(kwargs) # Todo o contexto do DAG em execução
    #print(ds) # Data de execução do DAG
    #print(my_param) # Passar se parametro no log

    with open('/tmp/my_file.txt', 'w') as f:
        f.write('my_data')

    ti.xcom_push(key='my_key', task_ids=['doanloading_data'])

    return 42

def _checking_data(ti):
    my_xcom = ti.xcom_pull(key='return_value', task_ids=['downloading_data'])
    print(my_xcom) 

def _failure(context):
    print("On callback failure")
    print(context)

with DAG(dag_id='simple_dag', default_args=default_args, schedule_interval="*/10****", 
    start_date=datetime(2021, 1, 1), catchup=True, max_active_runs=2) as dag:

    # DummyOperators
    '''
    task_1 = DummyOperator(
        task_id = 'task_1'
        #start_date=datetime(2021, 1 , 2)
    )

    task_2 = DummyOperator(
        task_id = 'task_2',
        #start_date=datetime(2021, 1 , 2)
        retry=3
    )

    task_3 = DummyOperator(
        task_id = 'task_3'
        #start_date=datetime(2021, 1 , 2)
    )
    '''

    # PythonOperators
    downloading_data = PythonOperator(
        task_id='downloading_data',        
        python_callable=_downloading_data
        #op_kwargs={'my_param': 42}
    )

    checking_data = PythonOperator(
        task_id = 'checking_data'
        ,python_callable=_checking_data
    )

    wating_for_data = FileSensor(
        task_id = 'wating_for_data'
        ,fs_conn_id = 'fs_default' #Id da conexao necessaria para o FileSensor 
        ,filepath = 'my_file.txt'
        #poke_interval=15 #Verifica a cada 15 segundos, se a condição 
    )

    processing_data = BashOperator(
        task_id = 'processing_data'
        #,bash_command='exit 0' # 0 Retorno de Sucesso
        ,bash_command='exit 1' # 1 Retorno de Error
        ,on_failure_callback=_failure
    )

    # Dependencias entre as TASKS
    downloading_data.set_downstream(wating_for_data)
    wating_for_data.set_downstream(processing_data)

    # Mesmas dependencias que antes
    processing_data.set_upstream(wating_for_data)
    wating_for_data.set_upstream(downloading_data)

    # Outra forma de indicar dependencias 
    downloading_data >> wating_for_data >> processing_data

    # Execuutando em paralelo, apos o downloading_data
    downloading_data >> [wating_for_data, processing_data]

    # Outra forma de indicar dependencias 
    chain(downloading_data, wating_for_data, processing_data)

    # Cruzamento de dependencias 
    # (processing_data depende de checking_data e donloading_data)
    # (wating_for_data depende de checking_data e donloading_data)
    cross_downstream([downloading_data, checking_data], [wating_for_data, processing_data])
    
    # Nao é possivel criar dependencias entre duas listas de TASKS
    [downloading_data, checking_data] >> [wating_for_data, processing_data]

    # XComs - “comunicação cruzada” e permite a troca de mensagens ou pequenas quantidades de dados entre tarefas. 
    # Não utilizar XComs como um framework de processamento


# ------------------------------------------------------------------------------------------------------

# start_date:

    # Data em que o DAG começará a ser agendado

    # TIMEZONE
    # with DAG(dag_id='simple_dag', start_date=datetime(2020, 1, 1, 20)) as dag:
                                                     #ANO, MES, DIA, TIMEZONE

    # NUNCA FAÇA ISSO:
    # with DAG(dag_id='simple_dag', start_date=datetime.now()) as dag:

# schedule_interval: 

    # O intervalo de tempo a partir do 'start_date' mínimo em que queremos que nosso DAG seja acionado.

    # Verificar 'schedule expression' -> https://crontab.guru/
    # "*/10 * * * *" -> A cada 10 min
    # @daily -> todos os dias
    # @weekly -> toda semana 
    # timedelta(days=1) -> A cada 01 dia
    # timedelta(hours=7) -> A cada 7 horas
    # None -> Nunca será automaticamente

    # crontab expression vs timedelta:
        # Crontab Expression = É absoluta. Ex: Sua DAG sempre as 7 PM.
        # Timdelta = Ex: Sua DAG executa a cada 7 horas.

# catchup:

    # O Airflow permite que execuções perdidas do DAG sejam programadas novamente para que os pipelines acompanhem as programações que foram perdidas por algum motivo. Também permite a reexecução de DAGs na data anterior manualmente e preenche essas execuções.

# backfill:

    # Se por alguma razão quisermos executar os DAGs em certos horários manualmente, podemos usar o seguinte comando CLI para fazê-lo.
    # airflow backfill -s <START_DATE> -e <END_DATE> --rerun_failed_tasks -B <DAG_NAME>

# max_active_runs:

    # Numero de DAGs executando ao mesmo tempo

# Operator:

    # task_id, precisa ser unico
    # Nunca colocar mais de uma TASK no mesmo operador, pois se um falhar você terá que reexecutar as duas TASKs