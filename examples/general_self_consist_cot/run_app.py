# Import required modules and components
import os
from omagent_core.utils.container import container
from omagent_core.engine.workflow.conductor_workflow import ConductorWorkflow
from omagent_core.engine.workflow.task.simple_task import simple_task
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()  # 加载.env文件中的变量

from omagent_core.utils.registry import registry
from omagent_core.clients.devices.app.client import AppClient
from omagent_core.utils.logger import logging
from agent.input_interface.input_interface import COTInputInterface  # Change to COTInputInterface
from omagent_core.advanced_components.workflow.self_consist_cot.workflow import SelfConsistentWorkflow  # Change to SelfConsistentWorkflow
logging.init_logger("omagent", "omagent", level="INFO")

# Set current working directory path
CURRENT_PATH = root_path = Path(__file__).parents[0]

# Import registered modules
registry.import_module(CURRENT_PATH.joinpath('agent'))

# Load container configuration from YAML file
container.register_stm("RedisSTM")
container.from_config(CURRENT_PATH.joinpath('container.yaml'))

# Initialize simple VQA workflow
workflow = ConductorWorkflow(name='general_self_consist_cot')

# Configure workflow tasks:
# 1. Input interface for user interaction
client_input_task = simple_task(task_def_name=COTInputInterface, task_reference_name='input_interface')  # Change to COTInputInterface

self_consist_cot_workflow = SelfConsistentWorkflow()  # Change to SelfConsistentWorkflow
self_consist_cot_workflow.set_input(user_question=client_input_task.output('user_question'), path_num=client_input_task.output('path_num'))  # Set appropriate inputs

# 6. Conclude task for task conclusion


# Configure workflow execution flow: Input -> Initialize global variables -> Self Consistent Loop -> Conclude
workflow >> client_input_task >> self_consist_cot_workflow 

# Register workflow
workflow.register(overwrite=True)

# Initialize and start app client with workflow configuration
config_path = CURRENT_PATH.joinpath('configs')
app_client = AppClient(interactor=workflow, config_path=config_path, workers=[COTInputInterface()])
app_client.start_interactor()
