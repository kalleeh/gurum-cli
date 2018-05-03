import os
import sys
import click

plugin_folder = os.path.join(os.path.dirname(__file__), 'commands')


class UsersCommands(click.MultiCommand):
    def list_commands(self, ctx):
        rv = []
        for filename in os.listdir(plugin_folder):
            if filename.endswith('.py'):
                rv.append(filename[:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        ns = {}
        fn = os.path.join(plugin_folder, name + '.py')
        try:
            with open(fn) as f:
                code = compile(f.read(), fn, 'exec')
                eval(code, ns, ns)
            return ns['cli']
        except IOError:
            return None


@click.group(cls=UsersCommands, help="User management")
def users():
    pass
