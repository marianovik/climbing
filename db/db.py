import logging

from db.core import Session

LOG = logging.getLogger("db.db")

query = Session.query
flush = Session.flush
commit = Session.commit
add = Session.add
remove = Session.remove
delete = Session.delete
rollback = Session.rollback
expunge = Session.expunge
info = Session.info
