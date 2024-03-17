import logging
import os
import sys

from datetime import datetime
from rich.console import Console
from rich.table import Table
from typing import Any, Dict, List, Optional
from jinja2 import Template

from . import constants
from .console_helper import print_yellow, print_red
from .file_utils import check_infile_status, calculate_md5



console = Console()

DEFAULT_TEST_MODE = False

# If the following is set to True, the manager will add provenance information to the report.
DEFAULT_ADD_PROVENANCE = True

# If the following is set to True, the manager will add data files metadata to the report.
DEFAULT_ADD_DATA_FILES_METADATA = True

# If the following is set to True, the manager will add runtime parameters to the report.
DEFAULT_ADD_RUNTIME_PARAMETERS = True


DEFAULT_OUTDIR = os.path.join(
    constants.DEFAULT_OUTDIR_BASE,
    os.path.splitext(os.path.basename(__file__))[0],
    constants.DEFAULT_TIMESTAMP,
)


class Manager:

    def __init__(self, **kwargs):
        self.config = kwargs.get("config", None)
        self.add_provenance = kwargs.get("add_provenance", None)
        self.add_data_files_metadata = kwargs.get("add_data_files_metadata", None)
        self.add_runtime_parameters = kwargs.get("add_runtime_parameters", None)
        self.config_file = kwargs.get("config_file", constants.DEFAULT_CONFIG_FILE)
        self.executable = kwargs.get("executable", None)
        self.outdir = kwargs.get("outdir", DEFAULT_OUTDIR)
        self.logfile = kwargs.get("logfile", None)
        self.outfile = kwargs.get("outfile", None)
        self.template_file = kwargs.get("template_file", None)
        self.verbose = kwargs.get("verbose", constants.DEFAULT_VERBOSE)

        if self.add_provenance is None or self.add_provenance == "":
            self.add_provenance = self.config.get("add_provenance", DEFAULT_ADD_PROVENANCE)

        if self.add_data_files_metadata is None or self.add_data_files_metadata == "":
            self.add_data_files_metadata = self.config.get("add_data_files_metadata", DEFAULT_ADD_DATA_FILES_METADATA)

        if self.add_runtime_parameters is None or self.add_runtime_parameters == "":
            self.add_runtime_parameters = self.config.get("add_runtime_parameters", DEFAULT_ADD_RUNTIME_PARAMETERS)

        self.runtime_parameters = []
        self.data_files = []

        logging.info(f"Instantiated Manager in '{os.path.abspath(__file__)}'")

    def set_executable(self, executable: str) -> None:
        self.executable = executable

    def set_template_file(self, template_file: str) -> None:
        self.template_file = template_file

    def add_runtime_parameter(
            self,
            key: str,
            value: str,
            name: str,
            desc: str = None
        ) -> None:

        self.runtime_parameters.append(
            {
                "key": key,
                "value": value,
                "name": name,
                "desc": desc,
            }
        )
        logging.info(f"Added runtime parameter '{key}' with value '{value}'")

    def register_data_file(
        self,
        data_file: str,
        name: str = None,
        desc: str = None
        ) -> None:
        if name is None:
            name = os.path.basename(data_file)
        if desc is None:
            desc = "No description provided"
        checksum = calculate_md5(data_file)
        self.data_files.append(
            {
                "name": name,
                "desc": desc,
                "file": data_file,
                "checksum": checksum,

            }
        )
        logging.info(f"Registered data file '{data_file}' with checksum '{checksum}'")

    def generate_report(self, lookup: Dict[str, Any]) -> None:
        if lookup is None:
            logging.warning("the lookup is not defined")

        check_infile_status(self.template_file)

        logging.info(f"Will attempt to generate report using template file '{self.template_file}'")

        template_lookup = {"report_lookup": lookup}

        section_titles = self.config.get("section_titles", None)
        for section_title, value in section_titles.items():
            template_lookup[section_title] = value
            logging.info(f"Added section title '{section_title}' with value '{value}' to the template lookup")

        template_lookup["summary_lines"] = self.config.get("summary_lines", None)
        template_lookup["summary_desc"] = self.config.get("summary_description", None)


        if self.add_provenance:
            template_lookup["provenance"] = {
                "template_file": self.template_file,
                "method_created": os.path.abspath(self.executable),
                "date_created": str(datetime.today().strftime('%Y-%m-%d-%H%M%S')),
                "created_by": os.environ.get('USER'),
                "logfile": os.path.abspath(self.logfile),
            }
            logging.info("Added provenance metadata to lookup")

        if self.add_data_files_metadata:
            template_lookup["data_files"] = self.data_files
            logging.info("Added data files metadata to lookup")

        if self.runtime_parameters:
            template_lookup["runtime_parameters"] = self.runtime_parameters
            logging.info("Added runtime parameters to lookup")

        with open(self.template_file) as fh:
            template = Template(fh.read())

        content = template.render(template_lookup)

        with open(self.outfile, "w") as of:
            of.write(content)

        if self.verbose:
            print(f"Wrote report file '{self.outfile}'")
        logging.info(f"Wrote report file '{self.outfile}'")

