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
        self.model_name = settings.ollama_cloud_model_classification
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
        
        # 💡 優化提示詞：讓 Ollama 根據 JSON Schema 自動填入，通常不需要在 Prompt 強調 True/False 字串
        prompt = f"""
               You are an expert data extraction assistant. Analyze the text provided below and extract specific information based on the fields required.
       
               Text to analyze:\n{combined_content}\n
               """
        
        # resp 本身就已經是 ExtractedData 物件
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
        
        # 💡 修正：移除冗餘的 ExtractedData.model_validate(resp)
        self.logger.info(f"id: {item.get('id')}, \ntitle: {item.get('title')}")
        self.logger.info(f"Extracted item: \n%s", pformat(resp.model_dump(by_alias=True), indent=2))
        
        return resp
        
        
    async def extract_data_from_all_news(self, state: State):
        
        self.logger.info(f"Start extracting data from press releases.")
        
        semaphore = asyncio.Semaphore(4) # Tune this (3~6) based on your GPU/RAM
        
        async def bounded_extract(item: dict):
            async with semaphore:
                try:
                    return await self._extract_data(item = item)
                except Exception as e:
                    # 💡 紀錄單一任務失敗的 Log，避免無聲無息地不見
                    self.logger.error(f"Failed to extract item {item.get('id')}: {e}")
                    return e

        tasks = [bounded_extract(item=result) for result in state.search_results]
        raw_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 💡 修正：過濾掉 Exception 物件，確保 main.py 拿到的都是 ExtractedData 
        extracted_datas = [res for res in raw_results if isinstance(res, ExtractedData)]
        
        # 可選：如果你想知道失敗了幾個
        failed_count = len(raw_results) - len(extracted_datas)
        if failed_count > 0:
            self.logger.warning(f"Successfully processed {len(extracted_datas)} items, but {failed_count} items failed.")
        else:
            self.logger.info(f"Extraction completed. {len(state.search_results)} press releases processed.")
        
        return extracted_datas
