import click

from .context import Context


def debug_option(f):
    """
    Configures --debug option for CLI

    :param f: Callback Function to be passed to Click
    """
    def callback(ctx, _param, value):
        state = ctx.ensure_object(Context)
        state.debug = value
        return value

    return click.option('--debug',
                        expose_value=False,
                        is_flag=True,
                        envvar="GURUM_DEBUG",
                        help='Turn on debug logging to print debug message generated by GURUM CLI.',
                        callback=callback)(f)


def profile_option(f):
    """
    Configures --profile option for CLI

    :param f: Callback Function to be passed to Click
    """
    def callback(ctx, _param, value):
        state = ctx.ensure_object(Context)
        state.profile = value
        return value

    return click.option('--profile',
                        expose_value=False,
                        help='Select a specific profile.',
                        callback=callback)(f)
