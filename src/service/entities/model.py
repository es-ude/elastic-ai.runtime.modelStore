from dataclasses import dataclass


@dataclass
class Model:
   name: str
   version: int
   formats: dict
   files: dict
