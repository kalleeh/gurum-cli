import click
import json

from gureume.cli import pass_context


@click.command('test', short_help='Test command for CLI')
@click.argument('name')
@click.option('--tasks', prompt=False, default='1', help='Number of tasks to run')
@click.option('--health-check-path', prompt=False, help='Path that is queried for health checks')
@click.option('--image', prompt=False, default='nginx:latest', help='Docker image to run')
@pass_context
def cli(ctx, name, **kwargs):
    """Test arguments"""
    print('Name: ' + name)

    print('kwargs:')
    print(kwargs)

    filtered = json.dumps({k: v for k, v in kwargs.items() if v is not None})

    print('Filtered kwargs:')
    print(filtered)