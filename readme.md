## Holytools
A collection of general utilities in various very general areas that aim for simplicity in use. 
Functiontionalities include:

- object serialization -> holytools.abstract.serialization
- fileIO and mock files -> holytools.file
- configuration management -> holytools.configs
- file system navigation and management -> holytools.fsys
- task/event scheduling -> holytools.events
- hardware interaction ->  holytools.hardware
- web search/scraping -> holytools.web
- command line interfaces -> holytools.userIO


#### Setup
Latest release from PyPI:
```
pip install holytools 
```

OR: Most recent commit from github:
```
git clone https://github.com/Somerandomguy10111/holytools && pip install ./holytools
```


#### Examples
```
# fsys
from holytools.fsys import FsysNode
node = FsysNode(path='/home/daniel/Drive/Desktop/fluent_python.pdf')
zip_bytes = node.get_zip()
last_modified : float = node.get_epochtime_last_modified()
file_size_mb : float = node.get_size_in_MB()
```
```
# config
from holytools.configs import FileConfigs
configs = FileConfigs(config_fpath='~/myconfigs.ini')
key = 'plot_images'
configs.set(key=key, value=False)
plot_images : bool = configs.get(key=key) # False
```
```
# serialization
from holytools.abstract import Picklable
class SomeClass(Picklable):
    def __init__(self, s : str, x : float):
        import uuid
        self.s = s
        self.x = x
        self.uuid = uuid.uuid4()

obj = SomeClass(s='hello there', x =2.3)
serialized_obj = obj.to_str()
loaded_obj = SomeClass.from_str(s=serialized_obj)
print(obj.__dict__)          # {'s': 'hello there', 'x': 2.3, 'uuid': UUID('79b489be-3871-4da0-ade4-665097b9bf42')}
print(loaded_obj.__dict__)   # {'s': 'hello there', 'x': 2.3, 'uuid': UUID('79b489be-3871-4da0-ade4-665097b9bf42')}
```