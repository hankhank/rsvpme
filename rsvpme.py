#! /usr/bin/env python
import optparse
import os
import time
import datetime
import re
from meetup import *

answermsg = 'Never gonna give up\nNever gonna let you down\nNever gonna miss another hack-and-tell'

def controller():
    opt = optparse.OptionParser(description='Fucking sick of missing things',
                        prog='rsvpme',
                        version="3.14",
                        usage="%prog [option] file/directory ")

    opt.add_option('--verbose', '-v',
            action = 'store_true',
            help='prints verbosely',
            default=False)

    opt.add_option('--name', '-n',
            action = 'store',
            help='name of specific meetup instance',
            default='.*')

    opt.add_option('--group', '-g',
            action = 'store',
            help='name of meetup group',
            default='hack-and-tell')

    opt.add_option('--apikey', '-a',
            action = 'store',
            help='your api key',
            default='nokey')
    
    options, arguments = opt.parse_args()

    eventre = re.compile('.*' + options.name + '.*')

    mup = Meetup(options.apikey)

    hacktellEvents = mup.get_events(group_urlname=options.group)
    for event in hacktellEvents.results:
        if eventre.match(event.name):
            waittime = 0
            if event.utc_rsvp_open_time != 'None':
                timeof = datetime.datetime.utcfromtimestamp(float(event.utc_rsvp_open_time)/1000.0)
                waittime = (timeof - 
                            datetime.datetime.utcnow() - 
                            datetime.timedelta(seconds=10)
                           ).total_seconds()
            print "Rsvpin to {}-{} in {} seconds".format(options.group, event.name, waittime)
            time.sleep(waittime)
            args = {'event_id': event.id, 'rsvp': 'yes'}
            while True:
                try: 
                    mup.post_rsvp(**args)
                    break
                except meetup_api_client.BadRequestError as ex:
                    time.sleep(1)


def main():
    controller()

if __name__ == '__main__':
    main()
