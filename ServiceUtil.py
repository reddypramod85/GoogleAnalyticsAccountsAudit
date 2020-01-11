from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
import json
from googleapiclient.errors import HttpError

def get_service(api_name, api_version, scopes, key_file_location):
    """Get a service that communicates to a Google API.

    Args:
        api_name: The name of the api to connect to.
        api_version: The api version to connect to.
        scopes: A list auth scopes to authorize for the application.
        key_file_location: The path to a valid service account JSON key file.

    Returns:
        A service that is connected to the specified API.
    """

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
            key_file_location, scopes=scopes)

    # Build the service object.
    service = build(api_name, api_version, credentials=credentials)

    return service

def call_back(request_id, response, exception):
  """Handle batched request responses."""
  print (request_id)
  if exception is not None:
    if isinstance(exception, HttpError):
      message = json.loads(exception.content)['error']['message']
      print ('Request %s returned API error : %s : %s ' %
             (request_id, exception.resp.status, message))
  else:
    print (response)