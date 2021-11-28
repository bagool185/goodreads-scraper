import json
import urllib.parse

import azure.functions as func
from azure.functions import HttpResponse

from models.BookSelection import BookSelectionList
from models.ErrorResponse import ErrorResponse
from services.goodreads_service import GoodreadsService


async def main(req: func.HttpRequest) -> func.HttpResponse:

    search_term: str = req.params.get('q')

    if not (search_term and search_term.strip()):
        err_res = ErrorResponse(
            code='missing_required_info',
            message='Query parameter "q" must be specified and it cannot be empty or whitespace'
        )

        return HttpResponse(body=err_res.json(by_alias=True), status_code=400, mimetype='application/json')

    # TODO: add validation for search limit
    search_limit: int = int(req.params.get('n')) if req.params.get('n') else None

    decoded_search_term: str = urllib.parse.unquote(search_term)
    goodreads_service = GoodreadsService()

    search_result: BookSelectionList = await goodreads_service.search_async(decoded_search_term, search_limit)

    if len(search_result.__root__) == 0:
        return HttpResponse(status_code=404)

    return HttpResponse(body=search_result.json(), status_code=200, mimetype='application/json')
