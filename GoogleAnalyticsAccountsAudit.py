"""A script to manage the Google Analytics Account Users."""

import json
import yaml
from googleapiclient.errors import HttpError
from googleapiclient.http import BatchHttpRequest
import httplib2
from oauth2client import client
from oauth2client import file
from oauth2client import tools
from ServiceUtil import get_service
import AccountSummaries
from email.mime.text import MIMEText
import smtplib
from HpeLdapSearch import get_user_info
from WebPropertiesUsersUtility import get_webproperty_UserLinks,delete_prop_users
from ProfileUserLinksUtility import get_profile_user_links

def google_analytics_audit(analytics,cfg):
    counter = 0
    account_owner=""
    emailMessage = str(cfg['DisclaimerMsg']+cfg['GARemoveMsg'] +cfg['GAcreate'])
    try:
      accounts = AccountSummaries.main()
      myEmail = ['reddypramod85@gmail.com']
      for account in accounts.get('items', []):
        print ('\n%s (%s) has (%d) properties\n' % (account.get('name'), account.get('id'), len(account.get('webProperties', []))))
        if account.get('name') == "design@hpe":
          account_owner=cfg['HPEDesignAccountOwner']
        elif account.get('name') == "developer portal":
          account_owner=cfg['HPEDEVAccountOwner']
        elif account.get('name') == "Grommet":
          account_owner=cfg['GrommetAccountOwner']
        elif account.get('name') == "HPE GreenLake":
          account_owner=cfg['HPEGreenLakeccountOwner']
        elif account.get('name') == "HPE OneSphere":
          account_owner=cfg['HPEOneSphereAccountOwner']
        elif account.get('name') == "HPE OneView":
          account_owner=cfg['OneViewAccountOwner']
        elif account.get('name') == "hpe.global.dashboard":
          account_owner=cfg['HPEGlobalDashccountOwner']
        else:
          account_owner="hpedev@hpe.com"
        for property in account.get('webProperties', []):
          print ('   %s (%s)   [%s | %s]\n' % (property.get('name'), property.get('id'),property.get('websiteUrl'), property.get('level')))
          print('       account owner %s\n' % account_owner)
          try:
            property_links = get_webproperty_UserLinks(analytics, account.get('id'), property.get('id')) 
          except HttpError as error:
            # Handle API errors.
            if error.resp.status == 403:
                    hpeEmailList = []
                    nonHpeEmailList = []
                    counter = 0  
                    for view in property.get('profiles', []):
                      # Construct the Profile User Link.
                      links = get_profile_user_links(analytics, account.get('id'), property.get('id'), view.get('id'))
                      for property in links.get('items', []):
                        userRef = property.get('userRef')
                        domain = userRef.get('email').split('@')[1]
                        if domain == "hpe.com":
                            counter += 1
                            employee_details = get_user_info(userRef.get('email'),['cn'])
                            if not employee_details:
                              hpeEmailList.append(userRef.get('email'))
                        else:
                            #if  userRef.get('email') and userRef.get('email') in myEmail and "gserviceaccount" not in userRef.get('email'):
                            if  userRef.get('email') and "gserviceaccount" not in userRef.get('email'):
                                counter += 1
                                #delete_prop_users(analytics, account.get('id'), property.get('id'), propertyUserLink.get('id'))
                                #send_email(userRef.get('email'), emailMessage.format(property.get('name'), userRef.get('email'), account_owner ))
                                nonHpeEmailList.append(userRef.get('email'))
          if counter == 0:
            hpeEmailList = []
            nonHpeEmailList = []              
          for propertyUserLink in property_links.get('items', []):
            userRef = propertyUserLink.get('userRef', {})
            domain = userRef.get('email').split('@')[1]
            if domain == "hpe.com":
                employee_details = get_user_info(userRef.get('email'),['cn'])
                if not employee_details:
                  hpeEmailList.append(userRef.get('email'))
            else:
                #if  userRef.get('email') and userRef.get('email') in myEmail and "gserviceaccount" not in userRef.get('email'):
                if  userRef.get('email') and "gserviceaccount" not in userRef.get('email'):
                    #delete_prop_users(analytics, account.get('id'), property.get('id'), propertyUserLink.get('id'))
                    #send_email(userRef.get('email'), emailMessage.format(property.get('name'), userRef.get('email'), account_owner ))
                    nonHpeEmailList.append(userRef.get('email'))
          print("      HPE User(s) count to be removed is '{0}' and their email address are '{1}'\n" .format(len(hpeEmailList), hpeEmailList))
          print("      Non HPE User(s) count to be removed is '{0}' and their email address are '{1}'\n" .format(len(nonHpeEmailList), nonHpeEmailList))

    except TypeError as error:
      # Handle errors in constructing a query.
      print ('There was an error in constructing your query : %s' % error)
    except HttpError as error:
      # Handle API errors.
      print ('There was an API error : %s : %s' % (error.resp.status, error.resp.reason))

    return None

#
# Send email message of results to specified address
#
def send_email(address, output):
      
  msg = MIMEText(output)
  msg['Subject'] = "Google Analytics Account user audit"
  msg['From'] = "hpedev@hpe.com"
  msg['To'] = address
  # print("message",msg)

  s = smtplib.SMTP('smtp3.hpe.com')
  s.sendmail('hpedev@hpe.com', address, msg.as_string())
  s.quit()

def main():
    # Define the auth scopes to request.
    scope = 'https://www.googleapis.com/auth/analytics.manage.users'
 
    with open('config.yaml', 'r') as ymlfile:
        print("yaml", ymlfile)
        try:
            cfg = yaml.load(ymlfile, Loader=yaml.SafeLoader)
            print(cfg['SecretKeyFile'])
        except yaml.YAMLError as exc:
            print(exc)

    print ("inside Google Account Audit main")

    # Authenticate and construct service.
    service = get_service(
            api_name='analytics',
            api_version='v3',
            scopes=[scope],
            key_file_location=cfg['SecretKeyFile'])

    # call the list_account_summaries function to Requests a list of all account summaries for the authorized user.
    return google_analytics_audit(service,cfg)



if __name__ == '__main__':
    main()
