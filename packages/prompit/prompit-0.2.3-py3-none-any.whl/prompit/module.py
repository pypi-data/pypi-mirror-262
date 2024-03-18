import os
from pathspec import PathSpec
from pathspec.patterns import GitWildMatchPattern
from pathlib import Path
import json
from typing import List


# Get the directory of the current module
module_dir = Path(__file__).resolve().parent

# Load the languages.json file
with open(module_dir / "ext_to_AceMode.json", "r") as f:
    languages = json.load(f)


def _get_gitignore_spec() -> PathSpec:
    """
    Reads the .gitignore file and returns a PathSpec object.

    Returns:
        PathSpec: A PathSpec object containing the .gitignore specifications.
    """
    gitignore_lines = []

    if os.path.exists(".gitignore"):
        with open(".gitignore", "r") as f:
            gitignore_lines.extend(f.readlines())

    for root, dirs, files in os.walk("."):
        if ".gitignore" in files:
            with open(os.path.join(root, ".gitignore"), "r") as f:
                gitignore_lines.extend(
                    [
                        f"{Path(root).as_posix()}/{line.strip()}"
                        for line in f.readlines()
                        if line.strip() and not line.startswith("#")
                    ]
                )

    gitignore_lines = list(set(gitignore_lines))

    return PathSpec.from_lines(GitWildMatchPattern, gitignore_lines)


def list_files(
    directory: str = ".",
    include_files: List[str] = None,
    ignore_files: List[str] = None,
) -> List[str]:
    """
    Lists all non-ignored files in the given directory.

    Args:
        directory (str, optional): The directory to list files from. Defaults to '.'.
        include_files (List[str], optional): Additional specs to append. Defaults to None.
        ignore_files (List[str], optional): Specs to ignore. Defaults to None.

    Raises:
        FileNotFoundError: If the given directory does not exist.

    Returns:
        List[str]: A list of filepaths for all non-ignored files in the directory.
    """
    if not os.path.exists(directory):
        raise FileNotFoundError(f"The directory {directory} does not exist.")

    spec = _get_gitignore_spec()

    include_files = "\n".join(include_files) if include_files else ""
    a_spec = PathSpec.from_lines(GitWildMatchPattern, include_files.splitlines())

    ignore_files = "\n".join(ignore_files) if ignore_files else ""
    i_spec = PathSpec.from_lines(
        GitWildMatchPattern, [*ignore_files.splitlines(), "*.gitignore", ".git"]
    )

    selected_files = 0
    filepaths = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if (
                not spec.match_file(file_path)
                and not i_spec.match_file(file_path)
                or a_spec.match_file(file_path)
            ):
                # check if file can be read
                try:
                    with open(file_path, "r", encoding="utf-8"):
                        selected_files += 1
                        filepaths.append(file_path)
                except Exception:
                    pass

    return filepaths


def get_repo_structure(
    directory: str = ".",
    include_files: List[str] = None,
    ignore_files: List[str] = None,
    filepaths: List[str] = None,
) -> str:
    """
    Returns a string representing the directory structure of the repository.

    Args:
        directory (str, optional): The directory to get the structure of. Defaults to '.'.
        include_files (List[str], optional): Additional specs to append. Defaults to None.
        ignore_files (List[str], optional): Specs to ignore. Defaults to None.
        filepaths (List[str], optional): List of filepaths to use. Can be used with `prompit.list_files` output.

    Raises:
        FileNotFoundError: If the given directory does not exist.

    Returns:
        str: A string representing the directory structure of the repository.
    """
    # Check if the directory exists
    if not os.path.exists(directory):
        raise FileNotFoundError(f"The directory {directory} does not exist.")

    promptified_repo = "\n# Project Structure:\n\n"
    if filepaths is None or not filepaths:
        filepaths = list_files(directory, include_files, ignore_files)

    structure = {}
    for filepath in filepaths:
        parts = filepath.replace(directory + os.sep, "").split(os.sep)
        current_level = structure
        for part in parts[:-1]:
            if part not in current_level:
                current_level[part] = {}
            current_level = current_level[part]
        current_level[parts[-1]] = None

    def build_structure(level, indent=""):
        result = []
        for name, sublevel in sorted(level.items()):
            if sublevel is None:
                result.append(f"{indent}|-- {name}")
            else:
                result.append(f"{indent}|-- {name}")
                if sublevel:
                    result.append(build_structure(sublevel, indent + "    "))
        return "\n".join(result)

    promptified_repo += build_structure(structure)

    return promptified_repo


def get_promptified_repo(
    directory: str = ".",
    include_files: List[str] = None,
    ignore_files: List[str] = None,
    show_structure: bool = False,
    xml_comments: bool = True,
) -> str:
    """
    Returns a string representing the repository as a codebase.

    Args:
        directory (str, optional): The directory to get the codebase of. Defaults to '.'.
        include_files (List[str], optional): Additional specs to append. Defaults to None.
        ignore_files (List[str], optional): Specs to ignore. Defaults to None.
        show_structure (bool, optional): Whether to show the directory structure. Defaults to False.
        xml_comments (bool, optional): Whether to wrap each file on xml tags.

    Raises:
        FileNotFoundError: If the given directory does not exist.

    Returns:
        str: A string representing the repository as a codebase.
    """
    # Check if the directory exists
    if not os.path.exists(directory):
        raise FileNotFoundError(f"The directory {directory} does not exist.")

    filepaths = list_files(directory, include_files, ignore_files)

    promptified_repo = "<!-- codebase -->\n"
    for filepath in filepaths:
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                text_content = f.read()
                wrapper = (
                    "```" if "```" not in text_content else "~~~"
                )  # not infalible, thus it might be better to add a <file> tag
                ext = filepath.split(".")[-1]
                language = languages.get(f".{ext}", "")
                content = f"{filepath}\n{wrapper}{language}\n{text_content}\n{wrapper}"

                if xml_comments:
                    content = "<!-- file -->\n" + content + "\n<!-- end of file -->"

                content += "\n\n"

            if content:
                promptified_repo += content
        except Exception:
            pass

    if show_structure:
        promptified_repo += get_repo_structure(directory, include_files, ignore_files)

    promptified_repo = promptified_repo.strip() + "\n\n<!-- end of codebase -->"

    return promptified_repo
