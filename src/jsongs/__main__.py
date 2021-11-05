"""Jsongs program main funtion."""

import os
from flask_restful.reqparse import Namespace

from .arg_parser import parser as argparser
from .app import app

"""Configure the app"""
args = argparser.parse_args()
args.config = args.config or os.environ.get("JSONGS_CONFIG")
args.http = (
    int(os.environ["NO_SSL"]) and args.http if "NO_SSL" in os.environ else args.http
)


def main(args: Namespace):
    """Main entery function"""

    ssl = (args.ssl_cert, args.ssl_privkey)
    ssl = ("" in ssl and not args.http and ssl) or (not args.http and "adhoc") or None
    app.run(
        debug=args.debug,
        threaded=True,
        port=args.port or 8080,
        host="0.0.0.0",
        ssl_context=ssl,
    )


main(args)
