# -*- coding: utf-8 -*-

from playhouse.migrate import *
import config


def run_migrate():
    print('Begin migrate ...')
    migrator = PostgresqlMigrator(config.dbconnect)
    status_field = IntegerField(null=False, default=0)
    try:
        migrate(migrator.add_column('tabapp', 'valid', status_field))
    except:
        pass
    try:
        migrate(migrator.drop_column('cabmember', 'valid'))
    except:
        pass



    try:
        migrate(migrator.add_column('cabmember', 'time_login', status_field))
    except:
        pass
    try:
        migrate(migrator.add_column('cabmember', 'time_create', status_field))
    except:
        pass

    try:
        migrate(migrator.add_column('cabmember', 'time_update', status_field))
    except:
        pass

    try:
        migrate(
            migrator.rename_column('cabmember', 'reset_passwd_timestamp', 'time_reset_passwd')
        )
    except:
        pass

    print('QED')
