#!/usr/bin/python
from __future__ import print_function

import argparse
import syslog
import time
import errno
import os
import stat
import subprocess
import getpass
import pwd
import grp

def logFormat( message ):
  print (time.strftime("%b %d %H:%M:%S "), message)
  syslog.syslog(message)


parser = argparse.ArgumentParser()
parser.add_argument("role", help="The name of the Ansible role you wish to create.")
parser.add_argument("group", help="The group that will share ownership of the repo.")
args = parser.parse_args()

#print ("Creating Ansible role {}.".format(args.role))
logFormat ("Creating Ansible role {}.".format(args.role))
print 

try:
  # Print without line end but the else of the try/elif/else doesn't work
  #print('Attempting to create {} directory.'.format(args.role), end='')
  logFormat ("Creating {} directory.".format(args.role))
  os.makedirs(args.role)
except OSError as e:
  if e.errno != errno.EEXIST:
    raise
  elif e.errno == errno.EEXIST:
    logFormat ("Directory exists, continuing.")
  else:
    logFormat ("Success!")

try:
  logFormat ("Change ownership on directory {}".format(args.role))
  # get the username for the chown
  user_name = getpass.getuser()
  # get the uid
  uid = pwd.getpwnam(user_name).pw_uid
  # get information about group arguement
  gid = grp.getgrnam(args.group)
  # change ownership of role directory
  os.chown(args.role, uid, gid.gr_gid)
except:
  logFormat ("Error setting ownership on directory {}".format(args.role))
  raise

try:
  logFormat ("Setting permissions on directory {}.".format(args.role))
  os.chmod(args.role, stat.S_IRWXU | stat.S_IRWXG | (stat.S_ISGID | 8) | stat.S_IROTH | stat.S_IXOTH)
except:
  logFormat ("Error setting permissions on directory {}".format(args.role))
  raise

try:
  logFormat ("Creating Ansible role in {}.".format(args.role))
  logFormat (subprocess.check_output(["ansible-galaxy", "init", "--force", args.role]))
except:
  logFormat ("Error creating ansible role.")
  raise

try:
  logFormat ("Creating git repository in {}.".format(args.role))
  logFormat (subprocess.check_output(["git", "init", "--shared=group", args.role]))
except:
  logFormat ("Error creating git repository.")
  raise
