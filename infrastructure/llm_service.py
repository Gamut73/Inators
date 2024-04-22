from abc import ABC, abstractmethod

from abc import ABC, abstractmethod
from example import Example

class LLMService(ABC):

    def __init__(self) -> None:
        super().__init__()
    
    @abstractmethod
    def make_prompt(self, action: str, examples: list[Example]) -> str:
        pass
