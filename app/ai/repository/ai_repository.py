import time
from logging import Logger
from dataclasses import dataclass, field
from openai import Omit, OpenAI
from openai.types import Batch
from app.core.settings import AppSettings
from logging import Logger
from app.ai.repository.prompt_repository import PromptRepository
from typing import TypeVar

TextFormatT = TypeVar(
    "TextFormatT",
    default=None,
)


@dataclass
class OpenAIRepository:
    prompt_provider: PromptRepository
    settings: AppSettings
    logger: Logger
    client: OpenAI = field(init=False)
    
    def __post_init__(self):      
        self.client = OpenAI(
            api_key=self.settings.openai_api_key, 
            base_url=self.settings.ai_endpoint, 
            max_retries=3,
            
        )                
        self.logger.info("openAI client initialized")        

    def output_file_content(self, output_file_id):
        return self.client.files.content(output_file_id)

    def process_batch(self, file: str) -> str:
        batch_file =  self.client.files.create(
            file = open(file, "rb"),
            purpose="batch"
        )
        batch = self.client.batches.create(
            input_file_id=batch_file.id,
            endpoint="/v1/responses",
            completion_window="24h"
        )        
        return batch.id 

    def wait_batch_response(self, batch_id: str) -> Batch:
        while True:
            batch = self.client.batches.retrieve(batch_id)
            self.logger.info(f"Batch processing ({batch.status})...")
            if batch.status == "completed":
                break
            if batch.status in (
                "failed",
                "expired",
                "cancelled",
            ):
                raise RuntimeError( f"Batch {batch.status}" )
            time.sleep(3.0)
        return batch


        

    def execute_prompt(self, prompt: str, text_format: type[TextFormatT] | Omit):    
        response = self.client.responses.parse(
            model=self.settings.openai_model,
            instructions=self.prompt_provider.system_prompt, 
            input=prompt, 
            text_format=text_format
        )
        return  response

    