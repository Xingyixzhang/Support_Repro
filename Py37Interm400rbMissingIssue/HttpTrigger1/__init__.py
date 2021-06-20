import logging
import os
import sys
import inspect
import azure.functions as func

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))


def main(req: func.HttpRequest) -> func.HttpResponse:
    """Accepts an HTTP request from the caller and a json document from an
    Azure blob storage account. If credentials are valid in the request, this
    will attempt to make an AzureAD Group with the provided information. Any
    response from graph.microsoft.com will be passed back to the caller.

    req: an HTTP request
    inputblob: a JSON document contining AAD public key info
    """

    logging.info('Python HTTP trigger function processed a request.')

    req_body = None
    if req.method == 'POST':
        try:
            req_body = req.get_json()
            logging.info(f'JSON payload: {req.get_json()}')
            logging.info(f'requestinfo: {inspect.getmembers(req)}')  # for AZ support. DELETE ME
        except ValueError as err:
            logging.error(f'could not decode JSON from request: {err}')
            logging.error(f'requestinfo: {inspect.getmembers(req)}')
            logging.error(f'requestHeaders: {inspect.getmembers(req.headers)}')
            logging.error(f'headers size: {sys.getsizeof(req.headers)} bytes')

            return func.HttpResponse(
                "HTTP request does not contain valid JSON data",
                status_code=400
            )

        return func.HttpResponse(
            status_code=200,
            body=f'echo body: {req_body}'
        )

    else:
        return func.HttpResponse(
            "Method not supported. https://github.comcast.com/public-cloud/AzureADGroups/blob/main/README.md#use",
            status_code=400
        )
