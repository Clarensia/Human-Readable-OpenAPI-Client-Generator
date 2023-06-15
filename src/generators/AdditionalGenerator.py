import os

class AdditionalGenerator:
    """Append the code inside of the additional folder to the destination folder
    
    It simply goes through all files and folders inside of inputs/additional and create files
    and folders when required, if file and folder already exists, it append the content to the
    file
    """
    
    _additional_folder: str
    _api_folder: str
    
    def __init__(self, additional_folder: str, api_folder: str):
        self._additional_folder = additional_folder
        self._api_folder = api_folder

    def _append_additional_rec(self, curr_path: str, curr_dest_path: str, file_folder: str):
        curr_path = os.path.join(curr_path, file_folder)
        curr_dest_path = os.path.join(curr_dest_path, file_folder)
        if os.path.isdir(curr_path):
            if not os.path.isdir(curr_dest_path):
                os.mkdir(curr_dest_path)
            elif os.path.isfile(curr_dest_path):
                raise Exception(f"Destination path: {curr_dest_path} is a file it should be a folder or not exist")

            for file_in_folder in os.listdir(curr_path):
                self._append_additional_rec(curr_path, curr_dest_path, file_in_folder)

        else:
            with open(curr_path, "r") as read_file:
                content = read_file.read()
            with open(curr_dest_path, "a+") as write_file:
                write_file.write(content)

    def append_additional(self):
        if not os.path.isdir(self._additional_folder):
            print(f"[Warning] The given path: {self._additional_folder} is not a folder")
        else:
            self._append_additional_rec(self._additional_folder, self._api_folder, "")
