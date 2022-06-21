from dataclasses import dataclass


@dataclass
class Model:
    name: str
    version: int
    format: str
    data_url: str
