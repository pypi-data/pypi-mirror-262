"""
Functions for generating code badges
"""

__all__ = [
    "print_pylint_badge",
    "WITH_PYLINT",
]

import pkgutil
from collections import OrderedDict
import sys
from .raiseif import raiseif
from .setuptools import get_kwargs
from . import __path__

try:
    from pylint.lint import Run
    from lyncs_utils import redirect_stdout

    WITH_PYLINT = True
except ModuleNotFoundError:
    WITH_PYLINT = False

try:
    import enchant

    WITH_ENCHANT = True
except ImportError as err:
    WITH_ENCHANT = False
    WITH_ENCHANT_ERROR = err

mark = raiseif(
    not WITH_PYLINT, ImportError("Please install `lyncs_setuptools[pylint]`")
)


@mark
def run_pylint(do_exit=True, spelling=WITH_ENCHANT):
    "Runs the pylint executable with some additional options"

    if "." in sys.argv:
        sys.argv.remove(".")
        pkgs = []
        for pkg in get_kwargs()["packages"]:
            if pkg.split(".")[0] not in pkgs:
                pkgs.append(pkg)
        sys.argv += pkgs

    if spelling and not WITH_ENCHANT:
        raise WITH_ENCHANT_ERROR

    if spelling and "spelling" not in sys.argv and enchant.dict_exists("en"):
        sys.argv += [
            "--enable",
            "spelling",
            "--spelling-dict",
            "en",
            "--spelling-ignore-words",
            ",".join(ignore_words),
        ]

    return Run(sys.argv[1:], exit=do_exit)


@mark
def print_pylint_badge(do_exit=True, **kwargs):
    "Runs the pylint executable and prints the badge with the score"

    with redirect_stdout(sys.stderr):
        results = run_pylint(do_exit=False, **kwargs)

    score = results.linter.stats.global_note
    colors = OrderedDict(
        {
            9.95: "brightgreen",
            8.95: "green",
            7.95: "yellowgreen",
            6.95: "yellow",
            5.95: "orange",
            0.00: "red",
        }
    )

    color = "brightgreen"
    for val, color in colors.items():
        if score >= val:
            break

    print(
        f"[![pylint](https://img.shields.io/badge/pylint%20score-{score:.1f}%2F10-{color}?logo=python&logoColor=white)](http://pylint.pycqa.org/)"
    )

    if not do_exit:
        return
    if results.linter.config.exit_zero:
        sys.exit(0)
    if score > results.linter.config.fail_under:
        sys.exit(0)
    sys.exit(results.linter.msg_status)


ignore_words = sorted(
    [
        "anymore",
        "API",
        "arg",
        "args",
        "argv",
        "bool",
        "cartesian",
        "cls",
        "color",
        "config",
        "coord",
        "coords",
        "cwd",
        "dict",
        "dofs",
        "dtype",
        "etc",
        "filename",
        "func",
        "i",
        "idxs",
        "int",
        "iterable",
        "itertools",
        "Iwasaki",
        "j",
        "kwargs",
        "lyncs",
        "metaclass",
        "mpi",
        "mpirun",
        "namespace",
        "openmp",
        "parallelize",
        "params",
        "plaquette",
        "procs",
        "QCD",
        "rhs",
        "Schwinger",
        "spinor",
        "stdout",
        "str",
        "Symanzik",
        "sys",
        "TBA",
        "TBD",
        "tuple",
        "url",
        "utils",
        "vals",
        "varnames",
    ]
    + list(
        set(
            part
            for mod in pkgutil.iter_modules(None)
            for part in mod.name.replace("-", "_").split("_")
        ).difference([""])
    )
)
