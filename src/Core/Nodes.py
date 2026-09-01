# # Add Nodes
#     workflow.add_node("parse_query", parse_query_node)
#     workflow.add_node("check_database", check_database_node)
#     workflow.add_node("fetch_and_save", fetch_and_save_node)
#     workflow.add_node("retrieve_prs", retrieve_prs_node)
#     workflow.add_node("generate_summary", generate_summary_node)

#     # Set Entry Point
#     workflow.set_entry_point("parse_query")

#     # Standard Linear Edges
#     workflow.add_edge("parse_query", "check_database")
#     workflow.add_edge("fetch_and_save", "retrieve_prs")
#     workflow.add_edge("retrieve_prs", "generate_summary")
#     workflow.add_edge("generate_summary", END)

# initiate classes.
from src.Util.logger import Logger
from src.Core.State import State
from src.LLM.QueryParser import QueryParser
from src.Database.PG_DBHandler import PG_DBHandler
from src.WebScraper.NewsScraper import NewsScraper




# define nodes.
def parse_query_node(state: State, logger: Logger):
    parser = QueryParser(logger=logger)
    state.original_query = input("Enter the query to the Gov News or type 'q' for exit:")
    logger.info(f"User Query stored in state: {state.original_query}")
    
    # parse the user query.
    parser.parse_query(state=state)
    
    return


def fetch_and_save_node(state: State, dbhandler: PG_DBHandler, logger: Logger):
    # fetch news items based on the parsed query and save them to the database.
    logger.info("Fetching news items based on the parsed query and saving them to the database.")
    
    # Implement your fetching and saving logic here.
    scraper = NewsScraper(logger=logger)
    scraper.fetch_news_by_dates(state=state)
    
    # save scraped news into database.
    for news_item in scraper.news_items:
        dbhandler.insert_news(item=news_item)

    return

# def check_database_node(state: State, dbhandler: PG_DBHandler, logger: Logger):
#     # check if the parsed query exists in the database.
#     logger.info("Checking if the parsed query exists in the database.")
    
#     # Implement your database checking logic here.
    
#     return