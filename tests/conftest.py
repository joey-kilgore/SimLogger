import pytest
import os
import shutil


@pytest.fixture(scope="session", autouse=True)
def temporary_session_dir(tmpdir_factory):
    # Create a temporary directory for the entire test session
    temp_dir = tmpdir_factory.mktemp("session-tmp")

    # Change the working directory to the temporary directory
    original_dir = os.getcwd()
    os.chdir(temp_dir)

    # Yield control back to pytest
    yield temp_dir

    # Change back to the original working directory after tests are done
    os.chdir(original_dir)

    # Optionally clean up the temporary directory
    shutil.rmtree(temp_dir)
