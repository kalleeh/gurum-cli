import importlib
from configparser import NoSectionError, NoOptionError
import click
from gurumcommon.logger import configure_logger
from gurumcli.libs.config_manager import ConfigNotFoundException

LOGGER = configure_logger(__name__)

# Commands that are bundled with the CLI by default
_GURUM_CLI_COMMAND_PACKAGES = {
    "gurumcli.commands.apps.apps",
    "gurumcli.commands.configure",
    "gurumcli.commands.down",
    "gurumcli.commands.init",
    "gurumcli.commands.login",
    "gurumcli.commands.logout",
    "gurumcli.commands.pipelines.pipelines",
    "gurumcli.commands.services.services",
    "gurumcli.commands.up",
    "gurumcli.commands.users.users",
}


class BaseCommand(click.MultiCommand):
    """
    Dynamically loads commands. It takes a list of names of Python packages representing the commands, loads
    these packages, and initializes them as Click commands. If a command "hello" is available in a Python package
    "foo.bar.hello", then this package name is passed to this class to load the command. This allows commands
    to be written as standalone packages that are dynamically initialized by the CLI.

    Each command, along with any subcommands, is implemented using Click annotations. When the command is loaded
    dynamically, this class expects the Click object to be exposed through an attribute called ``cli``. If the
    attribute is not present, or is not a Click object, then an exception will be raised.

    For example: if "foo.bar.hello" is the package where "hello" command is implemented, then
    "/foo/bar/hello/__init__.py" file is expected to contain a Click object called ``cli``.

    The command package is dynamically loaded using Python's standard ``importlib`` library. Therefore package names
    can be specified using the standard Python's dot notation such as "foo.bar.hello".

    By convention, the name of last module in the package's name is the command's name. ie. A package of "foo.bar.baz"
    will produce a command name "baz".
    """

    def __init__(self, cmd_packages=None, *args, **kwargs):
        """
        Initializes the class, optionally with a list of available commands

        :param cmd_packages: List of Python packages names of CLI commands
        :param args: Other Arguments passed to super class
        :param kwargs: Other Arguments passed to super class
        """
        super(BaseCommand, self).__init__(*args, **kwargs)

        if not cmd_packages:
            cmd_packages = _GURUM_CLI_COMMAND_PACKAGES

        self._commands = {}
        self._commands = BaseCommand._set_commands(cmd_packages)

    def __call__(self, *args, **kwargs):
        """
        General exception handling for all commands. Useful for things in the Context object
        or exceptions that might be thrown across all commands.
        """
        try:
            return self.main(*args, **kwargs)
        except AttributeError as exc:
            if "'NoneType' object has no attribute 'get'" in exc.args:
                click.echo('Configuration file failed to load. Run "gurum configure".')
        except ConfigNotFoundException:
            click.echo('No config file found. Run "gurum configure" to set up a profile.')
        except NoSectionError as exc:
            click.echo('Profile not set up. Run "gurum configure (--profile)".')
        except NoOptionError as exc:
            if "id_token'" in exc.message:
                click.echo('Profile configured but no credentials present. Did you run "gurum login"?')
        except Exception as exc:
            click.echo('Unknown Error: %s' % exc)

    @staticmethod
    def _set_commands(package_names):
        """
        Extract the command name from package name. Last part of the module path is the command
        ie. if path is foo.bar.baz, then "baz" is the command name.

        :param package_names: List of package names
        :return: Dictionary with command name as key and the package name as value.
        """

        commands = {}

        for pkg_name in package_names:
            cmd_name = pkg_name.split('.')[-1]
            commands[cmd_name] = pkg_name

        return commands

    def list_commands(self, ctx):
        """
        Overrides a method from Click that returns a list of commands available in the CLI.

        :param ctx: Click context
        :return: List of commands available in the CLI
        """
        return list(self._commands.keys())

    def get_command(self, ctx, cmd_name):
        """
        Overrides method from ``click.MultiCommand`` that returns Click CLI object for given command name, if found.

        :param ctx: Click context
        :param cmd_name: Top-level command name
        :return: Click object representing the command
        """
        if cmd_name not in self._commands:
            LOGGER.error("Command %s not available", cmd_name)
            return

        pkg_name = self._commands[cmd_name]

        try:
            mod = importlib.import_module(pkg_name)
        except ImportError:
            LOGGER.exception("Command '%s' is not configured correctly. Unable to import '%s'", cmd_name, pkg_name)
            return

        if not hasattr(mod, "cli"):
            LOGGER.error("Command %s is not configured correctly. It must expose an function called 'cli'", cmd_name)
            return

        return mod.cli
