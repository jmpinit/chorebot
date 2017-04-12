#!/usr/bin/env python

import os, json, datetime
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
LAST_ACTUATOR_FILE = os.path.join(SCRIPT_DIR, "last_actuator.json")
LOG_FILE = os.path.join(SCRIPT_DIR, "logfile.txt")
CONFIG_FILE = os.path.join(SCRIPT_DIR, "config.json")

def die(msg):
  print(msg)
  exit(1)

def log(msg):
  with open(LOG_FILE, "a") as logfile:
    logfile.write(msg) 

def validate_config(config):
  keys = [
    "robot_name",
    "hackerspace_mailing_list",
    "subject_line",
    "actuators",
    "api_key",
    "mailgun_domain",
  ]

  for key in keys:
    if not key in config:
      die("Must specify \"{0}\" in config.json".format(keyA))

  if len(config["actuators"]) == 0:
    die("I am but ephemeral infrastructure. I need actuators to enact my will upon Earth. List them in config.json.")
  elif len(config["actuators"]) == 1:
    poorSoul = config["actuators"][0]
    die("If {} is the only actuator, just tell them to always do the chores. You don't need my help.".format(poorSoul))

def generate_chore_message(config):
  if os.path.isfile(LAST_ACTUATOR_FILE):
    with open(LAST_ACTUATOR_FILE) as lastActuatorFile:
      lastActuator = json.load(lastActuatorFile)
  else:
    # FIXME: Function doing more than what is advertised on the tin
    with open(LAST_ACTUATOR_FILE, "w") as lastActuatorFile:
      lastActuatorFile.write(json.dumps(config["actuators"][-1]))

    lastActuator = config["actuators"][-1]

  indexOfLast = config["actuators"].index(lastActuator)
  currentActuator = config["actuators"][(indexOfLast + 1) % len(config["actuators"])]
  nextActuator = config["actuators"][(indexOfLast + 2) % len(config["actuators"])]

  messageForCurrentActuator = "@{}: you are up for this week (start of day {} to end of day {})\n".format(currentActuator, str(datetime.date.today()), str(datetime.date.today() + datetime.timedelta(days=6)))
  messageForNextActuator = "@{}: you are up after that\n".format(nextActuator)

  # FIXME: Function doing more than what is advertised on the tin
  with open(LAST_ACTUATOR_FILE, "w") as lastActuatorFile:
    lastActuatorFile.write(json.dumps(currentActuator))

  return "{}\n{}".format(messageForCurrentActuator, messageForNextActuator)

def main():
  with open(CONFIG_FILE) as configFile:
    config = json.load(configFile)

  validate_config(config)
  messageText = generate_chore_message(config)

  command = ' '.join(["/bin/bash -c \"set -o xtrace; set -o errexit; curl", '-s',
    '--user', "'api:{}'".format(config["api_key"]),
    'https://api.mailgun.net/v3/{}/messages'.format(config["mailgun_domain"]),
    '-F', "from='{} <mailgun@{}>'".format(config["robot_name"], config["mailgun_domain"]),
    '-F', 'to={}'.format(config["hackerspace_mailing_list"]),
    '-F', "subject='{}'".format(config["subject_line"]),
    '-F', "text=\\'$'{}'\\'".format(messageText.replace('\n', '\\n')),
    '\"',
  ])

  print subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.read()

main()
