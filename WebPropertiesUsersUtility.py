from googleapiclient.errors import HttpError

def delete_prop_users(analytics, account_id, property_id, link_id):
    """Delete users to a property User Link.

    Args:
      users: A list of user email addresses.
      permissions: A list of user permissions.
    Note: this code assumes you have MANAGE_USERS level permissions
    to each profile and an authorized Google Analytics service object.
    """
    try:

        # Construct the Profile User Link.
        link = analytics.management().webpropertyUserLinks().delete(
            accountId=account_id,
            webPropertyId=property_id,
            linkId=link_id
        ).execute()
        if link:
            print("+++++deleted+++++",account_id,link_id,link)
    except TypeError as error:
      # Handle errors in constructing a query.
      print ('There was an error in constructing your query : %s' % error)

    except HttpError as error:
      # Handle API errors.
      print ('There was an API error : %s : %s' %(error.resp.status, error.resp.reason))

def get_webproperty_UserLinks(analytics, account_id, property_id):
  property_links = analytics.management().webpropertyUserLinks().list(
              accountId=account_id,
              webPropertyId=property_id
              ).execute()
  return property_links