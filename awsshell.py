#!/usr/bin/env python
import subprocess
import os
import shlex
import boto3
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--profile", type=str,  default="saml",
                    help='name of your AWS profile in ~/.aws/config file')
parser.add_argument("--region", type=str,  default="us-east-1",
                    help='name of AWS_REGION')
args = parser.parse_args()

sess = boto3.session.Session(profile_name=args.profile)
sts_connection = sess.client('sts')
credentials = sess.get_credentials().get_frozen_credentials()

env_vars = dict()
env_vars['aws_access_key_id'] = credentials.access_key
env_vars['aws_secret_access_key'] = credentials.secret_key
if credentials.token:
    env_vars['aws_session_token'] = credentials.token

my_env = os.environ.copy()

for k, v in env_vars.items():
    my_env[k.upper()] = v

my_env["AWS_DEFAULT_REGION"] = args.region
args = shlex.split("bash")
print("\n#############")
print("Setting up AWS shell with access keys. 'exit' when finished")
print("#############\n")
subprocess.run(args, env=my_env, shell="True")
