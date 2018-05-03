import os
import click


class LoadCommands(click.MultiCommand):
    def __init__(self):
        self.plugin_folder = os.path.join(os.path.dirname(__file__), 'commands')

    def list_commands(self, ctx):
        rv = []
        for filename in os.listdir(self.plugin_folder):
            if filename.endswith('.py'):
                rv.append(filename[:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        ns = {}
        fn = os.path.join(self.plugin_folder, name + '.py')
        with open(fn) as f:
            code = compile(f.read(), fn, 'exec')
            eval(code, ns, ns)
        return ns['cli']