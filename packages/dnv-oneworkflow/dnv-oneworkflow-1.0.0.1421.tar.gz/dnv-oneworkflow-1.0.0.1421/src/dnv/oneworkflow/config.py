"""
This module defines data classes for configuring OneCompute workflows.
"""
import os
import uuid
from dataclasses import dataclass


@dataclass
class WorkspaceConfiguration:
    """
    A data class that represents the configuration for a workspace.

    Attributes:
        workspace_id (str): The ID of the workspace.
        workspace_path (str): The path to the workspace directory.
        common_files_directory (str): The name of the directory where common files are stored.
        load_cases_parent_directory (str): The name of the parent directory where load cases are
            stored.
        results_directory (str): The name of the directory where results are stored.
    """

    workspace_id: str = str(uuid.uuid4())
    workspace_path: str = ""
    common_files_directory: str = ""
    load_cases_parent_directory: str = ""
    results_directory: str = ""

    @property
    def common_files_fullpath(self) -> str:
        """
        Get the full path to the directory where common files are stored.

        Returns:
            str: The full path to the directory containing common files.
        """
        return os.path.join(self.workspace_path, self.common_files_directory)

    @property
    def results_fullpath(self) -> str:
        """
        Get the full path to the directory where results are stored.

        Returns:
            str: The full path to the directory containing results.
        """
        return os.path.join(self.workspace_path, self.results_directory)

    @property
    def load_cases_fullpath(self) -> str:
        """
        Get the full path to the directory where load cases are stored.

        Returns:
            str: The full path to the directory containing load cases.
        """
        return os.path.join(self.workspace_path, self.load_cases_parent_directory)


@dataclass
class WorkerConfiguration:
    """
    Configuration class for a worker that is used in the OneCompute framework.

    Attributes:
        command (str): A command string that is used by the worker.
        service_name (str): The name of the service used by the worker.
        pool_id (str): The ID of the pool that the worker should be assigned to.
        use_result_lake_storage (bool): Whether the worker should use result lake storage
            or standard storage.
    """

    # Needed until OneCompute platform is adapted to accept this from the portal
    command: str = ""
    service_name: str = ""
    pool_id: str = ""
    use_result_lake_storage: bool = False
