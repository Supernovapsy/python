# usage: python NETtalk_reminder.py <input info dict file> <outgoing email>
# The input file MUST be a dictionary with matching keyword values filled out
# in a dictionary called "info".

# The email will be also sent via cc to info@hackeracademy.org

import os
import argparse
from string import Template
from getpass import getpass
from Email import send_email

def main(args):
    body_template = Template("""\
Hi $name,
    Salute fellow hacker! You're at our Python NETtalk for $date.

    Hacker Academy has booked $location for this 50 minute NETtalk \
starting promptly at $time, we hope you're enjoying the talk.

Wen and Alan
Hacker Academy
University of Toronto\
    """)

    sender = "tonywli@hotmail.com"
    pwd = getpass()

    subject_template = Template("HA string.Template & smtplib demo $date $time "
    "$location_short")

    exec("from " + os.path.splitext(args.input_file)[0] + " import info")

    body = body_template.substitute(info)
    subject = subject_template.substitute(info)

    test_email = args.test if args.test else "tony.wenbo.li@gmail.com"

    if args.send:
        raw_input("Watch out! Email about to be sent!")
        send_email(
            sender, pwd, info["email"], subject, body,
            cc=["mailwen.li@mail.utoronto.ca",
            "alan.daniels@mail.utoronto.ca"])
    else:
        send_email(sender, pwd, info["email"], subject, body, test=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="input dict file")
    parser.add_argument("--sender", help="sender email if different from "
    "info@webdev.skule.ca.")
    parser.add_argument("--cc", nargs="*", help="cc")
    parser.add_argument("--bcc", nargs="*", help="bcc")
    parser.add_argument("-t", "--test", help="test email to send to")
    parser.add_argument("--send", action="store_true", help="Actually send "
    "the email instead of just testing")
    args = parser.parse_args()

    main(args)
