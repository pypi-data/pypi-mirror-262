# Python Library for Sesam Workflows

This Python library is designed to streamline the development and execution of Sesam-integrated workflows. It supports both local systems and OneCompute cloud platforms.

## Usage and Examples

For a more comprehensive understanding and additional examples, please visit the Homepage link provided on this page.

```python
"""Demonstration of executing a SesamCoreCommand using the OneWorkflow client asynchronously."""

# Import necessary modules and functions
import asyncio
from dnv.oneworkflow.utils import (
    CommandInfo,
    one_workflow_client,
    run_managed_commands_parallelly_async,
)
from dnv.sesam.commands import SesamCoreCommand

# Instantiate the OneWorkflow client with workspace ID and path
client = one_workflow_client(
    workspace_id="TestWorkflow", workspace_path=r"C:\MyWorkspace", cloud_run=False
)

# Create an instance of the SesamCoreCommand class, specifying the command, input file name, and options
sesam_core_command = SesamCoreCommand(
    command="uls", input_file_name="input.json", options="-v"
)

# Create an instance of the CommandInfo class, specifying the commands and load case folder name
cmd_info = CommandInfo(
    commands=[sesam_core_command],
    load_case_foldername="LoadCase1",
)

# Run the workflow/command asynchronously using the run_managed_commands_parallelly_async function
asyncio.run(
    run_managed_commands_parallelly_async(
        client=client,
        commands_info=[cmd_info],
    )
)
```
