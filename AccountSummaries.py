"""A simple example of how to access the Google Analytics API."""

import json
from googleapiclient.errors import HttpError
from googleapiclient.http import BatchHttpRequest
import httplib2
from oauth2client import client
from oauth2client import file
from oauth2client import tools
from ServiceUtil import get_service

def list_account_summaries(analytics):
    try:
      account_summaries = analytics.management().accountSummaries().list().execute()
      #print ('account_summaries: %s' % account_summaries)
      print ('\n ***** Audit is running against below: %s accounts *****' % len(account_summaries.get('items', [])))
      for account in account_summaries.get('items', []):
        print ('\n%s (%s)' % (account.get('name'), account.get('id')))
        # print_property_summaries(account)

    except TypeError as error:
      # Handle errors in constructing a query.
      print ('There was an error in constructing your query : %s' % error)
    except HttpError as error:
      # Handle API errors.
      print ('There was an API error : %s : %s' % (error.resp.status, error.resp.reason))

    return account_summaries

def print_property_summaries(account_summary):
  if account_summary:
    for property in account_summary.get('webProperties', []):
      print ('   %s (%s)' % (property.get('name'), property.get('id')))
      print ('   [%s | %s]' % (property.get('websiteUrl'), property.get('level')))
      print_profile_summary(property)

def print_profile_summary(property_summary):
  if property_summary:
    for profile in property_summary.get('profiles', []):
      print ('     %s (%s) | %s' % (profile.get('name'), profile.get('id'),
                                   profile.get('type')))

def main():
    # Define the auth scopes to request.
    scope = 'https://www.googleapis.com/auth/analytics.edit'
    key_file_location = 'ga-api-test-pramod-bdbcfaf2b1cc.json'

    # Authenticate and construct service.
    service = get_service(
            api_name='analytics',
            api_version='v3',
            scopes=[scope],
            key_file_location=key_file_location)

    # call the list_account_summaries function to Requests a list of all account summaries for the authorized user.
    return list_account_summaries(service)



if __name__ == '__main__':
    main()
