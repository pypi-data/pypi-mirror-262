"""Mock SCM definitions"""

from cppython_core.plugin_schema.scm import (
    SCM,
    SCMPluginGroupData,
    SupportedSCMFeatures,
)
from cppython_core.schema import Information
from pydantic import DirectoryPath


class MockSCM(SCM):
    """A mock generator class for behavior testing"""

    def __init__(self, group_data: SCMPluginGroupData) -> None:
        self.group_data = group_data

    @staticmethod
    def features(directory: DirectoryPath) -> SupportedSCMFeatures:
        """Broadcasts the shared features of the SCM plugin to CPPython

        Args:
            directory: The root directory where features are evaluated

        Returns:
            The supported features
        """

        return SupportedSCMFeatures(repository=True)

    @staticmethod
    def information() -> Information:
        """Returns plugin information

        Returns:
            The plugin information
        """
        return Information()

    def version(self, directory: DirectoryPath) -> str:
        """Extracts the system's version metadata

        Args:
            directory: The repository path

        Returns:
            A version
        """
        return "1.0.0"
