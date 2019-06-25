import argparse
import functools
import inspect
import json
import logging
import requests
import sys

from hubb_client import HubbClient

import requests_cache

requests_cache.install_cache()


def config_logging():
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stderr)
    handler.setLevel(logging.DEBUG)
    root.addHandler(handler)


def translate(a, b, fields):
  for new, old in fields.items():
    if old:
      a[new] = b[old]
  return a


def reducer(x, y):
  if not x:
    return [y]
  o = x[-1]
  if o['SessionId'] == y['SessionId']:
    o[y['PropertyMetadataId']] = y['Value']
  else:
    x.append({'SessionId': y['SessionId'], y['PropertyMetadataId']: y['Value']})
  return x

  # "TrackId": 16161,
  # "TimeSlotId": 92748,
  # "RoomId": 45414,

EVENT_ID = 2717

def export_all_talks(hc):
  session_fields = {'additional_notes': 'Id',
                    'title': 'Title',
                    'description': 'Description',
                    'start_time': 'StartTime',
                    'end_time': 'EndTime',
                    'room': 'room',
                    'slot': 'SlotDescription',
  }
  property_fields = {47953: 'talk_length',
                     47941: 'type',
                     47942: 'theme',
                     47943: 'audience_level',
                     47944: 'abstract',
                     47945: 'what_attendees_will_learn'
  }
  speaker_fields = { 'speaker_email': "EmailAddress",
                     'first_name': "FirstName",
                     'last_name': "LastName",
                     'speaker_biography': 'Biography',
                     'photo': 'PhotoLink'}

  # First get the users which is a list of objects [{"Id", ...},]
  users = hc.users(event_id=EVENT_ID)
  # And convert to dict of Ids {Id: {}, }
  users = {user['Id']: user for user in users}

  # Next get "property values"  [{"PropertyMetadataId", "SessionId", "Value" ...},]
  properties = hc.propertyvalues(event_id=EVENT_ID)
  # Filter down to the properties we're interested in
  properties = [p for p in properties if p['SessionId'] and p["PropertyMetadataId"] in property_fields]
  # Convert to dict of sessionids: {pid: value, ...}
  properties = sorted(properties, key=lambda p: p['SessionId'])
  properties = functools.reduce(reducer, properties, None)
  properties = {p['SessionId']: p for p in properties}

  # Get the rooms and convert to {Id: Name} map
  rooms = hc.rooms(event_id=EVENT_ID)
  rooms = {int(r['Id']): r['Name'] for r in rooms}

  # Get the timeslots and convert to {Id: {Start: t, End: t} map
  slots = hc.timeslots(event_id=EVENT_ID)
  slots = {s['Id']: s for s in slots}
  # Get the time slots


  export_data = []
  data = hc.sessions(event_id=EVENT_ID)
  for record in data:
    new_record = {}
    record['room'] = rooms[record['RoomId']]
    record['StartTime'] = slots[record['TimeSlotId']]['StartTime']['EventTime']
    record['EndTime'] = slots[record['TimeSlotId']]['EndTime']['EventTime']
    record['SlotDescription'] = slots[record['TimeSlotId']]['Label']
    translate(new_record, record, session_fields)
    new_record['additional_notes'] = str(new_record['additional_notes'])
    new_record['speakers'] = []
    for key in record['SpeakerOrder']:
      user = users[int(key)]
      new_record['speakers'].append(translate({}, user, speaker_fields))
    props = properties.get(record['Id'], {})
    for num, val in props.items():
      if num in property_fields:
        new_record[property_fields[num]] = val
    export_data.append(new_record)
  return json.dumps(export_data)


if __name__ == "__main__":
    config_logging()
    # Setup CLI options
    parser = argparse.ArgumentParser()
    # Gotta have a secrets file to read API creds
    txt = "Required. Json configuration file containing client_id, client_secret, and scope"
    parser.add_argument( "--config", help=txt, type=argparse.FileType("r"))
    args = parser.parse_args()
    if not args.config:
        parser.exit("Must supply secrets config file")
    secrets = json.load(args.config)
    # Make a client
    hc = HubbClient(**secrets)
    print(export_all_talks(hc))
