import subprocess

def get_user_info(email, fields):

  ldapsearch = "/usr/bin/ldapsearch"
  host = 'ldap.hp.com'
  baseDN = 'ou=people,o=hp.com'
  searchFilter = '(&(uid=' + email + '))'
  # #  .\ldapsearch.exe '-x', '-LLL', '-h' 'ldap.hp.com' '-b' 'ou=people,o=hp.com', '(&(uid=pramod-reddy.sareddy@hpe.com))'

  cmd = [ldapsearch, '-x', '-LLL', '-h', host, '-b', baseDN, searchFilter] + fields

  result = {}
  # output = subprocess.check_output(["echo", "Hello World!"])
  # print ("output",output)
  output = subprocess.check_output(cmd).decode("utf-8").split('\n')
  for line in output:
    if ":" in line:
      attribute, value = line.split(':', 1)
      attribute = attribute.strip()
      value = value.strip()
      result.update({attribute: value})
  return result
  # if ":" in (output):
  #   attribute, value = output.split(':', 1)
  #   print ("attribute",attribute,value)
  # output.split('\n')
  # print ("output after split",output)
  # for line in output:
  # if ":" in output:
  #     attribute, value = output.split(':', 1)
  #     attribute = attribute.strip()
  #     value = value.strip()
  #     result.update({attribute: value})
  # return result

def main():
  email = "peng.liu@hpe.com"
  fields = ["cn", "hpStatus"]

if __name__ == '__main__':
  import sys
  main()
