"""Common utility functions and classes"""

import docker
import time
import os
from datetime import datetime
import subprocess
from pathlib import Path

# import mysql
# import mysql.connector
# from mysql.connector import Error

from exec_engine.execution_engine import python_containerize_and_execute
from exec_engine.db_manager import DBManager

ROOT_FOLDER_PATH = os.path.dirname(Path(os.path.realpath(__file__)).parent)
DEFAULT_CHECKPOINT_PATH = os.path.join(ROOT_FOLDER_PATH, 'checkpoints')

def format_container_logs(container):
    docker_out = []
    for log in container.logs(stdout=True, stderr=False, stream=True):
        log = log.decode("utf-8")
        if log == "\n":
            continue
        else:
            if log[-1] == "\n":
                log = log[:-1]
            docker_out.append(log)
    
    docker_debug = container.logs(stdout=False, stderr=True).decode("utf-8")
    return docker_out, docker_debug

def export_db(db_manager: DBManager, output_dir=DEFAULT_CHECKPOINT_PATH):
    configs = db_manager.connection_config
    os.makedirs(output_dir, exist_ok=True)

    database_name = configs['database']
    user = configs['user']
    password = configs['password']
    output_file = os.path.join(output_dir, f"database_dump.sql")

    # Command to dump the database
    dump_command = f"mysqldump -u {user} -p{password} {database_name} > {output_file}"

    # Execute the command
    subprocess.call(dump_command, shell=True)

def generate_container_exec_code(api_call, neg_api_call):
    reversion_tester_file = os.path.join(ROOT_FOLDER_PATH, "exec_engine/db_reversion_test.txt")
    with open(reversion_tester_file, "r") as file:
        script = file.read()


    exec_code = '''
api_call = """{}"""
neg_api_call = """{}"""

# Execute api pair on new
execute_commands(config_new, [api_call, neg_api_call])

# Compare new and original db to see if reversion worked
print(compare_databases(config_orig, config_new))
'''.format(api_call, neg_api_call)
    
    return script + exec_code

