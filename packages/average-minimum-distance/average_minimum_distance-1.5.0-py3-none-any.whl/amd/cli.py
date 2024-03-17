"""Command line interface for :func:`amd.compare() <.compare.compare>`.
"""

import argparse
import sys

from .compare import compare


def main():
    """Entry point for command line interface for
    :func:`amd.compare() <.compare.compare>.
    """

    description = (
        "Compare crystals by AMD or PDD from the command line. Given one or "
        "two paths to cifs/folders, lists of CSD refcodes or periodic sets, "
        "compare them and return a DataFrame of the distance matrix. By "
        "default, uses AMD with k = 100. Accepts most keyword arguments "
        "accepted by amd's CIF/CSD readers and comparison functions."
    )

    parser = argparse.ArgumentParser(description=description)

    parser.add_argument(
        'paths', type=str, nargs='+',
        help='(str) One or two paths to CIF files or folders.'
    )
    parser.add_argument(
        '--outpath', '-o', type=str,
        help='(str) Path of the output file.'
    )
    parser.add_argument(
        '--format', '-f', type=str, default='csv',
        help='(str) Format of the output file, default csv.'
    )

    # amd.compare args
    parser.add_argument(
        '--by', '-b', type=str, default='AMD', choices=['AMD', 'PDD'],
        help='(str) Use AMD or PDD to compare crystals.'
    )
    parser.add_argument(
        '--k', '-k', type=int, default=100,
        help='(int) Number of neighbor atoms to use for AMD/PDD.'
    )
    parser.add_argument(
        '--nearest', '-n', type=int, default=None,
        help='(int) Find n nearest neighbors instead of a full distance '
             'matrix between crystals.'
    )

    # Reading args
    parser.add_argument(
        '--supress_warnings', default=False, action='store_true',
        help='(flag) Do not show warnings encountered during reading.'
    )
    parser.add_argument(
        '--reader', '-r', type=str, default='gemmi',
        choices=['gemmi', 'pymatgen', 'ase', 'pycodcif', 'ccdc'],
        help='(str) Backend package used to parse files, default gemmi.'
    )
    parser.add_argument(
        '--remove_hydrogens', default=False, action='store_true',
        help='(flag) Remove Hydrogen atoms.'
    )
    parser.add_argument(
        '--disorder', type=str, default='skip',
        choices=['skip', 'ordered_sites', 'all_sites'],
        help='(str) Control how disordered structures are handled.'
    )
    parser.add_argument(
        '--heaviest_component', default=False, action='store_true',
        help='(flag) (csd-python-api only) Keep only the heaviest part of the '
             'asymmetric unit, intended for removing solvents.'
    )
    parser.add_argument(
        '--molecular_centres', default=False, action='store_true',
        help='(flag) (csd-python-api only) Uses the centres of molecules for '
             'comparisons instead of atoms.'
    )
    parser.add_argument(
        '--csd_refcodes', default=False, action='store_true',
        help='(flag) (csd-python-api only) Interpret paths as CSD refcodes.'
             'refcode families.'
    )
    parser.add_argument(
        '--refcode_families', default=False, action='store_true',
        help='(flag) (csd-python-api only) Interpret paths as CSD refcode '
             'families.'
    )

    # PDD args
    parser.add_argument(
        '--collapse_tol', type=float, default=1e-4,
        help='(float) Tolerance for collapsing rows of PDDs.'
    )

    # compare args
    parser.add_argument(
        '--metric', type=str, default='chebyshev',
        help='(str) Metric used to compare AMDs/rows of PDDs, default '
             'chebyshev.'
    )
    parser.add_argument(
        '--n_jobs', type=int, default=1,
        help='(int) Number of cores to use for multiprocessing when comparing '
             'PDDs.'
    )
    parser.add_argument(
        '--backend', type=str, default='multiprocessing',
        help='(str) The parallelization backend implementation for PDD '
             'comparisons.'
    )
    parser.add_argument(
        '--verbose', default=False, action='store_true',
        help='(int) Print an ETA to the terminal when comparing PDDs. Passed '
             'to joblib.Parallel if using multiprocessing.'
    )
    parser.add_argument(
        '--low_memory', default=False, action='store_true',
        help='(flag) Use a slower but more memory efficient method for AMD '
             'comparisons.'
    )

    # Remove some arguments before passing others to amd.compare
    kwargs = vars(parser.parse_args())
    paths = kwargs.pop('paths')
    outpath = kwargs.pop('outpath', None)
    if outpath is None:
        outpath = f"{kwargs['by']}_k={kwargs['k']}_dist_matrix"
    ext = kwargs.pop('format', 'csv')

    # Parameter is show_warnings, here it's a flag supress_warnings
    kwargs['show_warnings'] = not kwargs['supress_warnings']
    kwargs.pop('supress_warnings', None)

    crystals = paths[0]
    crystals_ = None
    if len(paths) == 2:
        crystals_ = paths[1]
    elif len(paths) > 2:
        raise ValueError(
            'amd.compare accepts one or two collections of crystals for '
            'comparison.'
        )

    df = compare(crystals, crystals_, **kwargs)

    if kwargs['verbose']:
        sys.stdout.write(str(df))

    if not outpath.endswith('.' + ext):
        outpath += '.' + ext

    try:
        output_func = getattr(df, 'to_' + ext)
        output_func(outpath)
    except AttributeError:
        raise ValueError(f'Unknown format {ext}.')
