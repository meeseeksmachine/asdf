"""
Implementation of command for converting ASDF-in-FITS to standalone ASDF file.
"""

import asdf
from asdf.fits_embed import AsdfInFits

from .main import Command

__all__ = ["extract_file"]


class AsdfExtractor(Command):  # pragma: no cover
    """This class is the plugin implementation for the asdftool runner."""

    @classmethod
    def setup_arguments(cls, subparsers):
        parser = subparsers.add_parser(
            "extract",
            help="Extract ASDF extensions in ASDF-in-FITS files into pure ASDF files",
            description="Extracts ASDF extensions into pure ASDF files.",
        )

        parser.add_argument(
            "infile",
            action="store",
            type=str,
            help="Name of ASDF-in-FITS file containing extension to be extracted",
        )
        parser.add_argument(
            "outfile",
            action="store",
            type=str,
            help="Name of new pure ASDF file containing extracted extension",
        )

        parser.set_defaults(func=cls.run)

        return parser

    @classmethod
    def run(cls, args):
        return extract_file(args.infile, args.outfile)


def extract_file(input_file, output_file):
    """Function for performing extraction from ASDF-in-FITS to pure ASDF."""

    try:
        with asdf.open(input_file) as ih:
            if not isinstance(ih, AsdfInFits):
                msg = f"Given input file '{input_file}' is not ASDF-in-FITS"
                raise RuntimeError(msg)  # noqa: TRY004

            with asdf.AsdfFile(ih.tree) as oh:
                oh.write_to(output_file)

    except (OSError, ValueError) as err:
        raise RuntimeError(str(err)) from err
