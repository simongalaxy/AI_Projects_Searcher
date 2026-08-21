import os
import json
import asyncio
import instructor
from openai import AsyncOpenAI
from pprint import pformat
from typing import List


from src.logger import Logger
from src.Settings import settings
from src.States import State, ExtractedData


class NewsClassifier:
    def __init__(self, logger: Logger):
        # logger setting.
        self.logger = logger
        
        # Explicitly declare the remote host address
        self.model_name = settings.ollama_cloud_model
        self.base_url = settings.ollama_base_url
        self.api_key = settings.ollama_api_key
        self.client = instructor.from_openai(
            AsyncOpenAI(
                base_url=self.base_url,
                api_key=self.api_key
            ),
            mode=instructor.Mode.JSON_SCHEMA,  # Forces JSON extraction compatible with Ollama
        )


    async def _extract_data(self, item: dict) -> ExtractedData:
        
        combined_content = f"id: {item.get('id')}\nTitle:\n{item.get('title')}\nContent:\n{item.get('content')}"
        self.logger.info(f"Combined content: \n{combined_content}")
        
        prompt = f"""
        Extract the information from the content and strictly follow the rule below:
        
        content: \n{combined_content}\n
        
        """
        
        resp = await self.client.create(
            model=self.model_name,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            response_model=ExtractedData,
        )
        
        extracted_data = ExtractedData.model_validate(resp)
        self.logger.info(f"id: {item.get('id')}, \ntitle: {item.get('title')}")
        self.logger.info(f"Extracted item: \n%s", pformat(extracted_data.model_dump(by_alias=True), indent=2))
        
        return extracted_data
        
        
    async def extract_data_from_all_news(self, state: State):
        
        self.logger.info(f"Start extracting data from press releases.")
        
        semaphore = asyncio.Semaphore(4) # Tune this (3~6) based on your GPU/RAM
        
        async def bounded_extract(item: dict):
            async with semaphore:
                return await self._extract_data(item = item)

        tasks = [bounded_extract(item=result) for result in state.search_results]
        extracted_datas = await asyncio.gather(*tasks, return_exceptions=True)
        
        self.logger.info(f"Extraction completed. {len(state.search_results)} press releases processed.")
        
        return extracted_datas
        