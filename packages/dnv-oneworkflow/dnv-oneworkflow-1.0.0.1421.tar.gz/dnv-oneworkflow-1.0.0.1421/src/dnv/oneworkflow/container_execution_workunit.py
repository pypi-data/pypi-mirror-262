"""
This module defines the `ContainerExecutionWorkUnit`. This is a WorkUnit which is runs
a containerised task, either in Azure Batch or in the OneCompute Kubernetes backend.

There are also two data classes, `KubernetesPropertyNames` and `ContainerSettingsNames`, for 
managing property names and settings related to Kubernetes and containers, respectively. These 
classes are marked as frozen for immutability.
"""

from dataclasses import dataclass

from dnv.onecompute.flowmodel import WorkUnit


@dataclass(frozen=True)
class KubernetesPropertyNames:
    """
    A class that defines constants for Kubernetes property names.

    Attributes:
        CPU_REQUEST (str): The name of the CPU request property.
        CPU_LIMIT (str): The name of the CPU limit property.
        MEMORY_REQUEST (str): The name of the memory request property.
        TOLERATION_KEY (str): The name of the toleration key property.
        TOLERATION_VALUE (str): The name of the toleration value property.
    """

    CPU_REQUEST = "CpuRequest"
    CPU_LIMIT = "CpuLimit"
    MEMORY_REQUEST = "MemoryRequest"
    MEMORY_LIMIT = "MemoryLimit"
    TOLERATIONS = "Tolerations"

@dataclass(frozen=True)
class ContainerSettingsNames:
    """
    Defines names of custom properties used to indicate a WorkItem should be run as containerized
    application.

    Attributes:
        IMAGE_NAME (str): Name of property used to indicate the image that will be used to execute
            a WorkUnit.
        RUN_OPTIONS (str):  Name of property used to indicate the run options for launching a
            container to execute a WorkUnit.
    """

    IMAGE_NAME = "ImageName"
    RUN_OPTIONS = "RunOptions"


class ContainerExecutionWorkUnit(WorkUnit):
    """
    A class that represents a work unit that executes in a container.

    Keyword arguments:
    json_string (str): The JSON input for the work unit.
    image_registry (str): The registry containing the image (e.g. onecompute.azurecr.io).
    image_repository (str): The name of the image.
    image_tag (str): The image tag.
    cpu_request (str): The requested CPU resources.
    cpu_limit (str): The maximum CPU resources.
    memory_request (str): The requested memory resources.
    memory_limit (str): The maximum memory resources.
    tolerations (str): A semi-colon delimited list of tolerations.

    Note: The CPU and memory requests and limits, and the tolerations are only relevant
    when the container runs in the OneCompute Kubernetes backend. They will be ignored
    if running in Azure Batch.
    """
    def __init__(
            self,
            json_string: str,
            image_registry: str,
            image_repository: str,
            image_tag: str,
            work_unit_id: str = "",
            cpu_request: str = "",
            cpu_limit: str = "",
            memory_request: str = "",
            memory_limit: str = "",
            tolerations: str = ""):
        """
        Initializes a new instance of the ContainerExecutionCommand class.

        Args:
            json_string (str): A JSON string representing the container execution command.
            command_id (str): An ID for the command.
        """
        super().__init__(data=json_string, work_unit_id=work_unit_id)
        image_name = f'{image_registry}/{image_repository}:{image_tag}'
        self.properties[ContainerSettingsNames.IMAGE_NAME] = image_name
        self.properties[KubernetesPropertyNames.CPU_REQUEST] = cpu_request
        self.properties[KubernetesPropertyNames.CPU_LIMIT] = cpu_limit
        self.properties[KubernetesPropertyNames.MEMORY_REQUEST] = memory_request
        self.properties[KubernetesPropertyNames.MEMORY_LIMIT] = memory_limit
        self.properties[KubernetesPropertyNames.TOLERATIONS] = tolerations
