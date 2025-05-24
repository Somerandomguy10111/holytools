from typing import Optional

from .fileio import FileIO

class PlaintextFile(FileIO):
    def read(self) -> str:
        with open(self.fpath, 'r') as f:
            text = f.read()
        return text

    def write(self, content: str):
        with open(self.fpath, 'w', encoding='utf-8') as file:
            file.write(content)

    def view(self):
        content = self.read()
        print(content)

    def check_content_ok(self):
        try:
            with open(self.fpath, 'rb') as file:
                bytes_content = file.read()
                bytes_content.decode('utf-8')
            return True
        except UnicodeDecodeError:
            raise TypeError(f'File {self.fpath} is not a valid utf-8 encoded text file')

    @classmethod
    def get_text(cls, fpath : str) -> str:
        with open(fpath, 'r') as f:
            text = f.read()
        return text

    def read_section(self, name : str, sub : Optional[list[str]] = None, delimiter : str = '##'):
        file_content = self.read()
        lines = file_content.split('\n')
        lines = [l for l in lines if not l == '']
        file_content = '\n'.join(lines)

        segments = file_content.split(delimiter)[1:]

        segement_map : dict[str, str] = {}
        for s in segments:
            segment_name = s.split('\n')[0].strip()
            content_lines = s.split('\n')[1:]
            segment_content = '\n'.join(content_lines)
            segement_map[segment_name] = segment_content

        section_content = segement_map[name].rstrip('\n')
        if sub is None:
            sub = []
        for j, s in enumerate(sub):
            section_content = section_content.replace(f'#{j+1}', s)

        return section_content

