import click
import pkg_resources
from luminos.app import App
from luminos.logger import logger
import os
import yaml

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

    provider, model_name = model.split("/") if model else (None, None)
    
    rc_file_path = os.path.join(directory if directory else '.', '.luminos_rc.yaml')
    preload_prompt = None
    autorun = False

    if os.path.exists(rc_file_path):
        while True:
            user_input = input(f".luminos_rc.yaml detected in {directory or '.'}. Would you like to use it? (yes/no): ").strip().lower()
            if user_input in ['yes', 'y']:
                with open(rc_file_path, 'r') as file:
                    rc_config = yaml.safe_load(file)
                preload_prompt = rc_config.get('prompt', '')
                autorun = rc_config.get('autorun', False)
                model_name = rc_config.get('defaults', {}).get('model', model_name)
                provider = rc_config.get('defaults', {}).get('provider', provider)
                break
            elif user_input in ['no', 'n']:
                break
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")
    
    app = App()

    if preload_prompt and autorun:
        execute_ai_with_prompt(preload_prompt)

    app.start(permissive=permissive, directory=directory if directory else '.', model_name=model_name, provider=provider, verbose=verbose, api_key=api_key, preload_prompt=preload_prompt)

def execute_ai_with_prompt(prompt):
    print(f"Executing AI with prompt: {prompt}")
    # Placeholder for AI execution logic
    # Do not exit the program, just ensure the prompt is handled appropriately

if __name__ == "__main__":
    main()
