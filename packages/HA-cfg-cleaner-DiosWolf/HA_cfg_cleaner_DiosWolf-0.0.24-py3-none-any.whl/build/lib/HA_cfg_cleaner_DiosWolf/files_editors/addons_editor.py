import os
from subprocess import run, CompletedProcess, PIPE
from HA_cfg_cleaner_DiosWolf.data_classes_json.file_config import SshCommands
from HA_cfg_cleaner_DiosWolf.files_editors.fileIO_cls import FileIO


class AddonsEditor:
    def __init__(self, configuration: SshCommands):
        self.configuration = configuration
        self.file_io = FileIO()

    def __send_ssh_command(self, command: list[str]) -> CompletedProcess[str]:
        return run(command, stdout=PIPE, text=True)

    def __get_command(self, command: list[str], addon_id: str) -> list[str]:
        return command + [addon_id]

    def write_new_cfg(self, cfg_path: str, cfg_name: str, new_cfg: dict):
        os.mkdir(cfg_path)
        self.file_io.yaml_write(cfg_path + cfg_name, new_cfg)

    def use_ssh_addon(self, addon_id: str, command: list[str]):
        command = self.__get_command(command, addon_id)
        if (result := self.__send_ssh_command(command)).returncode:
            raise Exception(result.stdout)
