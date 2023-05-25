import os

def create_requirements(dest_folder: str):
    """This creates the requirements.txt file inside of the destination folder

    :param dest_folder: The destination folder
    :type dest_folder: str
    """
    with open(os.path.join(dest_folder, "requirements.txt"), "w+") as f:
        f.write("aiohttp\n")
    
