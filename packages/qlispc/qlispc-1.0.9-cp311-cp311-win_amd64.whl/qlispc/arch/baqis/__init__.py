from ..general import Architecture
from .assembly_code import assembly_code as code
from .assembly_data import assembly_data as data
from .config import QuarkConfig as Config
from .config import QuarkLocalConfig as Snapshot

baqisArchitecture = Architecture('baqis', "", code, data, Config, Snapshot)
