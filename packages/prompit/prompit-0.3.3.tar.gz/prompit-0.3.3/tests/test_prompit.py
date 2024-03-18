import os
import pytest
import src.prompit as prompit


def test_list_files():
    # Test with current directory
    files = prompit.list_files(".")
    assert isinstance(files, list)
    assert len(files) > 0

    # Test with non-existent directory
    with pytest.raises(FileNotFoundError):
        prompit.list_files("non_existent_directory")

    # Test with directory that doesn't contain files
    os.mkdir("empty_directory")
    files = prompit.list_files("empty_directory")
    os.rmdir("empty_directory")
    assert len(files) == 0


def test_get_repo_structure():
    # Test with current directory
    structure = prompit.get_repo_structure(".")
    assert isinstance(structure, str)
    assert len(structure) > 0

    # Test with non-existent directory
    with pytest.raises(FileNotFoundError):
        prompit.get_repo_structure("non_existent_directory")

    # Test with directory that doesn't contain files
    os.mkdir("empty_directory")
    structure = prompit.get_repo_structure("empty_directory")
    os.rmdir("empty_directory")
    assert structure == "\n# Project Structure:\n\n"  # updated this line


def test_get_promptified_repo():
    # Test with current directory
    repo = prompit.get_promptified_repo(".")
    assert isinstance(repo, str)
    assert len(repo) > 0

    # Test with non-existent directory
    with pytest.raises(FileNotFoundError):
        prompit.get_promptified_repo("non_existent_directory")

    # Test with directory that doesn't contain files
    os.mkdir("empty_directory")
    repo = prompit.get_promptified_repo("empty_directory")
    os.rmdir("empty_directory")
    assert repo == "<!-- codebase -->\n\n<!-- end of codebase -->"  # updated this line
