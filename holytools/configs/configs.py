import os.path
import subprocess
from typing import Optional

from holytools.configs.base import BaseConfigs
from holytools.logging import LogLevel

# ---------------------------------------------------------

class FileConfigs(BaseConfigs):
    def __init__(self, fpath : str = '~/.pyconfig'):
        self._config_fpath: str = self._as_abspath(path=fpath)
        config_dirpath = os.path.dirname(self._config_fpath)
        os.makedirs(config_dirpath, exist_ok=True)
        super().__init__()

    def _populate_map(self):
        if not os.path.isfile(self._config_fpath):
            self.log(msg=f'File {self._config_fpath} could not be found, configs are empty', level=LogLevel.WARNING)
            return self._map

        with open(self._config_fpath, 'r') as f:
            content = f.read()
            lines = content.split(f'\n')

        current_section = None
        non_empty_lines = [line for line in lines if line.strip()]
        for num, line in enumerate(non_empty_lines):
            parts = line.split(f' = ')
            if line.startswith('[') and line.endswith(']'):
                current_section = line[1:-1]
                self._map[current_section] = {}
            elif len(parts) == 2:
                self._read_line(parts=parts, current_section=current_section, num=num)
            else:
                raise ValueError(f'Line {num + 1} in config file is invalid: \"{line}\"')

    def _read_line(self, parts : (str, str), current_section : Optional[str], num : int):
        key, value = parts
        if ' ' in key:
            raise ValueError(f'Key must not contain whitespaces, got key \"{key}\" in line {num + 1}')
        if ' ' in value:
            raise ValueError(f'Value must not contain whitespaces, got value \"{value}\" in line {num + 1}')
        self._map[current_section][key] = value

    def _update_resource(self):
        general_section = {k:v for k,v in self._map[None].items()}
        other_sections = {k:v for k,v in self._map.items() if not k is None}

        config_content = ''
        for k,v in general_section.items():
            config_content += f'{k} = {v}\n'

        for section_name, section_map  in other_sections.items():
            config_content += f'\n[{section_name}]\n'
            for subkey, subval in section_map.items():
                config_content += f'{subkey} = {subval}\n'

        print(f'Writing to file: {self._config_fpath}')
        with open(self._config_fpath, 'w') as f:
            f.write(config_content)


class PassConfigs(BaseConfigs):
    def __init__(self):
        if 'PASSWORD_STORE_DIR' in os.environ:
            self._pass_dirpath: str = self._as_abspath(path=os.environ['PASSWORD_STORE_DIR'])
        else:
            self._pass_dirpath = os.path.expanduser(f'~/.password-store')
        super().__init__()

    def _populate_map(self):
        keys = self._get_toplevel_keys()
        for k in keys:
            self._map[None][k] = self._try_run_cmd(f'pass {k}')

    def _update_resource(self):
        existing_keys = os.listdir(path=self._pass_dirpath)
        sectionless_map = self.get_general_section()
        missing_keys = [k for k in sectionless_map if k not in existing_keys]
        for k in missing_keys:
            value = sectionless_map[k]
            insert_command = f"echo \"{value}\" | pass insert --echo {k}"
            self._try_run_cmd(cmd=insert_command)

    def _try_run_cmd(self, cmd : str) -> Optional[str]:
        try:
            result = subprocess.run(cmd, text=True, capture_output=True, check=True, shell=True)
            return result.stdout.strip()
        except Exception as e:
            self.log(f"An error occurred during command execution, you configuration is likely not saved to pass:\n"
                     f'err = \"{e}\"\n', level=LogLevel.WARNING)
            result = None
        return result

    def _get_toplevel_keys(self) -> list[str]:
        filenames = os.listdir(path=self._pass_dirpath)
        keys = [os.path.splitext(f)[0] for f in filenames if f.endswith('.gpg')]
        return keys

