import os

def create_gitignore(dest_folder: str):
    """Create the .gitignore file containing secret_* inside

    :param dest_folder: The destination folder
    :type dest_folder: str
    """
    with open(os.path.join(dest_folder, ".gitignore"), "w+") as f:
        f.write('''
secret_*
.env
__pycache__
venv
.venv
''')
