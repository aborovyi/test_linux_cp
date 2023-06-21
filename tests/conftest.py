"""
All fixtures are stored in this place
"""

import pytest
from test_linux_cp.dir_structure import DirStructure


@pytest.fixture(name="vfs")
def deploy_single_file_copying_structure(tmp_path):
    """
    Create a directory for tests with all the infrastructure
    """
    structure = DirStructure(tmp_path)
    structure.call_cmd(f"cd {tmp_path}")
    yield structure
    structure.clean()
