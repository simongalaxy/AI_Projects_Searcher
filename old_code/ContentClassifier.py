import asyncio
import instructor
from pprint import pformat
from typing import List

from src.logger import Logger
from src.Settings import settings
from src.States import State, ExtractedData


class ContentClassifier:
    def __init__(self, logger):
        self.logger = logger
        
        # ollama localhost settings.
        self.model_name = settings.ollama_extraction_model
        if not self.model_name:
            raise ValueError("OLLAMA_EXTRACTION_MODEL not set in .env file")
        
        self.async_client = instructor.from_provider(
            model=f"ollama/{self.model_name}",
            base_url="http://localhost:11434/v1",
            mode=instructor.Mode.JSON,
            async_client=True
        )
        self.logger.info(f"Ollama Summarizer initialized with model: {self.model_name}")
        
        # ollama cloud settings.
        
        
    async def _extract_data(self, item: dict) -> ExtractedData:
        
        combined_content = f"id: {item.get('id')}\nTitle:\n{item.get('title')}\nContent:\n{item.get('content')}"
        
        prompt = f"""
        You are an expert data extraction assistant. Analyze the text provided below and extract specific information based on these rules:

        1. **AI Relation**: Determine if the content relates to Artificial Intelligence (including machine learning, LLMs, neural networks, automation tools, or data science). Answer strictly with "True" or "False".

        Text to analyze:\n{combined_content}\n
        
        """
        
        resp = await self.async_client.create(
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
        
        self.logger.info(f"Combined content: \n%s", pformat(combined_content, indent=2))
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

        valid_results = []
        for result in extracted_datas:
            if isinstance(result, Exception):
                self.logger.warning(f"Skipping extraction failure: {result}")
                continue
            if isinstance(result, ExtractedData):
                valid_results.append(result)

        self.logger.info(
            f"Extraction completed. {len(valid_results)} valid classifications returned out of {len(state.search_results)} press releases."
        )
        
        return valid_results
            