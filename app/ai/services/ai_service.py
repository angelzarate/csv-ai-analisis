from dataclasses import dataclass
from logging import Logger
from app.ai.repository.ai_repository import OpenAIRepository
from app.core.settings import AppSettings
from app.schemas.requisition import Requistion
from app.schemas.requisition_result import RequistionResult


import pandas as pd
import json
from uuid import uuid4




@dataclass
class AIService:
    logger: Logger
    connector: OpenAIRepository
    settings: AppSettings





    def df_to_jsonl(self, df: pd.DataFrame):
      self.logger.info("dataframe to jsonl")
      if df.empty:
          raise ValueError("dataset is empty")
      file_path = self.settings.storage_dir /  f"{uuid4()}.jsol"
      with open(file_path, "w", encoding="utf-8") as file:
        for row in df.itertuples(index=False):
          item = {
              "custom_id": str(row.id_solicitud),
              "method": "POST",
              "url": "/v1/responses",
              "body": {
                "model": self.settings.openai_model,
                "instructions": self.connector.prompt_provider.system_prompt,
                "input": row,
                "text": {
                    "format": {
                        "type": "json_schema",
                        "name": "analisis",
                        "schema": RequistionResult.model_json_schema()
                    }
                }
              }                
          }
          file.write(
            json.dumps(item) + "\n"
          )
      return file_path            

            



    def process_batch(self, file):
        self.logger.info("Processing File on openAI")
        batch_id = self.connector.process_batch(file)
        batch = self.connector.wait_batch_response(batch_id)
        
        content_result = self.connector.output_file_content(batch.output_file_id) 
        outputh_file = self.settings.storage_dir / f"output_{batch_id}.jsonl"
        
        with open(outputh_file, "wb", encoding="utf-8") as file:
           file.write(content_result.read())                   
    
    
    def analyze_request(self, item: Requistion) -> RequistionResult | None:        
        self.logger.info("Analyze Service ...")
        text = item.model_dump_json()
        response = self.connector.execute_prompt(text, RequistionResult)        
        output = response.output_parsed
        if output:
           output.tokens_usados = response.usage.total_tokens if response.usage else 0 
           output.modelo_usado  = response.model
        
        return output
        
