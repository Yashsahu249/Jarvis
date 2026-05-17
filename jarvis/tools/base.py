from abc import ABC, abstractmethod


class BaseTool(ABC):
    @abstractmethod
    def name(self) -> str:
        ...

    @abstractmethod
    def description(self) -> str:
        ...

    @abstractmethod
    async def execute(self, **kwargs) -> str:
        ...

    def to_dict(self) -> dict:
        return {
            "name": self.name(),
            "description": self.description(),
        }
