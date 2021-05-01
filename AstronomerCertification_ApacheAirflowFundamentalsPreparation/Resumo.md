# AirFlow Certification

- Basics
    - Essentials
        - Why AirFlow

            Criar, monitorar e gerenciar diversos pipelines com mais facilidade

        - What is AirFlow
            - Ferramenta openSource para automatiza workflows de **Author**, **Schedule** e **Monitor**.
            - Altamente escalavel
            - Altamente interativo ( User Interface / CLI)

            Altamente extensivel

            Altamente configuravel

            AirFlow NÃO é um framework de Streaming ou de Processamento de dados

            Dynamic!

            Usa Python

    - Airflow 2
        - mudar DockerFile
            - FROM [quay.io/astronomer/ap-airflow:2.0.0-2-buster-onbuild](http://quay.io/astronomer/ap-airflow:2.0.0-2-buster-onbuild)
            - astro dev stop && astro dev start
        - OBS:
            - Quando o webser e o scheduler ficar reinicializando
                - Reiniciar o Cluster
                    - astro d kill
                    - astro d start
    - Principais Components
        - Webserver
            - Flusk Server
            - User Interface
        - Metadata Database
            - Users
            - Jobs
            - Variables
            - Connections
            - Qualquer dado ligado ao AirFlow
        - Scheduler
            - Para  programar as tarefas
            - obs: Com mongoDB não roda vários schedulers ao mesmo tempo
    - Other Components
        - Executor
            - Define **como** sua tarefa vai ser executada pelo airflow e em qual sistema e tem uma fila para cada executor para ordenar sua tarefa
        - Worker
            - Define **onde** sua tarefa vai ser executada
            - É um processo ou subprocesso onde sua tarefa vai ser executada
    - Architetures
        - Single Node Architeture
            - Web Server pega dados do metastore para mostrá-los no user interface
            - Scheduler interage com o metastore e muda o status da tarefa a ser executada e cria a instancia da tarefa que será enviada para o Executor
            - Executor pega os dados do scheduler para saber como rodar as tarefas gerando as filas para que os workers rodem as tarefas
            - Ao finalizar a tarefa o Executor atualiza os dados no metastore que vai ser mostrado no Web Server ( User Interface)
        - Multi Node Architeture (Celery)
            - Node 1
                - Web Server
                - Scheduler
                - Executor
            - Node 2
                - Metastore
                - Fila
            - Worker nodes fora dos nodes pegam as tarefas das filas ( escalável aumentando o númedo dos worker nodes)
    - Core concepts
        - DAG
            - É um Data Pipeline
            - DAG - Directed Acyclic Graph (no Loop)
            - Operator
                - Tarefa em uma DAG (objeto)
                - 3 Tipos de Operator
                    - Action Operators: Executar algo no Data Pipeline
                    - Transfer Operators: Transfere data de uma origem para um destino
                    - Sensor Operator: Espera algo acontecer para começar outra tarefa
            - A tarefa é uma instancia de um operador
                - A Instância de uma tarfa é representada por uma tarefa específica quando: DAG + Tarefa + Trigger do Schedule
            - Dependências
                - Conceito de sequencialidade dos operadores
                - set_upstream  or set_downstream  (<< or >> boas maneiras)
            - Workflow
                - Combinação dos conceitos anteriores
    - Life Cycle
        1. adiciona [dag.py](http://dag.py) na pasta de DAGS
        2. [dag.py](http://dag.py) parsed no webserver ( a cada 30 segundos) e no scheduler ( a cada 5 minutos)
        3. Scheduler cria um objeto Dagrun no Metastore
        4. Scheduler cria a instancia da tarefa e manda para o executor quando 
        5. Executor pega a tarefa e manda para o worker
        6. Executor atualiza o status da instancia da tarefa no Metastore
        7. WebServer atualiza o UI
    - Installing
        - Constraint file checklist
            - export AIRFLOW_VERSION=2.0.0
            - PYTHON_VERSION="$(python --version | cut -d " " -f 2 | cut -d "." -f 1-2)" ou PYTHON_VERSION="$(python3 --version | cut -d " " -f 2 | cut -d "." -f 1-2)"
            - export CONSTRAINT_URL="[https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt](https://raw.githubusercontent.com/apache/airflow/constraints-$%7BAIRFLOW_VERSION%7D/constraints-$%7BPYTHON_VERSION%7D.txt)"
            - pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
            - export AIRFLOW_HOME=/opt/airflow
            - export PATH=$PATH:~/.local/bin
            - python -m airflow ou python3 -m airflow
            - airflow db init
            - airflow users create \
                --username admin \
                --firstname Peter \
                --lastname Parker \
                --role Admin \
                --email spiderman@superhero.org
            - airflow webserver --port 8080
            - Documentacao

                [Running Airflow locally - Airflow Documentation](https://airflow.apache.org/docs/apache-airflow/stable/start/local.html)

        - Installing Extras:

            Providers - adiciona funcionalidades para o airflow (operator / hooks)

            Extras - Instala providers e/ ou  todas as dependencias necessarias para funcionalidades

    - Updating
        - Backup
            - SQLITE3
                - sqlite3 airflow.db
                - .database
                - .backup backup_sqlite.sq3
                - mkdir backups
                - mv backup_sqlite.sq3 backups/backup_sqlite.sq3
        - export AIRFLOW_VERSION=2.0.1
        - pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
        - airflow db upgrade
- The 3 Ways
    - CLI
        - Comandos
            - docker ps
            - docker exec -it <container> bash
            - airflow db init (inicia um metadata database)
                - [https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html#init](https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html#init)
            - airflow db upgrade ( atualiza o metadata ddatabase para  ac versão mais recente)
                - [https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html#upgrade](https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html#upgrade)
            - airflow db reset ( apaga e recria o metadata database)
                - [https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html#reset](https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html#reset)
            - airflow webserver ( inicia uma isntancia do webserver)
                - [https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html#webserver](https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html#webserver)
            - airflow scheduler ( inicia uma instancia do scheduler)
                - [https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html#scheduler](https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html#scheduler)
            - airflow celery worker ( multiple machines)
                - [https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html#worker](https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html#worker)
            - airflow dags pause
                - [https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html#unpause](https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html#unpause)
            - airflow dags unpause
                - [https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html#unpause](https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html#unpause)
            - airflow dags trigger
                - [https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html#trigger](https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html#trigger)
            - airflow dags list (lista as dags)
                - [https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html#list_repeat2](https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html#list_repeat2)
            - airflow tasks list  <nome da dag> ( lista as tarefas)
                - [https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html#list_repeat6](https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html#list_repeat6)
            - airflow tasks test <dag id task id data>
                - testa a tarefa
                - executar sempre que adicionar uma tarefa no dag
                - checa sem precisar de dependencias,
                - best practices
                - [https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html#test_repeat1](https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html#test_repeat1)
            - airflow dags backfill -s <initial date> -e (final date> —reset-dagruns <nome da dag>
                - [https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html#backfill](https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html#backfill)
    - User Interface
        - Toggle - Pause/Unpause dag (precisa ativar até pra rodar manualmente)
        - name - nome do dag
        - owner - autor do dag
        - runs - status do dag runs
        - schedule - frequencia com que vai rodar o dag
        - last run - data que rodou pela ultima vez
        - recent tasks - status dos ultimos dags rodados
        - actions - ações  como rodar o dag manualmente, atualizar ou deletar o DAG (nao deleta o arquivo)
        - links
            - Tree view
                - Mostra o histórico e os dag runs atuais
                    - Circulo Dag Runs
                    - Quadrado tarefa
            - Graph View
                - Checar as dependencias do data pipeline
                - Checar o status das tarefas
                - Visualização melhor dos relacionamentos na sua DAG
                - Clicando em cada tarefa pode ter acesso a:
                    - Detalhes da Instancia
                    - Renderizado
                    - Logs
                    - Todas as Instâncias
                    - Filtro de Upstream
                    - Ações das Tarefas ( Task Actions)
                        - Run (não pode com o local executor ainda, só com celery ou kubernetes)
                        - Clear (restarta a instancia)
                        - Mark Failed (Testa como se comporta quando falha)
                        - Mark Sucess (Testa como se comporta quando tem sucesso)
            - Gantt View
                - Analizar a duração e o paralelismo das tarefas
                - Identificar gargalos
    - Rest API
        - Stable (airflow 2)
        - [https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html#section/Overview](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html#section/Overview)
- Dags and tasks
    - DAG Basics
    - Monitoring
        - 
    - XCOMS
        - Cross comunication
        - compartilhar dados entre tarefas
        - sqlLite ate 2gb
        - postgres 1 gb
        - mysql 64 kbytes
    - Connections
- The executor Kingdom
    - Executors
        - Sequential Executor
            - Executor padrão
            - Uma única tarefa por vez
        - Local Executor
            - Varias tarefas
        - Celery Executor
            - Várias maquinas para implementar a arquitetura multi node
    - Parallelism
        - Parallelism
            - default = 32
            - Maximo de tarefas em paralelo no Airflow por completo
        - dag_concurrency
            - default = 16
            - Maximo de tarefas em paralelo em para um dag em todos os dag runs
        - max_active_runs_per_dag
            - default = 16
            - Maximo de dag runs rodando ao mesmo tempo
        - dag parameters (dag especifico)
            - max_active_runs
                - Dag runs em paralelo para um dag especifico
            - concurrency
                - Maximo de tarefas em paralelo para um dag especifico

## Checklist astrocli project

- mkdir astro
- cd astro
- astro dev init
- astro dev start
- astro dev ps