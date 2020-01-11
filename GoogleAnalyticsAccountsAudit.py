"""A simple example of how to access the Google Analytics API."""

import json
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


GARemoveMsg=" has been removed. Please create a new google account with your HPE email id and reply back to this email with your HPE email id to create an account"
GAcreate = """ Create a Google Account with a company email address: \n\n1. Go to google.com/accounts/NewAccount in your Web browser.\n
2. Type in your company’s email address in the “Your current email address:” field.\n
3. Click on Use my current email address instead.\n
4. Type in a password for your Google account. This must be at least eight characters in length and should include a mixture of letters and numbers. Re-enter this password in the “Re-enter password:” field.\n
5. Select your location by clicking the drop-down menu next to “Location.”\n
6. Type in your birthday and the verification code under “Word Verification:.”\n
7. Click the “I accept. Create my account” button at the bottom of the page to create your Google account with a company email address.\n
8. Verify your email address by entering the verification code sent your email.\n
8. Log in to your company email. Open the email from Google regarding your new account. Click the confirmation link in the email to activate your Google account and complete the process with your company’s email address.\n"""


def google_analytics_audit(analytics):
    counter = 0
    try:
      accounts = AccountSummaries.main()
      #accounts = ['UA-107971078-1']
      #myEmail = ['reddypramod85@gmail.com','denis.choukroun51@gmail.com','didier.lalli@gmail.com']
      myEmail = ['reddypramod85@gmail.com']
      # print ('accounts: %s' % accounts)
      for account in accounts.get('items', []):
        print ('\n%s (%s) has (%d) properties\n' % (account.get('name'), account.get('id'), len(account.get('webProperties', []))))
        for property in account.get('webProperties', []):
          print ('   %s (%s)   [%s | %s]\n' % (property.get('name'), property.get('id'),property.get('websiteUrl'), property.get('level')))
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
                            if  userRef.get('email') and "gserviceaccount" not in userRef.get('email'):
                                counter += 1
                                #delete_prop_users(analytics, account.get('id'), property.get('id'), propertyUserLink.get('id'))
                                #print ('       Non HPE Email = %s     Domain = %s' % (userRef.get('email'), domain) )
                                #send_email(userRef.get('email'), "Your access to "+property.get('name')+" Google Analytics Account with email id: " +userRef.get('email') 
                                #+" has been removed. Please create a new google account with your HPE email id by following below steps and send an email to hpedev@hpe.com with your HPE email id to get back your access\n\n"+GAcreate)
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
                    #send_email(userRef.get('email'), "Your access to "+property.get('name')+" Google Analytics Account with email id: " +userRef.get('email') 
                    #+" has been removed. Please create a new google account with your HPE email id by following below steps and send an email to hpedev@hpe.com with your HPE email id to get back your access\n\n"+GAcreate)
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
    key_file_location = 'ga-api-test-pramod-bdbcfaf2b1cc.json'
    print ("inside Google Account Audit main")

    # Authenticate and construct service.
    service = get_service(
            api_name='analytics',
            api_version='v3',
            scopes=[scope],
            key_file_location=key_file_location)

    # call the list_account_summaries function to Requests a list of all account summaries for the authorized user.
    return google_analytics_audit(service)



if __name__ == '__main__':
    main()
