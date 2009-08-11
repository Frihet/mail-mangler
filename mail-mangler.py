#! /usr/bin/python

import sys, email.Parser, smtplib

# Read configuration file
# See mail-mangler.config for mor details
config = open(sys.argv[1])
exec config
config.close()

parser = email.Parser.Parser()
sender = smtplib.SMTP('localhost')

msg = parser.parse(sys.stdin)
assert not msg.is_multipart()

# This makes the interface uniform to headers and body alike... The
# body is accessed as a "header" called "Body".
class FieldHandler(object):
    def __init__(self, msg):
        self.msg = msg
    def __getitem__(self, name):
        if name == "Body":
            return self.msg.get_payload()
        else:
            return self.msg[name]
    def __setitem__(self, name, value):
        if name == "Body":
            self.msg.set_payload(value)
        else:
            del self.msg[name]
            self.msg[name] = value

# Mangle message - %(name)s in replacement value refers to the
# original values in the message, before _any_ replacemenst have been
# made
msg_fieldhandler = FieldHandler(msg)
for name, value in ((name, value % msg_fieldhandler)
                    for name, value
                    in mangling.iteritems()):
    msg_fieldhandler[name] = value

# Send off the message :)
sender.sendmail(msg['From'], msg['To'].split(','), msg.as_string())

sender.quit()
