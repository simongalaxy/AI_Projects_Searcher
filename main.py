import asyncio
from pprint import pformat

from src.logger import Logger
from src.States import State
# from src.NewsScraper import NewsScraper
# from src.QueryParser import QueryParser
from src.PG_DBHandler import PG_DBHandler
# from old_code.NewsClassifier import NewsClassifier
from src.ContentClassifier import ContentClassifier



# main entry point.
def main():
    
    # initialize logger and crawler
    logger = Logger(__name__).get_logger()
    state = State()
    # parser = QueryParser(logger=logger)
    # scraper = NewsScraper(logger=logger)
    dbhandler = PG_DBHandler(logger=logger)
    classifier = ContentClassifier(logger=logger)

    
    # stage 1: scrape news.
    # while True:
    #     state.original_query = input("Enter the query to the Gov News or type 'q' for exit:")
    #     logger.info(f"User Query stored in state: {state.original_query}")
    #     if state.original_query.lower() == "q":
    #         break
        
    #     # parse the user query.
    #     parser.parse_query(state=state)
        
    #     # crawl all relevant news based on parsed_query.
    #     if state.parsed_query.start_date is not None:
    #         scraper.fetch_news_by_dates(state=state)
        
    #     # show summary of scraped news items by date.
    #     for date, news_urls in zip(state.dates, state.news_urls):
    #         logger.info(f"Date Page - {date}: {len(news_urls)} news.")
    #     logger.info("\n")
        
    #     # extract information from the news.
    #     # asyncio.run(extractor.extract_data_from_all_news(state=state))
        
    #     # # save news to database.
    #     # logger.info(f"Start saving total {len(state.news_items)} to database.")
    #     for item in state.news_items:
    #         dbhandler.insert_news(item=item)
    
    # stage 2: news classification.
    while True:
        start_date=input("Enter start date in format like 2026-08-01: ")
        end_date=input("Enter end date: ")
        
        dates = dbhandler.retrieve_distinct_dates(start_date=start_date, end_date=end_date)
        logger.info(f"Dates: {dates}")
        
        for date in dates:
            dbhandler.retrieve_news_for_extracting_data(state=state, start_date=date['published_date'])
            extracted_datas = asyncio.run(classifier.extract_data_from_all_news(state=state))
            
            for item in extracted_datas:
                dbhandler.update_news_classification(item=item)
    
    # stage 3: extract AI project details.
    
    
        
    return

if __name__ == "__main__":
    main()
