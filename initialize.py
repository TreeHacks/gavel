# Copyright (c) 2015-2019 Anish Athalye (me@anishathalye.com)
#
# This software is released under AGPLv3. See the included LICENSE.txt for
# details.


def rebuild():
    from gavel.models import db
    db.reflect()
    db.drop_all()
    db.create_all()


if __name__ == '__main__':
    rebuild()