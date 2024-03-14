"""This module will execute API calls and their reversals."""

import subprocess
from exec_engine.db_manager import DBManager

from exec_engine.credentials.credentials_utils import creds_from_prompt, CREDS_FOLDER_PATH
from exec_engine.docker_sandbox import *

class APIExecutor:
    """Base Class for all API executors

    Should be stateless and should not have any attributes.

    Attributes:
        None
    
    Methods:
        execute_api_call: Execute API call
    """
    def __init__(self):
        return None
    
    def execute_api_call(self, command: str) -> int:
        """Execute API call.
        
        Args:
            command (str): API call to execute.
        """
        raise NotImplementedError
    
    def set_execution_environment(self, env, docker_sandbox: DockerSandbox = None):
        if env == "local":
            self.env = "local"
            return
        elif env == "docker":
            self.env = "docker"
            self.docker_client = "docker_client"
            return
        else:
            print('env can only be set to "docker" or "local"')
    

class BashAPIExecutor(APIExecutor):
    """Executes Bash API calls
    
    Methods:
        execute_api_call: Execute API call
    """
    def __init__(self):
        return None
    
    def execute_api_call(self, command: str) -> int:
        """Execute API call.
        
        Args:
            command (str): API call to execute.
        """
        return subprocess.call(command, shell=True)

class PythonAPIExecutor(APIExecutor):
    """Executes Python API calls
    
    Methods:
        execute_api_call: Execute API call
    """
    def __init__(self, docker_sandbox: DockerSandbox = None):
        self.env = None
        self.docker_sandbox = docker_sandbox

    def prepare_credentials(self, prompt:str, technique="lut"):
        credentials = creds_from_prompt(prompt, CREDS_FOLDER_PATH, technique)
        try:
            services = [service_name for service_name, value, file_type in credentials]
        except:
            raise Exception("Error: credentials have to be passed in as a list of [service_name, value, cred_type] pairs")
        return credentials, services



    
    def execute_api_call(self, command: str, credentials: list = None) -> int:
        """Execute API call.
        
        Args:
            command (str): API call to execute.
        """
        image_id = self.docker_sandbox.create_image_from_python_code(command)
        result = self.docker_sandbox.create_python_sandbox(command, image_id, credentials=credentials)

        return result



