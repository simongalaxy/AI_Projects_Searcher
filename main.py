import asyncio
from pprint import pformat

from src.Util.logger import Logger
from src.Core.State import State
from src.Core.Graph import load_workflow


# main entry point.
def main():
    
    # initialize logger and crawler
    logger = Logger(__name__).get_logger()
    
    
    load_workflow()
    
    # # Scrape news and save them into Neon DB.
    # while True:
    #     state.original_query = input("Enter the query to the Gov News or type 'q' for exit:")
    #     logger.info(f"User Query stored in state: {state.original_query}")
    #     if state.original_query.lower() == "q":
    #         break
        
    #     # parse the user query.
    #     parser.parse_query(state=state)
        
    #     if state.parsed_query.action == "scrape":
        
    #         # crawl all relevant news based on parsed_query.
    #         if state.parsed_query.start_date is not None:
    #             scraper = NewsScraper(logger=logger)
    #             scraper.fetch_news_by_dates(state=state)
            
    #         # show summary of scraped news items by date.
    #         for date, news_urls in zip(state.dates, state.news_urls):
    #             logger.info(f"Date Page - {date}: {len(news_urls)} news.")
    #         logger.info("\n")
            
    #         # save news to database.
    #         for item in state.news_items:
    #             dbhandler.insert_news(item=item)
        
    #     elif state.parsed_query.action == "retrieve":
    #         # check keyword
    #         if state.parsed_query.departments is None:
    #             departments = input("Enter the departments/bureux (with ', ' as seperator) to search: ")
    #             if departments is not None:
    #                 state.parsed_query.departments = [item.strip() for item in departments.split(", ")]
    #             else:
    #                 state.parsed_query.departments = None
            
    #         if state.parsed_query.keywords is None:
    #             keywords = input("Enter the keywords (with ', ' as seperator) to search: ")
    #             if keywords is not None:
    #                 state.parsed_query.keywords = [item.strip() for item in keywords.split(", ")]
    #             else:
    #                 state.parsed_query.keywords = None
            
    #         # make query to Neon DB.
    #         dbhandler.query_full_text_search(state=state)
    #         classifier = NewsClassifier(logger=logger)
    #         # extracted_datas = await classifier.extract_data_from_all_news(state=state)
            
    #         # update classification results accordingly in neon db.
    #         for item in extracted_datas:
    #             dbhandler.update_news_classification(item=item)
        
    return

if __name__ == "__main__":
    # asyncio.run(main())
    main()