import pathlib

def get_file_paths(path: str, file_type: str='.csv') -> list:
    """
    Returns a list of all .file_type files in the specified folder path.
    """
    folder_path = pathlib.Path(path)
    file_paths = [str(file_path) for file_path in folder_path.glob(f'*{file_type}')]
    return file_paths