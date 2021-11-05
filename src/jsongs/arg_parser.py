"""Parser for comand line arguments."""

import argparse

parser = argparse.ArgumentParser(
    description="Flask application that serves an audio file access api."
)
parser.add_argument("-c", "--config", metavar="PATH", type=str, help="config file path")
parser.add_argument("--musicdir", metavar="PATH", type=str, help="music directory PATH")
parser.add_argument("--ssl-cert", metavar="PATH", type=str, help="ssl certificate path")
parser.add_argument(
    "--ssl-privkey", metavar="PATH", type=str, help="ssl private key path"
)
parser.add_argument("--http", action="store_true", help="do not use https for server")
parser.add_argument(
    "--self-signed",
    action="store_true",
    help="use self-signed 'adhoc' certificate for ssh",
)

parser.add_argument("-p", "--port", metavar="", help="the port for the server to use")
parser.add_argument("--debug", action="store_true", help="use debugging")

group_one = parser.add_mutually_exclusive_group()
group_one.add_argument(
    "--example-config", action="store_true", help="print example config"
)
group_one.add_argument(
    "--create-config",
    metavar="PATH",
    type=str,
    help="guided config creation and save to PATH",
)
