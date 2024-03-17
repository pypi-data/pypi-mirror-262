"""Console script for generating a report."""
import click
import logging
import os
import pathlib
import sys
import yaml

from rich.console import Console
from pathlib import Path

from .manager import Manager
from .console_helper import print_yellow, print_green
from .file_utils import check_infile_status
from . import constants

DEFAULT_OUTDIR = os.path.join(
    constants.DEFAULT_OUTDIR_BASE,
    os.path.splitext(os.path.basename(__file__))[0],
    constants.DEFAULT_TIMESTAMP,
)


error_console = Console(stderr=True, style="bold red")

console = Console()


def validate_verbose(ctx, param, value):
    """Validate the validate option.

    Args:
        ctx (Context): The click context.
        param (str): The parameter.
        value (bool): The value.

    Returns:
        bool: The value.
    """

    if value is None:
        click.secho("--verbose was not specified and therefore was set to 'True'", fg='yellow')
        return constants.DEFAULT_VERBOSE
    return value



@click.command()
@click.option(
    "--config_file",
    type=click.Path(exists=True),
    help=f"Optional: The configuration file for this project - default is '{constants.DEFAULT_CONFIG_FILE}'",
)
@click.option("--logfile", help="Optional: The log file")
@click.option(
    "--outdir",
    help=f"Optional: The default is the current working directory - default is '{DEFAULT_OUTDIR}'",
)
@click.option("--outfile", help="Optional: The output report file")
@click.option(
    "--template_file",
    help=f"Optional: The template file - default is '{constants.DEFAULT_TEMPLATE_FILE}'",
)

@click.option(
    '--verbose',
    is_flag=True,
    help=f"Will print more info to STDOUT - default is '{constants.DEFAULT_VERBOSE}'.",
    callback=validate_verbose
)

def main(
    config_file: str,
    logfile: str,
    outdir: str,
    outfile: str,
    template_file: str,
    verbose: bool,
):
    """Console script for generating a report."""
    error_ctr = 0

    if error_ctr > 0:
        return -1

    if config_file is None:
        config_file = constants.DEFAULT_CONFIG_FILE
        print_yellow(f"--config_file was not specified and therefore was set to '{config_file}'")

    check_infile_status(config_file)

    if template_file is None:
        template_file = constants.DEFAULT_TEMPLATE_FILE
        print_yellow(f"--template_file was not specified and therefore was set to '{template_file}'")

    check_infile_status(template_file)


    if outdir is None:
        outdir = DEFAULT_OUTDIR
        print_yellow(f"--outdir was not specified and therefore was set to '{outdir}'")

    if not os.path.exists(outdir):
        pathlib.Path(outdir).mkdir(parents=True, exist_ok=True)
        print_yellow(f"Created output directory '{outdir}'")

    if logfile is None:
        logfile = os.path.join(
            outdir, os.path.splitext(os.path.basename(__file__))[0] + ".log"
        )
        print_yellow(f"--logfile was not specified and therefore was set to '{logfile}'")

    if outfile is None:
        outfile = os.path.join(
            outdir, os.path.splitext(os.path.basename(__file__))[0] + ".report.html"
        )
        print_yellow(f"--outfile was not specified and therefore was set to '{outfile}'")


    logging.basicConfig(
        filename=logfile,
        format=constants.DEFAULT_LOGGING_FORMAT,
        level=constants.DEFAULT_LOGGING_LEVEL,
    )

    # Read the configuration from the JSON file and
    # load into dictionary.
    logging.info(f"Will load contents of config file '{config_file}'")
    config = yaml.safe_load(Path(config_file).read_text())


    manager = Manager(
        config=config,
        config_file=config_file,
        executable=os.path.abspath(__file__),
        logfile=logfile,
        outdir=outdir,
        outfile=outfile,
        template_file=template_file,
        verbose=verbose
    )

    manager.register_data_file(
        constants.DEFAULT_CONFIG_FILE,
        "The configuration file",
        "The YAML configuration file for this project."
    )

    manager.register_data_file(
        os.path.join(
            os.path.dirname(__file__),
            "constants.py"
        ),
        "The constants file",
        "The Python constants file for this project."
    )

    manager.add_runtime_parameter(
        "--logfile",
        os.path.abspath(logfile),
        "The log file",
        "The Python logging log file."
    )

    manager.add_runtime_parameter(
        "--template_file",
        os.path.abspath(template_file),
        "The template file",
        "The Python Jinja2 template file use to generate this report."
    )

    lookup = [
        {
            "key": "A",
            "val": "The first letter of the alphabet"
        },
        {
            "key": "B",
            "val": "The second letter of the alphabet"
        },
        {
            "key": "C",
            "val": "The third letter of the alphabet"
        }
    ]

    manager.generate_report(lookup)

    if verbose:
        console.print(f"The log file is '{logfile}'")
        print_green(f"Execution of '{os.path.abspath(__file__)}' completed")

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
