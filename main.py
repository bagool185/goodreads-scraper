import asyncio

from services.goodreads_service import GoodreadsService, BookSelectionDetails


async def main():
    goodreads_service = GoodreadsService()
    top_results = await goodreads_service.search_async('kafka')
    detailed_book_selection: BookSelectionDetails = await goodreads_service.parse_detailed_book_view_async(top_results[0])
    print(detailed_book_selection.json())

# windows specific bs
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())
