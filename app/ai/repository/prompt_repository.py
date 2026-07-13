import os
from logging import Logger
from dataclasses import dataclass, field
from pathlib import Path



@dataclass
class PromptRepository:
    
    logger: Logger
    __system_prompt__: str = field(init=False)
    
    def __post_init__(self) -> None:
        self.__system_prompt__ = ""
        prompt_path = Path( os.path.join( Path(__file__).parent.parent, 'system_prompt.md'))
        if prompt_path.exists():
          with open(prompt_path, 'r') as file:
              self.__system_prompt__ = file.read()
              self.logger.info("system prompt loaded")
        else:
            self.logger.error(f"path not found ...{prompt_path}" )            

    @property 
    def system_prompt(self):
        return self.__system_prompt__

