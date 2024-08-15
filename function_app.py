import azure.functions as func
import logging
import requests
import os
import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route('callWorkato', methods=['POST'])
def callWorkato(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    try:
        # parse the JSON request body
        req_body = req.get_json()
        message = req_body.get('Message')

        if not message:
            return func.HttpResponse(
                "Please pass a message in the request body",
                status_code=400
            )

        # define the API endpoint and headers
        workato_url = 'https://apid.kuokgroup.com.sg/sw-api-test-v1/sw-rec-dev-api-test'
        workato_token = os.getenv("WORKATO_API_TOKEN")
        
        headers = {
            "api-token": workato_token,
            "Content-Type": "application/json" # ensure the content type is set correctly
        }
    
        # payload for the POST request
        payload = {"Message": message}
        
        # make the POST request to the external API
        response = requests.post(workato_url, headers=headers, json=payload)
        response.raise_for_status() # raise an HTTPError for bad responses
    
        # parsing the response
        data = response.json()
    
        # return the data as JSON
        return func.HttpResponse(
            body=json.dumps(data),
            mimetype="application/json",
            status_code=200
        )
    
    except json.JSONDecodeError:
        logging.error("Invalid JSON in request body")
        return func.HttpResponse(
            "Invalid JSON in request body",
            status_code=400
        )
    
    except requests.exceptions.HTTPError as errh:
        logging.error(f"HTTP Error: {errh}")
        return func.HttpResponse(f"HTTP Error: {errh}", status_code=500)
    except requests.exceptions.ConnectionError as errc:
        logging.error(f"Error Connecting: {errc}")
        return func.HttpResponse(f"Error Connecting: {errc}", status_code=500)
    except requests.exceptions.Timeout as errt:
        logging.error(f"Timeout Error: {errt}")
        return func.HttpResponse(f"Timeout Error: {errt}", status_code=500)
    except requests.exceptions.RequestException as err:
        logging.error(f"Request Error: {err}")
        return func.HttpResponse(f"Request Error: {err}", status_code=500)
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return func.HttpResponse(
            "An unexpected error occurred.",
            status_code=500
        )
    
@app.route('getAllFolders', methods=['GET'])
def getAllFolders(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
 

    try:

        # Define headers and request body
        headers = {
            'accept': 'application/json',
            'authorization': f'Bearer {os.getenv("UIPATH_API_TOKEN")}'
        }

        # Make HTTP POST request to external API
        external_api_url = 'https://cloud.uipath.com/kslcorporateservicesptelted/Kuok_UAT/orchestrator_/odata/Folders'  # Replace with actual API endpoint
        response = requests.get(external_api_url, headers=headers)

        # Check if request was successful
        response.raise_for_status()

        # Assuming the API returns JSON, parse the response
        external_data = response.json()

        # Construct the response message
        return func.HttpResponse(f"Hello. External API response: {external_data}", status_code=200)
    
    except requests.exceptions.RequestException as e:
        return func.HttpResponse(f"Error occurred during external API request: {str(e)}", status_code=500)


@app.route('createNewFolder', methods=['POST'])
def createNewFolder(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    try:
        # parse the JSON request body
        req_body = req.get_json()
        message = req_body.get('Message')

        if not message:
            return func.HttpResponse(
                "Please pass a message in the request body",
                status_code=400
            )
        
        # Define headers and request body
        headers = {
            'accept': 'application/json',
            'authorization': f'Bearer {os.getenv("UIPATH_API_TOKEN")}',
            'Content-Type': 'application/json;odata.metadata=minimal;odata.streaming=true'
        }

        # Make HTTP POST request to external API
        external_api_url = 'https://cloud.uipath.com/kslcorporateservicesptelted/Kuok_UAT/orchestrator_/odata/Folders'
    
        # payload for the POST request
        payload = {
            "Key": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "DisplayName": "string",
            "FullyQualifiedName": "string",
            "Description": "string",
            "FolderType": "Standard",
            "ProvisionType": "Manual",
            "PermissionModel": "InheritFromTenant",
            "ParentId": 0,
            "ParentKey": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "FeedType": "Undefined",
            "Id": 0
        }
        
        # make the POST request to the external API
        response = requests.post(external_api_url, headers=headers, json=payload)
        response.raise_for_status() # raise an HTTPError for bad responses
    
        # parsing the response
        data = response.json()
    
        # return the data as JSON
        # return func.HttpResponse(
        #     body=json.dumps(data),
        #     mimetype="application/json",
        #     status_code=200
        # )

        return func.HttpResponse(f"Hello. External API response: {data}", status_code=200)

    except requests.exceptions.RequestException as e:
        return func.HttpResponse(f"Error occurred during external API request: {str(e)}", status_code=500)

    # except json.JSONDecodeError:
    #     logging.error("Invalid JSON in request body")
    #     return func.HttpResponse(
    #         "Invalid JSON in request body",
    #         status_code=400
    #     )
    
    # except requests.exceptions.HTTPError as errh:
    #     logging.error(f"HTTP Error: {errh}")
    #     return func.HttpResponse(f"HTTP Error: {errh}", status_code=500)
    # except requests.exceptions.ConnectionError as errc:
    #     logging.error(f"Error Connecting: {errc}")
    #     return func.HttpResponse(f"Error Connecting: {errc}", status_code=500)
    # except requests.exceptions.Timeout as errt:
    #     logging.error(f"Timeout Error: {errt}")
    #     return func.HttpResponse(f"Timeout Error: {errt}", status_code=500)
    # except requests.exceptions.RequestException as err:
    #     logging.error(f"Request Error: {err}")
    #     return func.HttpResponse(f"Request Error: {err}", status_code=500)
    # except Exception as e:
    #     logging.error(f"An unexpected error occurred: {e}")
    #     return func.HttpResponse(
    #         "An unexpected error occurred.",
    #         status_code=500
    #     )
