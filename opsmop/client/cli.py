
# Copyright 2018 Michael DeHaan LLC, <michael@michaeldehaan.net>
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import argparse

from opsmop.callbacks.local import LocalCallbacks
from opsmop.callbacks.common import CommonCallbacks
from opsmop.core.api import Api
from opsmop.core.errors import OpsMopError

# import argparse


USAGE = """
|
| opsmop - (C) 2018, Michael DeHaan LLC
|
| opsmop --validate demo/policy.py 
| opsmop --check demo/policy.py
| opsmop --apply demo/policy.py  
|
"""

class Cli(object):

    __slots__ = [ 'args' ]

    def __init__(self, args):
        """
        The CLI is constructed with the sys.argv command line, see bin/opsmop
        """
        self.args = args
 
    def go(self):
       
        if len(self.args) < 3 or sys.argv[1] == "--help":
            print(USAGE)
            sys.exit(1)

        mode = self.args[1]
        path = sys.argv[2]
        callbacks = [ LocalCallbacks(), CommonCallbacks() ]


        parser = argparse.ArgumentParser()
        parser.add_argument('--validate', help='policy file to validate')
        parser.add_argument('--apply', help="policy file to apply")
        parser.add_argument('--check', help="policy file to check")
        parser.add_argument('--tags', help='optional comma seperated list of tags')

        args = parser.parse_args(self.args[1:])

        all_modes = [ args.validate, args.apply, args.check ]
        selected_modes = [ x for x in all_modes if x is not None ]
        if len(selected_modes) != 1:
            print(USAGE)
            sys.exit(1)

        path = args.validate or args.apply or args.check

        tags = None
        if args.tags is not None:
            tags = args.tags.strip().split(",")

        api = Api.from_file(path=path, callbacks=callbacks, tags=tags)
        
        try:
            if args.validate:
                # just check for missing files and invalid types
                api.validate()
            elif args.check:
                # operate in dry-run mode
                api.check()
            elif args.apply:
                # configure everything
                api.apply()
            else:
                print(USAGE)
                sys.exit(1)
        except OpsMopError as ome:
            print("")
            print(str(ome))
            print("")
            sys.exit(1)


        print("")
        sys.exit(0)


def main():
    Cli(sys.argv).go()