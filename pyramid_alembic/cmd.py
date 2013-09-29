import os
import optparse
import sys
import textwrap
from pyramid.paster import bootstrap

from alembic.config import Config as AlembicConfig, CommandLine


def run_alembic():  # pragma: no cover

    description = """\
        pyramid wrapper for alembic
    """
    usage = "usage: %prog `config_uri` `alembic_command` [alembic options]"
    parser = optparse.OptionParser(
        usage=usage,
        description=textwrap.dedent(description)
    )

    options, args = parser.parse_args(sys.argv[1:])
    if not len(args) >= 2:
        parser.print_help()
        return 2

    config_uri = args[0]
    env = bootstrap(config_uri)

    # gettin app config
    config = env['registry']['config']
    alembic_cfg = AlembicConfig()

    migrations_path = os.getcwd() + '/migrations'
    if 'alembic' in config and config.alembic.get('location'):
        migrations_path = config.alembic.location

    alembic_cfg.set_main_option('script_location', migrations_path)

    alembic_command = CommandLine(args[1])
    alembic_command.run_cmd(alembic_cfg, alembic_command.parser.parse_args(args[2:]))
