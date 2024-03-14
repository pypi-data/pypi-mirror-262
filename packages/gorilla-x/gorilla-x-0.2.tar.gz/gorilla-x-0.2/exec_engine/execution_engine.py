"""Docker images/containers management"""

import docker
import logging
from typing import NewType

from exec_engine.container_utils.code_parser import extract_dependencies
import exec_engine.container_utils.container_utils as utils

from exec_engine.credentials.credentials_utils import *

import pandas as pd
# import pyodbc

import os
from pathlib import Path

ROOT_FOLDER_PATH = os.path.dirname(Path(os.path.realpath(__file__)).parent)
DOCKER_FOLDER_PATH = os.path.join(ROOT_FOLDER_PATH, "docker/docker")
DOCKER_REQUIREMENTS_PATH = os.path.join(DOCKER_FOLDER_PATH, "requirements.txt")
DOCKERFILE_PATH = os.path.join(DOCKER_FOLDER_PATH, "dockerfile")
DOCKER_EXECUTION_PATH = os.path.join(DOCKER_FOLDER_PATH, "python_executor.py")

MYSQL_DOCKER_FOLDER_PATH = os.path.join(ROOT_FOLDER_PATH, "docker/mysql_docker")

def get_docker_paths(docker_folder_path):
    requirements_path = os.path.join(docker_folder_path, "requirements.txt")
    dockerfile_path = os.path.join(docker_folder_path, "dockerfile")
    execution_path = os.path.join(docker_folder_path, "python_executor.py")
    
    return requirements_path, dockerfile_path, execution_path

SQL_Type = NewType("SQL_Type", str)
Filesystem_Type = NewType("Filesystem_Type", str)
RESTful_Type = NewType("RESTful_Type", str)
POSIX_Type = NewType("POSIX_Type", str)

logger = logging.getLogger(__name__)

def python_containerize_and_execute(code, client_config={}, image_id=None, auto_save=True, credentials=None, api_type=RESTful_Type):
    if api_type == SQL_Type:
        docker_folder_path = MYSQL_DOCKER_FOLDER_PATH
    else:
        docker_folder_path = DOCKER_FOLDER_PATH

    requirements_path, dockerfile_path, execution_path = get_docker_paths(docker_folder_path)

    try:
        # Search for the local Docker client and configure the base image for the container
        if not client_config:
            client = docker.from_env()
        else:
            client = docker.DockerClient(**client_config)
    except Exception as e:
        if not client_config:
            print(e)
            print("Could not run the script in a container. If you haven't already, please install Docker https://docs.docker.com/get-docker/")
        else:
            print("Unable to initialize a docker client based on client_config {client_config}. Error with error message {error}".format(client_config=client_config, error=e))
        return
    
    if not image_id:
        #generate requirements.txt file
        try:
            extract_dependencies(code, path=requirements_path)
            image_hash = utils.get_files_hash(dockerfile_path, requirements_path, execution_path)
            image_id = utils.find_local_docker_image(image_hash)
        except Exception as e:
            print(e)
            return

        # Run the container using the image specified if exists, else pull the image from docker hub
        try:
            if image_id:
                client.images.get(image_id)
                logger.debug(f"Image '{image_id}' found locally")
        except Exception as e:
            print("Image '{image_id}' not found locally, pulling from Docker Hub...".format(image_id))
            try:
                # Use the low-level API to stream the pull response
                low_level_client = docker.APIClient()
                low_level_client.pull(image_id, stream=True, decode=True)
                client.images.get(image_id)
            except:
                print("Unable to retrieve image form Docker Hub")
                image_id = None
                return
            
        try:
            if not image_id:
                image_id = client.images.build(path=docker_folder_path, dockerfile=dockerfile_path)[0].short_id
                if auto_save:
                    utils.save_image_hash(image_hash, image_id)
        except Exception as e:
            print("Unable to build docker image, returned with error: {error}".format(error=e))
            return
    
    if not credentials:
        volumes = {
                # path on your machine/host
                os.path.abspath("credentials"): {
                    "bind": "/sandbox/credentials",  # path inside the container
                    "mode": "rw",
                }
            }
    else:
        volumes = []
        paths, not_found = get_cred_paths(credentials, CREDS_FOLDER_PATH)
        for service in paths:
            host_path = paths[service]
            container_path = "/sandbox/credentials/" + service
            volumes.append(host_path + ":" + container_path)

    try:
        # Configure the container's setting and run
        logger.debug(f"Running container...")
        container = client.containers.run(
            image_id,
            command = 
                ['python',  'python_executor.py',  'code_execute'],
            environment = {
                "CODE": code
            },
            volumes=volumes,
            stderr = True,
            stdout=True,
            detach=True,
        )
        container.wait()
        docker_out, docker_debug = format_container_logs(container)
        container.remove()

        return {"output": docker_out, "debug": docker_debug}
    except Exception as e:
        print("Failure occured inside client.containers.run with the following error message:", e)
        return
    
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

def sql_execute(code, client_config={}):
    """
    Example usage:
    print(sql_execute(code = 'SELECT * FROM sys.databases;', client_config={'server':'localhost', 'port':'1433', 'user_id':'sa', 'password':'Str0ngPa54213w0rd'}))
    """
    cnxn_str = ("Driver={ODBC Driver 17 for SQL Server};" +
        "SERVER={server};".format(server=client_config['server']) +
        "PORT={port};".format(port=client_config['port']) +
        "UID={user_id};".format(user_id=client_config['user_id']) +
        "PWD={password}".format(password=client_config['password'])
        )
    try:
        cnxn = pyodbc.connect(cnxn_str)  # initialise connection
    except Exception as e:
        raise("Unable to connect to the database server with the inputted configurations, {e}".format(e=e))

    # execute the query and read to a dataframe in Python
    df = pd.read_sql(code, cnxn).to_json()

    return df
