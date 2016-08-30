import os

from pyfakefs import fake_filesystem_unittest

from shellfoundry.utilities.shell_package_builder import ShellPackageBuilder
from tests.asserts import assertFileExists
from tests.test_utilities.test_package_builder import TestPackageBuilder


class TestShellPackageBuilder(fake_filesystem_unittest.TestCase):
    def setUp(self):
        self.setUpPyfakefs()

    def test_tosca_based_shell_packed(self):
        # Arrange
        self.fs.CreateFile('nut-shell/TOSCA-Metadata/TOSCA.meta',
                           contents='TOSCA-Meta-File-Version: 1.0 \n'
                                    'CSAR-Version: 1.1 \n'
                                    'Created-By: Anonymous\n'
                                    'Entry-Definitions: shell-definition.yml')

        self.fs.CreateFile('nut-shell/shell-definition.yml',
                           contents='tosca_definitions_version: tosca_simple_yaml_1_0\n'
                                    'metadata:\n'
                                    '  template_name: NutShell\n'
                                    '  template_author: Anonymous\n'
                                    '  template_version: 1.0.0\n'
                                    'node_types:\n'
                                    '  vendor.switch.NXOS:\n'
                                    '    derived_from: cloudshell.nodes.Switch\n'
                                    '    artifacts:\n'
                                    '      icon:\n'
                                    '        file: nxos.png\n'
                                    '        type: tosca.artifacts.File\n'
                                    '      driver:\n'
                                    '        file: NutShellDriver.zip\n'
                                    '        type: tosca.artifacts.File')

        self.fs.CreateFile('nut-shell/nxos.png',
                           contents='IMAGE')

        os.chdir('nut-shell')

        shell_package_builder = ShellPackageBuilder()

        # Act
        shell_package_builder.pack('nut-shell')

        # Assert
        assertFileExists(self, 'dist/nut-shell.zip')
        TestPackageBuilder.unzip('dist/nut-shell.zip', 'dist/package_content')

        assertFileExists(self, 'dist/package_content/TOSCA-Metadata/TOSCA.meta')
        assertFileExists(self, 'dist/package_content/shell-definition.yml')
        assertFileExists(self, 'dist/package_content/nxos.png')
        assertFileExists(self, 'dist/package_content/NutShellDriver.zip')

    def test_tosca_based_shell_packed_when_artifacts_missing_in_yaml_file(self):
        # Arrange
        self.fs.CreateFile('nut-shell/TOSCA-Metadata/TOSCA.meta',
                           contents='TOSCA-Meta-File-Version: 1.0 \n'
                                    'CSAR-Version: 1.1 \n'
                                    'Created-By: Anonymous\n'
                                    'Entry-Definitions: shell-definition.yml')

        self.fs.CreateFile('nut-shell/shell-definition.yml',
                           contents='tosca_definitions_version: tosca_simple_yaml_1_0\n'
                                    'metadata:\n'
                                    '  template_name: NutShell\n'
                                    '  template_author: Anonymous\n'
                                    '  template_version: 1.0.0\n'
                                    'node_types:\n'
                                    '  vendor.switch.NXOS:\n'
                                    '    derived_from: cloudshell.nodes.Switch')

        os.chdir('nut-shell')

        shell_package_builder = ShellPackageBuilder()

        # Act
        shell_package_builder.pack('nut-shell')

        # Assert
        assertFileExists(self, 'dist/nut-shell.zip')
        TestPackageBuilder.unzip('dist/nut-shell.zip', 'dist/package_content')

        assertFileExists(self, 'dist/package_content/TOSCA-Metadata/TOSCA.meta')
        assertFileExists(self, 'dist/package_content/shell-definition.yml')

    def test_tosca_based_shell_packed_when_some_artifacts_missing_in_directory(self):
        # Arrange
        self.fs.CreateFile('nut-shell/TOSCA-Metadata/TOSCA.meta',
                           contents='TOSCA-Meta-File-Version: 1.0 \n'
                                    'CSAR-Version: 1.1 \n'
                                    'Created-By: Anonymous\n'
                                    'Entry-Definitions: shell-definition.yml')

        self.fs.CreateFile('nut-shell/shell-definition.yml',
                           contents='tosca_definitions_version: tosca_simple_yaml_1_0\n'
                                    'metadata:\n'
                                    '  template_name: NutShell\n'
                                    '  template_author: Anonymous\n'
                                    '  template_version: 1.0.0\n'
                                    'node_types:\n'
                                    '  vendor.switch.NXOS:\n'
                                    '    derived_from: cloudshell.nodes.Switch\n'
                                    '    artifacts:\n'
                                    '      icon:\n'
                                    '        file: nxos.png\n'
                                    '        type: tosca.artifacts.File\n')

        os.chdir('nut-shell')

        shell_package_builder = ShellPackageBuilder()

        # Act
        shell_package_builder.pack('//nut-shell')

        # Assert
        assertFileExists(self, 'dist/nut-shell.zip')
        TestPackageBuilder.unzip('dist/nut-shell.zip', 'dist/package_content')

        assertFileExists(self, 'dist/package_content/TOSCA-Metadata/TOSCA.meta')
        assertFileExists(self, 'dist/package_content/shell-definition.yml')
