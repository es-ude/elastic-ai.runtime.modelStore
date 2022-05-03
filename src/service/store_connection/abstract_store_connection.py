from abc import ABC, abstractmethod

from service.entities import Model


class ModelNotFound(Exception):
   pass


class AbstractStoreConnection(ABC):
   @abstractmethod
   def getModel(self, modelName: str, version: int = None) -> Model:
      raise NotImplementedError

   @abstractmethod
   def getNewestVersion(self, modelName: str) -> int:
      raise NotImplementedError
