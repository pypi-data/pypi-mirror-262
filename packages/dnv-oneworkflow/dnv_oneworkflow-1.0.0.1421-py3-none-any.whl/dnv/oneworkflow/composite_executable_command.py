"""
This module defines the `CompositeExecutableCommand` class, which represents a composite of multiple
executable worker commands, allowing them to be executed sequentially or concurrently within a
specified working directory. It also provides properties to access and modify the execution mode and
the list of executable commands.
"""

from .worker_command import WorkerCommand


class CompositeExecutableCommand(WorkerCommand):
    """
    A command that represents a composite of multiple executable worker commands.

    This command allows a list of worker commands to be executed either sequentially
    or concurrently within a specific working directory.

    Attributes:
        RunSequentially (bool): A flag indicating whether the commands should be executed
            sequentially (True) or concurrently (False).
        ContinueOnError (bool): When set to True, allows the commands within the CompositeExecutable
            command to continue running even if one of the commands fails. The composite executable
            command's execution status will be marked as 'Faulted' if any of the commands fail.
        ExecutableCommands (list[WorkerCommand]): The list of worker commands to be executed.
    """

    def __init__(self, commands: list[WorkerCommand], working_dir: str = ""):
        """
        Initialize a CompositeExecutableCommand.

        Args:
            commands (list[WorkerCommand]): A list of worker commands to be executed.
            working_dir (str, optional): The working directory in which to execute the commands.
                Defaults to an empty string.
        """
        super().__init__(working_dir)
        self.RunSequentially = True
        self.ExecutableCommands = commands
        self.ContinueOnError = False
        for cmd in commands:
            if not cmd.working_directory.strip():
                cmd.working_directory = working_dir

    @property
    def type(self) -> str:
        """
        Gets the type of the command.

        Returns:
            str: A string representing the type of the command.
        """
        return "DNV.One.Workflow.CommandModel.ExecutableCommands.CompositeExecutableCommand, DNV.One.Workflow.CommandModel"

    @property
    def run_sequentially(self) -> bool:
        """
        Get the execution mode for the commands.

        Returns:
            bool: True if the commands should be executed sequentially, False if concurrently.
        """
        return self.RunSequentially

    @run_sequentially.setter
    def run_sequentially(self, value: bool):
        """
        Set the execution mode for the commands.

        Args:
            value (bool): True to execute the commands sequentially, False to execute concurrently.
        """
        self.RunSequentially = value

    @property
    def executable_commands(self) -> list[WorkerCommand]:
        """
        Get the list of executable worker commands.

        Returns:
            list[WorkerCommand]: The list of worker commands to be executed.
        """
        return self.ExecutableCommands

    @executable_commands.setter
    def executable_commands(self, value: list[WorkerCommand]):
        """
        Set the list of executable worker commands.

        Args:
            value (list[WorkerCommand]): The list of worker commands to be executed.
        """
        self.ExecutableCommands = value

    @property
    def continue_onerror(self) -> bool:
        """
        Get the current status of the ContinueOnError attribute.

        Returns:
            bool: The current status of the ContinueOnError attribute.
        """
        return self.ContinueOnError

    @continue_onerror.setter
    def continue_onerror(self, value: bool):
        """
        Set the ContinueOnError attribute to the provided value.

        Args:
            value (bool): The value to set for the ContinueOnError attribute.
        """
        self.ContinueOnError = value
