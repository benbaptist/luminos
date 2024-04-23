import click
import pkg_resources
from luminos.app import App
from luminos.logger import logger

@click.command()
@click.option('--permissive', '-p', is_flag=True, default=False, help='Automatically grant permission for all safe operations.')
@click.option('--model', '-m', help='Model provider and name in format provider/model_name')
@click.option('--api-key', '-k', help='API key for model provider')
@click.option('--verbose', '-v', is_flag=True, default=False, help='Spit out more information when making requests')
@click.argument('directory', required=False, type=click.Path(exists=True, file_okay=False))
def main(permissive, model, api_key, verbose, directory):
    try:
        __version__ = pkg_resources.get_distribution("luminos").version
    except pkg_resources.DistributionNotFound:
        __version__ = "unknown"

    logger.info(f"Luminos version: {__version__}")
    # Split the model provider and name
    provider, model_name = model.split("/") if model else (None, None)
    
    app = App()
    app.setup_logging(verbose=verbose)
    app.start(permissive=permissive, directory=directory if directory else '.', model_name=model_name, provider=provider, api_key=api_key)

if __name__ == "__main__":
    main()
