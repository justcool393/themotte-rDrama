################################################################
#                 WARNING! THIS FILE IS EVIL.                  #
################################################################
# Previously, this file had a series of                        #
#     from .alts import *                                      #
#     from .award import *                                     #
#     from .badges import *                                    #
# and so on in that fashion. That means that anywhere that     #
#     from files.classes import *                              #
# (and there were a lot of places like that) got anything      #
# was imported for any model imported. So if you, for example, #
# removed                                                      #
#     from secrets import token_hex                            #
# from files/classes/user.py, the registration page would      #
# break because files/routes/login.py did                      #
#     from files.classes import *                              #
# in order to get the token_hex function rather than           #
# importing it with something like                             #
#     from secrets import token_hex                            #
#                                                              #
# Anyway, not fixing that right now, but in order to           #
# what needed to be imported here such that                    #
#     from files.classes import *                              #
# still imported the same stuff as before I ran the following: #
#     $ find files/classes -type f -name '*.py' \              #
#         -exec grep import '{}' ';' \                         #
#         | grep 'import' \                                    #
#         | grep -v 'from [.]\|__init__\|from files.classes' \ #
#         | sed 's/^[^:]*://g' \                               #
#         | sort \                                             #
#         | uniq                                               #
# and then reordered the list such that import * did not stomp #
# over stuff that had been explicitly imported.                #
################################################################

# First the import * from places which don't go circular
from sqlalchemy import *

# Then everything except what's in files.*
import pyotp
import random
import re
import time
from copy import deepcopy
from datetime import datetime
from flask import g, render_template
from json import loads
from math import floor
from os import remove, path
from random import randint
from secrets import token_hex
from sqlalchemy.orm import aliased, deferred, relationship
from urllib.parse import urlencode, urlparse, parse_qs

# It is now safe to define the models
from .alts import Alt
from .award import AwardRelationship
from .badges import BadgeDef, Badge
from .clients import OauthApp, ClientAuth
from .comment import Comment
from .domains import BannedDomain
from .flags import Flag, CommentFlag
from .follows import Follow
from .marsey import Marsey
from .mod_logs import ModAction
from .notifications import Notification
from .saves import SaveRelationship, CommentSaveRelationship
from .submission import Submission
from .subscriptions import Subscription
from .user import User
from .userblock import UserBlock
from .usernotes import UserTag, UserNote
from .views import ViewerRelationship
from .votes import Vote, CommentVote
from .volunteer_janitor import VolunteerJanitorRecord
from .cron.tasks import RepeatableTask
from .cron.submission import ScheduledSubmissionTask
from .cron.pycallable import PythonCodeTask

# Then the import * from files.*
from files.helpers.config.const import *
from files.helpers.media import *
from files.helpers.lazy import lazy
from files.helpers.security import *

# Then the specific stuff we don't want stomped on
from files.classes.base import Base, CreatedBase
