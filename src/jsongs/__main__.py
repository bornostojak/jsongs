"""Jsongs program main funtion."""

import os
from flask_restful.reqparse import Namespace

from .arg_parser import parser as argparser
from .app import app

aparser = argparser.parse_args()
aparser.config = aparser.config or os.environ.get("JSONGS_CONFIG")
aparser.http = (
    int(os.environ["NO_SSL"]) and aparser.http
    if "NO_SSL" in os.environ
    else aparser.http
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


main(aparser)
