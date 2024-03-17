"""Tools for reading crystals from files, or from the CSD with
``csd-python-api``. The readers return
:class:`amd.PeriodicSet <.periodicset.PeriodicSet>` objects representing
the crystal which can be passed to :func:`amd.AMD() <.calculate.AMD>`
and :func:`amd.PDD() <.calculate.PDD>`.
"""

import warnings
import collections
import os
import re
import functools
import errno
import math
import json
from pathlib import Path
from typing import (
    Iterable,
    Iterator,
    Optional,
    Union,
    Callable,
    Tuple,
    List
)

import numpy as np
import numpy.typing as npt
import numba
import tqdm

from .utils import cellpar_to_cell
from .periodicset import PeriodicSet

__all__ = [
    'CifReader',
    'CSDReader',
    'ParseError',
    'periodicset_from_gemmi_block',
    'periodicset_from_ase_cifblock',
    'periodicset_from_pymatgen_cifblock',
    'periodicset_from_ase_atoms',
    'periodicset_from_pymatgen_structure',
    'periodicset_from_ccdc_entry',
    'periodicset_from_ccdc_crystal',
]

FloatArray = npt.NDArray[np.floating]
IntArray = npt.NDArray[np.integer]

def _custom_warning(message, category, filename, lineno, *args, **kwargs):
    return f'{category.__name__}: {message}\n'

warnings.formatwarning = _custom_warning

with open(str(Path(__file__).absolute().parent / 'atomic_numbers.json')) as f:
    _ATOMIC_NUMBERS = json.load(f)

_EQ_SITE_TOL: float = 1e-3
_CIF_TAGS: dict = {
    'cellpar': [
        '_cell_length_a',
        '_cell_length_b',
        '_cell_length_c',
        '_cell_angle_alpha',
        '_cell_angle_beta',
        '_cell_angle_gamma'
    ],
    'atom_site_fract': [
        '_atom_site_fract_x',
        '_atom_site_fract_y',
        '_atom_site_fract_z'
    ],
    'atom_site_cartn': [
        '_atom_site_Cartn_x',
        '_atom_site_Cartn_y',
        '_atom_site_Cartn_z'
    ],
    'symop': [
        '_space_group_symop_operation_xyz',
        '_space_group_symop.operation_xyz',
        '_symmetry_equiv_pos_as_xyz'
    ],
    'spacegroup_name': [
        '_space_group_name_H-M_alt',
        '_symmetry_space_group_name_H-M'
    ],
    'spacegroup_number': [
        '_space_group_IT_number',
        '_symmetry_Int_Tables_number'
    ],
}

__all__ = [
    'CifReader',
    'CSDReader',
    'ParseError',
    'periodicset_from_gemmi_block',
    'periodicset_from_ase_cifblock',
    'periodicset_from_pymatgen_cifblock',
    'periodicset_from_ase_atoms',
    'periodicset_from_pymatgen_structure',
    'periodicset_from_ccdc_entry',
    'periodicset_from_ccdc_crystal',
]

class _Reader(collections.abc.Iterator):
    """Base reader class."""

    def __init__(
            self,
            iterable: Iterable,
            converter: Callable[..., PeriodicSet],
            show_warnings: bool,
            verbose: bool
    ):

        self._iterator = iter(iterable)
        self._converter = converter
        self.show_warnings = show_warnings
        if verbose:
            self._progress_bar = tqdm.tqdm(desc='Reading', delay=1)
        else:
            self._progress_bar = None

    def __next__(self):
        """Iterate over self._iterator, passing items through
        self._converter and yielding. If
        :class:`ParseError <.io.ParseError>` is raised in a call to
        self._converter, the item is skipped. Warnings raised in
        self._converter are printed if self.show_warnings is True.
        """

        if not self.show_warnings:
            warnings.simplefilter('ignore')

        while True:

            try:
                item = next(self._iterator)
            except StopIteration:
                if self._progress_bar is not None:
                    self._progress_bar.close()
                raise StopIteration

            with warnings.catch_warnings(record=True) as warning_msgs:
                try:
                    periodic_set = self._converter(item)
                except ParseError as err:
                    warnings.warn(str(err))
                    continue
                finally:
                    if self._progress_bar is not None:
                        self._progress_bar.update(1)

            for warning in warning_msgs:
                msg = f'(name={periodic_set.name}) {warning.message}'
                warnings.warn(msg, category=warning.category)

            return periodic_set

    def read(self) -> Union[PeriodicSet, List[PeriodicSet]]:
        """Read the crystal(s), return one
        :class:`amd.PeriodicSet <.periodicset.PeriodicSet>` if there is
        only one, otherwise return a list.
        """
        items = list(self)
        if len(items) == 1:
            return items[0]
        return items


class CifReader(_Reader):
    """Read all structures in a .cif file or all files in a folder
    with ase or csd-python-api (if installed), yielding
    :class:`amd.PeriodicSet <.periodicset.PeriodicSet>` s.

    Parameters
    ----------
    path : str
        Path to a .CIF file or directory. (Other files are accepted when
        using ``reader='ccdc'``, if csd-python-api is installed.)
    reader : str, optional
        The backend package used to parse the CIF. The default is
        :code:`gemmi`, :code:`pymatgen` and :code:`ase` are also
        accepted, as well as :code:`ccdc` if csd-python-api is
        installed. The ccdc reader should be able to read any format
        accepted by :class:`ccdc.io.EntryReader`, though only CIFs have
        been tested.
    remove_hydrogens : bool, optional
        Remove Hydrogens from the crystals.
    disorder : str, optional
        Controls how disordered structures are handled. Default is
        ``skip`` which skips any crystal with disorder, since disorder
        conflicts with the periodic set model. To read disordered
        structures anyway, choose either :code:`ordered_sites` to remove
        atoms with disorder or :code:`all_sites` include all atoms
        regardless of disorder.
    heaviest_component : bool, optional
        csd-python-api only. Removes all but the heaviest molecule in
        the asymmeric unit, intended for removing solvents.
    molecular_centres : bool, default False
        csd-python-api only. Extract the centres of molecules in the
        unit cell and store in the attribute molecular_centres.
    show_warnings : bool, optional
        Controls whether warnings that arise during reading are printed.
    verbose : bool, default False
        If True, prints a progress bar showing the number of items
        processed.

    Yields
    ------
    :class:`amd.PeriodicSet <.periodicset.PeriodicSet>`
        Represents the crystal as a periodic set, consisting of a finite
        set of points (motif) and lattice (unit cell). Contains other
        data, e.g. the crystal's name and information about the
        asymmetric unit.

    Examples
    --------

        ::

            # Put all crystals in a .CIF in a list
            structures = list(amd.CifReader('mycif.cif'))

            # Can also accept path to a directory, reading all files inside
            structures = list(amd.CifReader('path/to/folder'))

            # Reads just one if the .CIF has just one crystal
            periodic_set = amd.CifReader('mycif.cif').read()

            # List of AMDs (k=100) of crystals in a .CIF
            amds = [amd.AMD(item, 100) for item in amd.CifReader('mycif.cif')]
    """

    def __init__(
            self,
            path: Union[str, os.PathLike],
            reader: str = 'gemmi',
            remove_hydrogens: bool = False,
            disorder: str = 'skip',
            heaviest_component: bool = False,
            molecular_centres: bool = False,
            show_warnings: bool = True,
            verbose: bool = False
    ):

        if disorder not in ('skip', 'ordered_sites', 'all_sites'):
            raise ValueError(
                f"'disorder'' parameter of {self.__class__.__name__} must be "
                f"one of 'skip', 'ordered_sites' or 'all_sites' (passed "
                f"'{disorder}')"
            )

        if reader != 'ccdc':
            if heaviest_component:
                raise NotImplementedError(
                    "'heaviest_component' parameter of "
                    f"{self.__class__.__name__} only implemented with "
                    "csd-python-api, if installed pass reader='ccdc'"
                )
            if molecular_centres:
                raise NotImplementedError(
                    "'molecular_centres' parameter of "
                    f"{self.__class__.__name__} only implemented with "
                    "csd-python-api, if installed pass reader='ccdc'"
                )

        # cannot handle some characters (�) in cifs
        if reader == 'gemmi':
            import gemmi
            extensions = {'cif'}
            file_parser = gemmi.cif.read_file
            converter = functools.partial(
                periodicset_from_gemmi_block,
                remove_hydrogens=remove_hydrogens,
                disorder=disorder
            )

        elif reader in ('ase', 'pycodcif'):
            from ase.io.cif import parse_cif
            extensions = {'cif'}
            file_parser = functools.partial(parse_cif, reader=reader)
            converter = functools.partial(
                periodicset_from_ase_cifblock,
                remove_hydrogens=remove_hydrogens,
                disorder=disorder
            )

        elif reader == 'pymatgen':

            def _pymatgen_cif_parser(path):
                from pymatgen.io.cif import CifFile
                return CifFile.from_file(path).data.values()

            extensions = {'cif'}
            file_parser = _pymatgen_cif_parser
            converter = functools.partial(
                periodicset_from_pymatgen_cifblock,
                remove_hydrogens=remove_hydrogens,
                disorder=disorder
            )

        elif reader == 'ccdc':
            try:
                import ccdc.io
            except (ImportError, RuntimeError) as e:
                raise ImportError('Failed to import csd-python-api') from e

            extensions = set(ccdc.io.EntryReader.known_suffixes.keys())
            file_parser = ccdc.io.EntryReader
            converter = functools.partial(
                periodicset_from_ccdc_entry,
                remove_hydrogens=remove_hydrogens,
                disorder=disorder,
                molecular_centres=molecular_centres,
                heaviest_component=heaviest_component
            )

        else:
            raise ValueError(
                f"'reader' parameter of {self.__class__.__name__} must be one "
                f"of 'gemmi', 'pymatgen', 'ccdc', 'ase', or 'pycodcif' "
                f"(passed '{reader}')"
            )

        path = Path(path)
        if path.is_file():
            iterable = file_parser(str(path))
        elif path.is_dir():
            iterable = CifReader._dir_generator(path, file_parser, extensions)
        else:
            raise FileNotFoundError(
                errno.ENOENT, os.strerror(errno.ENOENT), str(path)
            )

        super().__init__(iterable, converter, show_warnings, verbose)

    @staticmethod
    def _dir_generator(
            path: Path, file_parser: Callable, extensions: Iterable
    ) -> Iterator:
        """Generate items from all files with extensions in
        ``extensions`` from a directory ``path``."""
        for file_path in path.iterdir():
            if not file_path.is_file():
                continue
            if file_path.suffix[1:].lower() not in extensions:
                continue
            try:
                yield from file_parser(str(file_path))
            except Exception as e:
                warnings.warn(
                    f'Error parsing "{str(file_path)}", skipping file. '
                    f'Exception: {repr(e)}'
                )


class CSDReader(_Reader):
    """Read structures from the CSD with csd-python-api, yielding
    :class:`amd.PeriodicSet <.periodicset.PeriodicSet>` s.

    Parameters
    ----------
    refcodes : str or List[str], optional
        Single or list of CSD refcodes to read. If None or 'CSD',
        iterates over the whole CSD.
    refcode_families : bool, optional
        Interpret ``refcodes`` as one or more refcode families, reading
        all entries whose refcode starts with the given strings.
    remove_hydrogens : bool, optional
        Remove hydrogens from the crystals.
    disorder : str, optional
        Controls how disordered structures are handled. Default is
        ``skip`` which skips any crystal with disorder, since disorder
        conflicts with the periodic set model. To read disordered
        structures anyway, choose either :code:`ordered_sites` to remove
        atoms with disorder or :code:`all_sites` include all atoms
        regardless of disorder.
    heaviest_component : bool, optional
        Removes all but the heaviest molecule in the asymmeric unit,
        intended for removing solvents.
    molecular_centres : bool, default False
        Extract the centres of molecules in the unit cell and store in
        attribute molecular_centres.
    show_warnings : bool, optional
        Controls whether warnings that arise during reading are printed.
    verbose : bool, default False
        If True, prints a progress bar showing the number of items
        processed.

    Yields
    ------
    :class:`amd.PeriodicSet <.periodicset.PeriodicSet>`
        Represents the crystal as a periodic set, consisting of a finite
        set of points (motif) and lattice (unit cell). Contains other
        useful data, e.g. the crystal's name and information about the
        asymmetric unit for calculation.

    Examples
    --------

        ::

            # Put these entries in a list
            refcodes = ['DEBXIT01', 'DEBXIT05', 'HXACAN01']
            structures = list(amd.CSDReader(refcodes))

            # Read refcode families (any whose refcode starts with strings in the list)
            families = ['ACSALA', 'HXACAN']
            structures = list(amd.CSDReader(families, refcode_families=True))

            # Get AMDs (k=100) for crystals in these families
            refcodes = ['ACSALA', 'HXACAN']
            amds = []
            for periodic_set in amd.CSDReader(refcodes, refcode_families=True):
                amds.append(amd.AMD(periodic_set, 100))

            # Giving the reader nothing reads from the whole CSD.
            for periodic_set in amd.CSDReader():
                ...
    """

    def __init__(
            self,
            refcodes: Optional[Union[str, List[str]]] = None,
            refcode_families: bool = False,
            remove_hydrogens: bool = False,
            disorder: str = 'skip',
            heaviest_component: bool = False,
            molecular_centres: bool = False,
            show_warnings: bool = True,
            verbose: bool = False
    ):

        if disorder not in ('skip', 'ordered_sites', 'all_sites'):
            raise ValueError(
                f"'disorder'' parameter of {self.__class__.__name__} must be "
                f"one of 'skip', 'ordered_sites' or 'all_sites' (passed "
                f"'{disorder}')"
            )

        try:
            import ccdc.search
            import ccdc.io
        except (ImportError, RuntimeError) as e:
            raise ImportError('Failed to import csd-python-api') from e

        if isinstance(refcodes, str) and refcodes.lower() == 'csd':
            refcodes = None
        if refcodes is None:
            refcode_families = False
        elif isinstance(refcodes, str):
            refcodes = [refcodes]
        elif isinstance(refcodes, list):
            if not all(isinstance(refcode, str) for refcode in refcodes):
                raise ValueError(
                    f'{self.__class__.__name__} expects None, a string or '
                    'list of strings.'
                )
        else:
            raise ValueError(
                f'{self.__class__.__name__} expects None, a string or list of '
                f'strings, got {refcodes.__class__.__name__}'
            )

        if refcode_families:
            all_refcodes = []
            for refcode in refcodes:
                query = ccdc.search.TextNumericSearch()
                query.add_identifier(refcode)
                hits = [hit.identifier for hit in query.search()]
                all_refcodes.extend(hits)
            # filter to unique refcodes while keeping order
            refcodes = []
            seen = set()
            for refcode in all_refcodes:
                if refcode not in seen:
                    refcodes.append(refcode)
                    seen.add(refcode)

        converter = functools.partial(
            periodicset_from_ccdc_entry,
            remove_hydrogens=remove_hydrogens,
            disorder=disorder,
            molecular_centres=molecular_centres,
            heaviest_component=heaviest_component
        )

        entry_reader = ccdc.io.EntryReader('CSD')
        if refcodes is None:
            iterable = entry_reader
        else:
            iterable = map(entry_reader.entry, refcodes)

        super().__init__(iterable, converter, show_warnings, verbose)


class ParseError(ValueError):
    """Raised when an item cannot be parsed into a periodic set."""
    pass


def periodicset_from_gemmi_block(
        block, remove_hydrogens: bool = False, disorder: str = 'skip'
) -> PeriodicSet:
    """Convert a :class:`gemmi.cif.Block` object to a
    :class:`amd.PeriodicSet <.periodicset.PeriodicSet>`.
    :class:`gemmi.cif.Block` is the type returned by
    :func:`gemmi.cif.read_file`.

    Parameters
    ----------
    block : :class:`gemmi.cif.Block`
        An ase CIFBlock object representing a crystal.
    remove_hydrogens : bool, optional
        Remove Hydrogens from the crystal.
    disorder : str, optional
        Controls how disordered structures are handled. Default is
        ``skip`` which skips any crystal with disorder, since disorder
        conflicts with the periodic set model. To read disordered
        structures anyway, choose either :code:`ordered_sites` to remove
        atoms with disorder or :code:`all_sites` include all atoms
        regardless of disorder.

    Returns
    -------
    :class:`amd.PeriodicSet <.periodicset.PeriodicSet>`
        Represents the crystal as a periodic set, consisting of a finite
        set of points (motif) and lattice (unit cell). Contains other
        useful data, e.g. the crystal's name and information about the
        asymmetric unit for calculation.

    Raises
    ------
    ParseError
        Raised if the structure fails to be parsed for any of the
        following: 1. Required data is missing (e.g. cell parameters),
        2. :code:``disorder == 'skip'`` and disorder is found on any
        atom, 3. The motif is empty after removing H or disordered
        sites.
    """

    import gemmi

    # Unit cell
    cellpar = [block.find_value(t) for t in _CIF_TAGS['cellpar']]
    if not all(isinstance(par, str) for par in cellpar):
        raise ParseError(f'{block.name} has missing cell data')
    cellpar = np.array([str2float(par) for par in cellpar])
    if np.isnan(np.sum(cellpar)):
        raise ParseError(f'{block.name} has missing cell data')
    cell = cellpar_to_cell(cellpar)

    # Asymmetric unit coordinates
    xyz_loop = block.find(_CIF_TAGS['atom_site_fract']).loop
    if xyz_loop is None:
        xyz_loop = block.find(_CIF_TAGS['atom_site_cartn']).loop
        if xyz_loop is None:
            raise ParseError(f'{block.name} has missing coordinate data')
        else:
            raise ParseError(
                f'{block.name} uses _atom_site_Cartn_ tags for coordinates, '
                'only _atom_site_fract_ is supported'
            )

    tablified_loop = [[] for _ in range(len(xyz_loop.tags))]
    for i, item in enumerate(xyz_loop.values):
        tablified_loop[i % xyz_loop.width()].append(item)
    loop_dict = {tag: l for tag, l in zip(xyz_loop.tags, tablified_loop)}
    xyz_str = [loop_dict[t] for t in _CIF_TAGS['atom_site_fract']]
    asym_unit = np.transpose(np.array(
        [[str2float(c) for c in xyz] for xyz in xyz_str]
    ))
    asym_unit = np.mod(asym_unit, 1)

    # recommended by pymatgen
    # asym_unit = _snap_small_prec_coords(asym_unit, 1e-4) 

    # Labels
    if '_atom_site_label' in loop_dict:
        labels = [
            gemmi.cif.as_string(lab) for lab in loop_dict['_atom_site_label']
        ]
    else:
        labels = [''] * xyz_loop.length()

    # Atomic types
    if '_atom_site_type_symbol' in loop_dict:
        symbols = []
        for s in loop_dict['_atom_site_type_symbol']:
            sym = gemmi.cif.as_string(s)
            match = re.search(r'([A-Za-z][A-Za-z]?)', sym)
            if match is not None:
                sym = match.group()
            else:
                sym = ''
            sym = list(sym)
            if len(sym) > 0:
                sym[0] = sym[0].upper()
            if len(sym) > 1:
                sym[1] = sym[1].lower()
            symbols.append(''.join(sym))
    else:  # Get atomic types from label
        symbols = _atomic_symbols_from_labels(labels)

    asym_types = []
    for s in symbols:
        if s in _ATOMIC_NUMBERS:
            asym_types.append(_ATOMIC_NUMBERS[s])
        else:
            asym_types.append(0)

    # Occupancies
    if '_atom_site_occupancy' in loop_dict:
        occs = [
            str2float(oc) for oc in loop_dict['_atom_site_occupancy']
        ]
        occupancies = [occ if not math.isnan(occ) else 1 for occ in occs]
    else:
        occupancies = [1] * xyz_loop.length()

    # Remove sites with missing coordinates, disorder and Hydrogens if needed
    remove_sites = []
    remove_sites.extend(np.nonzero(np.isnan(asym_unit.min(axis=-1)))[0])

    if disorder == 'skip':
        if any(_has_disorder(l, o) for l, o in zip(labels, occupancies)):
            raise ParseError(
                f"{block.name} has disorder, pass disorder='ordered_sites' or "
                "'all_sites' to remove/ignore disorder"
            )
    elif disorder == 'ordered_sites':
        for i, (label, occ) in enumerate(zip(labels, occupancies)):
            if _has_disorder(label, occ):
                remove_sites.append(i)

    if remove_hydrogens:
        remove_sites.extend(i for i, num in enumerate(asym_types) if num == 1)

    asym_unit = np.delete(asym_unit, remove_sites, axis=0)
    asym_types = [s for i, s in enumerate(asym_types) if i not in remove_sites]
    if asym_unit.shape[0] == 0:
        raise ParseError(f'{block.name} has no valid sites')

    if disorder != 'all_sites':
        keep_sites = _unique_sites(asym_unit, _EQ_SITE_TOL)
        if not np.all(keep_sites):
            warnings.warn(
                'may have overlapping sites; duplicates will be removed'
            )
        asym_unit = asym_unit[keep_sites]
        asym_types = [sym for sym, keep in zip(asym_types, keep_sites) if keep]

    # Symmetry operations, try xyz strings first
    for tag in _CIF_TAGS['symop']:
        sitesym = [v.str(0) for v in block.find([tag])]
        if sitesym:
            rot, trans = _parse_sitesyms(sitesym)
            break
    else:
        # Try spacegroup name; can be a pair or in a loop
        spg = None
        for tag in _CIF_TAGS['spacegroup_name']:
            for value in block.find([tag]):
                try:
                    # Some names cannot be parsed by gemmi.SpaceGroup
                    spg = gemmi.SpaceGroup(value.str(0))
                    break
                except ValueError:
                    continue
            if spg is not None:
                break

        if spg is None:
            # Try international number
            for tag in _CIF_TAGS['spacegroup_number']:
                spg_num = block.find_value(tag)
                if spg_num is not None:
                    spg_num = gemmi.cif.as_int(spg_num)
                    break
            else:
                warnings.warn('no symmetry data found, defaulting to P1')
                spg_num = 1
            spg = gemmi.SpaceGroup(spg_num)

        rot = np.array([np.array(o.rot) / o.DEN for o in spg.operations()])
        trans = np.array([np.array(o.tran) / o.DEN for o in spg.operations()])

    frac_motif, invs = _expand_asym_unit(asym_unit, rot, trans, _EQ_SITE_TOL)
    _, wyc_muls = np.unique(invs, return_counts=True)
    asym_inds = np.zeros_like(wyc_muls, dtype=np.int32)
    asym_inds[1:] = np.cumsum(wyc_muls)[:-1]
    types = np.array([asym_types[i] for i in invs], dtype=np.uint8)
    motif = np.matmul(frac_motif, cell)

    return PeriodicSet(
        motif=motif,
        cell=cell,
        name=block.name,
        asym_unit=asym_inds,
        multiplicities=wyc_muls,
        types=types
    )


def periodicset_from_ase_cifblock(
        block, remove_hydrogens: bool = False, disorder: str = 'skip'
) -> PeriodicSet:
    """Convert a :class:`ase.io.cif.CIFBlock` object to a 
    :class:`amd.PeriodicSet <.periodicset.PeriodicSet>`.
    :class:`ase.io.cif.CIFBlock` is the type returned by
    :func:`ase.io.cif.parse_cif`.

    Parameters
    ----------
    block : :class:`ase.io.cif.CIFBlock`
        An ase :class:`ase.io.cif.CIFBlock` object representing a
        crystal.
    remove_hydrogens : bool, optional
        Remove Hydrogens from the crystal.
    disorder : str, optional
        Controls how disordered structures are handled. Default is
        ``skip`` which skips any crystal with disorder, since disorder
        conflicts with the periodic set model. To read disordered
        structures anyway, choose either :code:`ordered_sites` to remove
        atoms with disorder or :code:`all_sites` include all atoms
        regardless of disorder.

    Returns
    -------
    :class:`amd.PeriodicSet <.periodicset.PeriodicSet>`
        Represents the crystal as a periodic set, consisting of a finite
        set of points (motif) and lattice (unit cell). Contains other
        useful data, e.g. the crystal's name and information about the
        asymmetric unit for calculation.

    Raises
    ------
    ParseError
        Raised if the structure fails to be parsed for any of the
        following: 1. Required data is missing (e.g. cell parameters),
        2. The motif is empty after removing H or disordered sites,
        3. :code:``disorder == 'skip'`` and disorder is found on any
        atom.
    """

    import ase
    import ase.spacegroup

    # Unit cell
    cellpar = [str2float(str(block.get(tag))) for tag in _CIF_TAGS['cellpar']]
    if None in cellpar:
        raise ParseError(f'{block.name} has missing cell data')
    cell = cellpar_to_cell(np.array(cellpar))

    # Asymmetric unit coordinates. ase removes uncertainty brackets
    asym_unit = [
        [str2float(str(n)) for n in block.get(tag)]
        for tag in _CIF_TAGS['atom_site_fract']
    ]
    if None in asym_unit:
        asym_unit = [
            block.get(tag.lower()) for tag in _CIF_TAGS['atom_site_cartn']
        ]
        if None in asym_unit:
            raise ParseError(f'{block.name} has missing coordinates')
        else:
            raise ParseError(
                f'{block.name} uses _atom_site_Cartn_ tags for coordinates, '
                'only _atom_site_fract_ is supported'
            )
    asym_unit = list(zip(*asym_unit))

    # Labels
    asym_labels = block.get('_atom_site_label')
    if asym_labels is None:
        asym_labels = [''] * len(asym_unit)

    # Atomic types
    asym_symbols = block.get('_atom_site_type_symbol')
    if asym_symbols is not None:
        asym_symbols_ = _atomic_symbols_from_labels(asym_symbols)
    else:
        asym_symbols_ = [''] * len(asym_unit)

    asym_types = []
    for s in asym_symbols_:
        if s in _ATOMIC_NUMBERS:
            asym_types.append(_ATOMIC_NUMBERS[s])
        else:
            asym_types.append(0)

    # Find where sites have disorder if necassary
    has_disorder = []
    if disorder != 'all_sites':
        occupancies = block.get('_atom_site_occupancy')
        if occupancies is None:
            occupancies = [1] * len(asym_unit)
        for lab, occ in zip(asym_labels, occupancies):
            has_disorder.append(_has_disorder(lab, occ))

    # Remove sites with ?, . or other invalid string for coordinates
    invalid = []
    for i, xyz in enumerate(asym_unit):
        if not all(isinstance(coord, (int, float)) for coord in xyz):
            invalid.append(i)
    if invalid:
        warnings.warn('atoms without sites or missing data will be removed')
        asym_unit = [c for i, c in enumerate(asym_unit) if i not in invalid]
        asym_types = [t for i, t in enumerate(asym_types) if i not in invalid]
        if disorder != 'all_sites':
            has_disorder = [
                d for i, d in enumerate(has_disorder) if i not in invalid
            ]

    remove_sites = []

    if remove_hydrogens:
        remove_sites.extend(i for i, num in enumerate(asym_types) if num == 1)

    # Remove atoms with fractional occupancy or raise ParseError
    if disorder != 'all_sites':
        for i, dis in enumerate(has_disorder):
            if i in remove_sites:
                continue
            if dis:
                if disorder == 'skip':
                    raise ParseError(
                        f'{block.name} has disorder, pass '
                        "disorder='ordered_sites' or 'all_sites' to "
                        'remove/ignore disorder'
                    )
                elif disorder == 'ordered_sites':
                    remove_sites.append(i)

    # Asymmetric unit
    asym_unit = [c for i, c in enumerate(asym_unit) if i not in remove_sites]
    asym_types = [t for i, t in enumerate(asym_types) if i not in remove_sites]
    if len(asym_unit) == 0:
        raise ParseError(f'{block.name} has no valid sites')
    asym_unit = np.mod(np.array(asym_unit), 1)

    # recommended by pymatgen
    # asym_unit = _snap_small_prec_coords(asym_unit, 1e-4)

    # Remove overlapping sites unless disorder == 'all_sites'
    if disorder != 'all_sites':
        keep_sites = _unique_sites(asym_unit, _EQ_SITE_TOL)
        if not np.all(keep_sites):
            warnings.warn(
                'may have overlapping sites, duplicates will be removed'
            )
            asym_unit = asym_unit[keep_sites]
            asym_types = [t for t, keep in zip(asym_types, keep_sites) if keep]

    # Get symmetry operations
    sitesym = block._get_any(_CIF_TAGS['symop'])
    if sitesym is None:
        label_or_num = block._get_any(
            [s.lower() for s in _CIF_TAGS['spacegroup_name']]
        )
        if label_or_num is None:
            label_or_num = block._get_any(
                [s.lower() for s in _CIF_TAGS['spacegroup_number']]
            )
        if label_or_num is None:
            warnings.warn('no symmetry data found, defaulting to P1')
            label_or_num = 1
        spg = ase.spacegroup.Spacegroup(label_or_num)
        rot, trans = spg.get_op()
    else:
        if isinstance(sitesym, str):
            sitesym = [sitesym]
        rot, trans = _parse_sitesyms(sitesym)

    frac_motif, invs = _expand_asym_unit(asym_unit, rot, trans, _EQ_SITE_TOL)
    _, wyc_muls = np.unique(invs, return_counts=True)
    asym_inds = np.zeros_like(wyc_muls, dtype=np.int32)
    asym_inds[1:] = np.cumsum(wyc_muls)[:-1]
    types = np.array([asym_types[i] for i in invs], dtype=np.uint8)
    motif = np.matmul(frac_motif, cell)

    return PeriodicSet(
        motif=motif,
        cell=cell,
        name=block.name,
        asym_unit=asym_inds,
        multiplicities=wyc_muls,
        types=types
    )


def periodicset_from_pymatgen_cifblock(
        block, remove_hydrogens: bool = False, disorder: str = 'skip'
) -> PeriodicSet:
    """Convert a :class:`pymatgen.io.cif.CifBlock` object to a
    :class:`amd.PeriodicSet <.periodicset.PeriodicSet>`.
    :class:`pymatgen.io.cif.CifBlock` is the type returned by
    :class:`pymatgen.io.cif.CifFile`.

    Parameters
    ----------
    block : :class:`pymatgen.io.cif.CifBlock`
        A pymatgen CifBlock object representing a crystal.
    remove_hydrogens : bool, optional
        Remove Hydrogens from the crystal.
    disorder : str, optional
        Controls how disordered structures are handled. Default is
        ``skip`` which skips any crystal with disorder, since disorder
        conflicts with the periodic set model. To read disordered
        structures anyway, choose either :code:`ordered_sites` to remove
        atoms with disorder or :code:`all_sites` include all atoms
        regardless of disorder.

    Returns
    -------
    :class:`amd.PeriodicSet <.periodicset.PeriodicSet>`
        Represents the crystal as a periodic set, consisting of a finite
        set of points (motif) and lattice (unit cell). Contains other
        useful data, e.g. the crystal's name and information about the
        asymmetric unit for calculation.

    Raises
    ------
    ParseError
        Raised if the structure can/should not be parsed for the
        following reasons: 1. No sites found or motif is empty after
        removing Hydrogens & disorder, 2. A site has missing
        coordinates, 3. :code:``disorder == 'skip'`` and disorder is
        found on any atom.
    """

    odict = block.data

    # Unit cell
    cellpar = [odict.get(tag) for tag in _CIF_TAGS['cellpar']]
    if any(par in (None, '?', '.') for par in cellpar):
        raise ParseError(f'{block.header} has missing cell data')

    try:
        cellpar = [str2float(v) for v in cellpar]
    except ValueError:
        raise ParseError(f'{block.header} could not be parsed')
    cell = cellpar_to_cell(
        np.array(cellpar, dtype=np.float64)
    )

    # Asymmetric unit coordinates
    asym_unit = [odict.get(tag) for tag in _CIF_TAGS['atom_site_fract']]
    # check for . and ?
    if None in asym_unit:
        asym_unit = [odict.get(tag) for tag in _CIF_TAGS['atom_site_cartn']]
        if None in asym_unit:
            raise ParseError(f'{block.header} has missing coordinates')
        else:
            raise ParseError(
                f'{block.header} uses _atom_site_Cartn_ tags for coordinates, '
                'only _atom_site_fract_ is supported'
            )
    asym_unit = list(zip(*asym_unit))
    try:
        asym_unit = [[str2float(coord) for coord in xyz] for xyz in asym_unit]
    except ValueError:
        raise ParseError(f'{block.header} could not be parsed')

    # Labels
    asym_labels = odict.get('_atom_site_label')
    if asym_labels is None:
        asym_labels = [''] * len(asym_unit)

    # Atomic types
    asym_symbols = odict.get('_atom_site_type_symbol')
    if asym_symbols is not None:
        asym_symbols_ = _atomic_symbols_from_labels(asym_symbols)
    else:
        asym_symbols_ = [''] * len(asym_unit)
    
    asym_types = []
    for s in asym_symbols_:
        if s in _ATOMIC_NUMBERS:
            asym_types.append(_ATOMIC_NUMBERS[s])
        else:
            asym_types.append(0)

    # Find where sites have disorder if necassary
    has_disorder = []
    if disorder != 'all_sites':
        occupancies = odict.get('_atom_site_occupancy')
        if occupancies is None:
            occupancies = np.ones((len(asym_unit), ))
        else:
            occupancies = np.array([str2float(occ) for occ in occupancies])
        labels = odict.get('_atom_site_label')
        if labels is None:
            labels = [''] * len(asym_unit)
        for lab, occ in zip(labels, occupancies):
            has_disorder.append(_has_disorder(lab, occ))

    # Remove sites with ?, . or other invalid string for coordinates
    invalid = []
    for i, xyz in enumerate(asym_unit):
        if not all(isinstance(coord, (int, float)) for coord in xyz):
            invalid.append(i)

    if invalid:
        warnings.warn('atoms without sites or missing data will be removed')
        asym_unit = [c for i, c in enumerate(asym_unit) if i not in invalid]
        asym_types = [c for i, c in enumerate(asym_types) if i not in invalid]
        if disorder != 'all_sites':
            has_disorder = [
                d for i, d in enumerate(has_disorder) if i not in invalid
            ]

    remove_sites = []

    if remove_hydrogens:
        remove_sites.extend((i for i, n in enumerate(asym_types) if n == 1))

    # Remove atoms with fractional occupancy or raise ParseError
    if disorder != 'all_sites':
        for i, dis in enumerate(has_disorder):
            if i in remove_sites:
                continue
            if dis:
                if disorder == 'skip':
                    raise ParseError(
                        f'{block.header} has disorder, pass '
                        "disorder='ordered_sites' or 'all_sites' to "
                        'remove/ignore disorder'
                    )
                elif disorder == 'ordered_sites':
                    remove_sites.append(i)

    # Asymmetric unit
    asym_unit = [c for i, c in enumerate(asym_unit) if i not in remove_sites]
    asym_types = [t for i, t in enumerate(asym_types) if i not in remove_sites]
    if len(asym_unit) == 0:
        raise ParseError(f'{block.header} has no valid sites')
    asym_unit = np.mod(np.array(asym_unit), 1)

    # recommended by pymatgen
    # asym_unit = _snap_small_prec_coords(asym_unit, 1e-4)

    # Remove overlapping sites unless disorder == 'all_sites'
    if disorder != 'all_sites':
        keep_sites = _unique_sites(asym_unit, _EQ_SITE_TOL)
        if not np.all(keep_sites):
            warnings.warn(
                'may have overlapping sites; duplicates will be removed'
            )
        asym_unit = asym_unit[keep_sites]
        asym_types = [sym for sym, keep in zip(asym_types, keep_sites) if keep]

    # Apply symmetries to asymmetric unit
    rot, trans = _get_syms_pymatgen(odict)
    frac_motif, invs = _expand_asym_unit(asym_unit, rot, trans, _EQ_SITE_TOL)
    _, wyc_muls = np.unique(invs, return_counts=True)
    asym_inds = np.zeros_like(wyc_muls, dtype=np.int32)
    asym_inds[1:] = np.cumsum(wyc_muls)[:-1]
    types = np.array([asym_types[i] for i in invs], dtype=np.uint8)
    motif = np.matmul(frac_motif, cell)

    return PeriodicSet(
        motif=motif,
        cell=cell,
        name=block.header,
        asym_unit=asym_inds,
        multiplicities=wyc_muls,
        types=types
    )


def periodicset_from_ase_atoms(
        atoms, remove_hydrogens: bool = False
) -> PeriodicSet:
    """Convert an :class:`ase.atoms.Atoms` object to a
    :class:`amd.PeriodicSet <.periodicset.PeriodicSet>`. Does not have
    the option to remove disorder.

    Parameters
    ----------
    atoms : :class:`ase.atoms.Atoms`
        An ase :class:`ase.atoms.Atoms` object representing a crystal.
    remove_hydrogens : bool, optional
        Remove Hydrogens from the crystal.

    Returns
    -------
    :class:`amd.PeriodicSet <.periodicset.PeriodicSet>`
        Represents the crystal as a periodic set, consisting of a finite
        set of points (motif) and lattice (unit cell). Contains other
        useful data, e.g. the crystal's name and information about the
        asymmetric unit for calculation.

    Raises
    ------
    ParseError
        Raised if there are no valid sites in atoms.
    """

    from ase.spacegroup import get_basis

    cell = atoms.get_cell().array

    remove_inds = []
    if remove_hydrogens:
        for i in np.where(atoms.get_atomic_numbers() == 1)[0]:
            remove_inds.append(i)
    for i in sorted(remove_inds, reverse=True):
        atoms.pop(i)

    if len(atoms) == 0:
        raise ParseError('ase Atoms object has no valid sites')

    # Symmetry operations from spacegroup
    spg = None
    if 'spacegroup' in atoms.info:
        spg = atoms.info['spacegroup']
        rot, trans = spg.rotations, spg.translations
    else:
        warnings.warn('no symmetry data found, defaulting to P1')
        rot = np.identity(3)[None, :]
        trans = np.zeros((1, 3))

    # Asymmetric unit. ase default tol is 1e-5
    # do differently! get_basis determines a reduced asym unit from the atoms;
    # surely this is not needed!
    asym_unit = get_basis(atoms, spacegroup=spg, tol=_EQ_SITE_TOL)
    frac_motif, invs = _expand_asym_unit(asym_unit, rot, trans, _EQ_SITE_TOL)
    _, wyc_muls = np.unique(invs, return_counts=True)
    asym_inds = np.zeros_like(wyc_muls, dtype=np.int32)
    asym_inds[1:] = np.cumsum(wyc_muls)[:-1]
    types = atoms.get_atomic_numbers().astype(np.uint8)
    motif = np.matmul(frac_motif, cell)

    return PeriodicSet(
        motif=motif,
        cell=cell,
        asym_unit=asym_inds,
        multiplicities=wyc_muls,
        types=types
    )


def periodicset_from_pymatgen_structure(
        structure, remove_hydrogens: bool = False, disorder: str = 'skip'
) -> PeriodicSet:
    """Convert a :class:`pymatgen.core.structure.Structure` object to a
    :class:`amd.PeriodicSet <.periodicset.PeriodicSet>`. Does not set
    the name of the periodic set, as pymatgen Structure objects seem to
    have no name attribute.

    Parameters
    ----------
    structure : :class:`pymatgen.core.structure.Structure`
        A pymatgen Structure object representing a crystal.
    remove_hydrogens : bool, optional
        Remove Hydrogens from the crystal.
    disorder : str, optional
        Controls how disordered structures are handled. Default is
        ``skip`` which skips any crystal with disorder, since disorder
        conflicts with the periodic set model. To read disordered
        structures anyway, choose either :code:`ordered_sites` to remove
        atoms with disorder or :code:`all_sites` include all atoms
        regardless of disorder.

    Returns
    -------
    :class:`amd.PeriodicSet <.periodicset.PeriodicSet>`
        Represents the crystal as a periodic set, consisting of a finite
        set of points (motif) and lattice (unit cell). Contains other
        useful data, e.g. the crystal's name and information about the
        asymmetric unit for calculation.

    Raises
    ------
    ParseError
        Raised if the :code:`disorder == 'skip'` and
        :code:`not structure.is_ordered`
    """

    from pymatgen.symmetry.analyzer import SpacegroupAnalyzer

    if remove_hydrogens:
        structure.remove_species(['H', 'D'])

    # Disorder
    if disorder == 'skip':
        if not structure.is_ordered:
            raise ParseError(
                'pymatgen Structure has disorder, pass '
                "disorder='ordered_sites' or 'all_sites' to remove/ignore "
                'disorder'
            )
    elif disorder == 'ordered_sites':
        remove_inds = []
        for i, comp in enumerate(structure.species_and_occu):
            if comp.num_atoms < 1:
                remove_inds.append(i)
        structure.remove_sites(remove_inds)

    spg = SpacegroupAnalyzer(structure)
    # sym_struct = spg.get_symmetrized_structure()

    # asym_inds = np.array([inds[0] for inds in sym_struct.equivalent_indices])
    # wyc_muls = np.array([len(inds) for inds in sym_struct.equivalent_indices])
    # types = np.array(sym_struct.atomic_numbers, dtype=np.uint8)
    # motif = sym_struct.cart_coords
    # cell = sym_struct.lattice.matrix
    
    # ops = spg.get_space_group_operations()
    # rot = np.array([op.rotation_matrix for op in ops])
    # trans = np.array([op.translation_vector for op in ops])
    # frac_motif, invs = _expand_asym_unit(, rot, trans, _EQ_SITE_TOL)

    # eq_inds = sym_structure.equivalent_indices
    # asym_inds = np.array([ix_list[0] for ix_list in eq_inds], dtype=np.int32)
    # wyc_muls = np.array([len(ix_list) for ix_list in eq_inds], dtype=np.int32)

    sym_structure = spg.get_conventional_standard_structure()
    motif = sym_structure.cart_coords
    cell = sym_structure.lattice.matrix

    asym_inds = np.arange(len(motif))
    wyc_muls = np.ones((len(motif), ), dtype=np.int32)
    types = np.array(sym_structure.atomic_numbers, dtype=np.uint8)

    return PeriodicSet(
        motif=motif,
        cell=cell,
        asym_unit=asym_inds,
        multiplicities=wyc_muls,
        types=types
    )


def periodicset_from_ccdc_entry(
        entry,
        remove_hydrogens: bool = False,
        disorder: str = 'skip',
        heaviest_component: bool = False,
        molecular_centres: bool = False
) -> PeriodicSet:
    """Convert a :class:`ccdc.entry.Entry` object to a
    :class:`amd.PeriodicSet <.periodicset.PeriodicSet>`.
    Entry is the type returned by :class:`ccdc.io.EntryReader`.

    Parameters
    ----------
    entry : :class:`ccdc.entry.Entry`
        A ccdc Entry object representing a database entry.
    remove_hydrogens : bool, optional
        Remove Hydrogens from the crystal.
    disorder : str, optional
        Controls how disordered structures are handled. Default is
        ``skip`` which skips any crystal with disorder, since disorder
        conflicts with the periodic set model. To read disordered
        structures anyway, choose either :code:`ordered_sites` to remove
        atoms with disorder or :code:`all_sites` include all atoms
        regardless of disorder.
    heaviest_component : bool, optional
        Removes all but the heaviest molecule in the asymmeric unit,
        intended for removing solvents.
    molecular_centres : bool, default False
        Use molecular centres of mass as the motif instead of centres of
        atoms.

    Returns
    -------
    :class:`amd.PeriodicSet <.periodicset.PeriodicSet>`
        Represents the crystal as a periodic set, consisting of a finite
        set of points (motif) and lattice (unit cell). Contains other
        useful data, e.g. the crystal's name and information about the
        asymmetric unit for calculation.

    Raises
    ------
    ParseError
        Raised if the structure fails parsing for any of the following:
        1. entry.has_3d_structure is False, 2.
        :code:``disorder == 'skip'`` and disorder is found on any atom,
        3. entry.crystal.molecule.all_atoms_have_sites is False,
        4. a.fractional_coordinates is None for any a in
        entry.crystal.disordered_molecule, 5. The motif is empty after
        removing Hydrogens and disordered sites.
    """

    # Entry specific flag
    if not entry.has_3d_structure:
        raise ParseError(f'{entry.identifier} has no 3D structure')

    # Disorder
    if disorder == 'skip' and entry.has_disorder:
        raise ParseError(
            f"{entry.identifier} has disorder, pass disorder='ordered_sites' "
            "or 'all_sites' to remove/ignore disorder"
        )

    return periodicset_from_ccdc_crystal(
        entry.crystal,
        remove_hydrogens=remove_hydrogens,
        disorder=disorder,
        heaviest_component=heaviest_component,
        molecular_centres=molecular_centres
    )


def periodicset_from_ccdc_crystal(
        crystal,
        remove_hydrogens: bool = False,
        disorder: str = 'skip',
        heaviest_component: bool = False,
        molecular_centres: bool = False
) -> PeriodicSet:
    """Convert a :class:`ccdc.crystal.Crystal` object to a
    :class:`amd.PeriodicSet <.periodicset.PeriodicSet>`.
    Crystal is the type returned by :class:`ccdc.io.CrystalReader`.

    Parameters
    ----------
    crystal : :class:`ccdc.crystal.Crystal`
        A ccdc Crystal object representing a crystal structure.
    remove_hydrogens : bool, optional
        Remove Hydrogens from the crystal.
    disorder : str, optional
        Controls how disordered structures are handled. Default is
        ``skip`` which skips any crystal with disorder, since disorder
        conflicts with the periodic set model. To read disordered
        structures anyway, choose either :code:`ordered_sites` to remove
        atoms with disorder or :code:`all_sites` include all atoms
        regardless of disorder.
    heaviest_component : bool, optional
        Removes all but the heaviest molecule in the asymmeric unit,
        intended for removing solvents.
    molecular_centres : bool, default False
        Use molecular centres of mass as the motif instead of centres of
        atoms.

    Returns
    -------
    :class:`amd.PeriodicSet <.periodicset.PeriodicSet>`
        Represents the crystal as a periodic set, consisting of a finite
        set of points (motif) and lattice (unit cell). Contains other
        useful data, e.g. the crystal's name and information about the
        asymmetric unit for calculation.

    Raises
    ------
    ParseError
        Raised if the structure fails parsing for any of the following:
        1. :code:``disorder == 'skip'`` and disorder is found on any
        atom, 2. crystal.molecule.all_atoms_have_sites is False,
        3. a.fractional_coordinates is None for any a in
        crystal.disordered_molecule, 4. The motif is empty after
        removing H, disordered sites or solvents.
    """

    molecule = crystal.disordered_molecule

    # Disorder
    if disorder == 'skip':
        if crystal.has_disorder or \
         any(_has_disorder(a.label, a.occupancy) for a in molecule.atoms):
            raise ParseError(
                f"{crystal.identifier} has disorder, pass "
                "disorder='ordered_sites' or 'all_sites' to remove/ignore "
                "disorder"
            )
    elif disorder == 'ordered_sites':
        molecule.remove_atoms(
            a for a in molecule.atoms if _has_disorder(a.label, a.occupancy)
        )

    if remove_hydrogens:
        molecule.remove_atoms(
            a for a in molecule.atoms if a.atomic_symbol in 'HD'
        )

    # Remove atoms with missing coordinates and warn
    if any(a.fractional_coordinates is None for a in molecule.atoms):
        warnings.warn('atoms without sites or missing data will be removed')
        molecule.remove_atoms(
            a for a in molecule.atoms if a.fractional_coordinates is None
        )

    if heaviest_component and len(molecule.components) > 1:
        molecule = _heaviest_component_ccdc(molecule)

    crystal.molecule = molecule
    cellpar = crystal.cell_lengths + crystal.cell_angles
    if None in cellpar:
        raise ParseError(f'{crystal.identifier} has missing cell data')
    cell = cellpar_to_cell(np.array(cellpar))

    if molecular_centres:
        frac_centres = _frac_molecular_centres_ccdc(crystal, _EQ_SITE_TOL)
        mol_centres = np.matmul(frac_centres, cell)
        return PeriodicSet(mol_centres, cell, name=crystal.identifier)

    asym_atoms = crystal.asymmetric_unit_molecule.atoms
    # check for None?
    asym_unit = np.array([tuple(a.fractional_coordinates) for a in asym_atoms])

    if asym_unit.shape[0] == 0:
        raise ParseError(f'{crystal.identifier} has no valid sites')

    asym_unit = np.mod(asym_unit, 1)

    # recommended by pymatgen
    # asym_unit = _snap_small_prec_coords(asym_unit, 1e-4)

    asym_types = [a.atomic_number for a in asym_atoms]

    # Remove overlapping sites unless disorder == 'all_sites'
    if disorder != 'all_sites':
        keep_sites = _unique_sites(asym_unit, _EQ_SITE_TOL)
        if not np.all(keep_sites):
            warnings.warn(
                'may have overlapping sites; duplicates will be removed'
            )
        asym_unit = asym_unit[keep_sites]
        asym_types = [sym for sym, keep in zip(asym_types, keep_sites) if keep]

    # Symmetry operations
    sitesym = crystal.symmetry_operators
    # try spacegroup numbers?
    if not sitesym:
        warnings.warn('no symmetry data found, defaulting to P1')
        sitesym = ['x,y,z']

    # Apply symmetries to asymmetric unit
    rot, trans = _parse_sitesyms(sitesym)
    frac_motif, invs = _expand_asym_unit(asym_unit, rot, trans, _EQ_SITE_TOL)
    _, wyc_muls = np.unique(invs, return_counts=True)
    asym_inds = np.zeros_like(wyc_muls, dtype=np.int32)
    asym_inds[1:] = np.cumsum(wyc_muls)[:-1]
    types = np.array([asym_types[i] for i in invs], dtype=np.uint8)
    motif = np.matmul(frac_motif, cell)

    return PeriodicSet(
        motif=motif,
        cell=cell,
        name=crystal.identifier,
        asym_unit=asym_inds,
        multiplicities=wyc_muls,
        types=types
    )


def memoize(f):
    """Cache for _parse_sitesym()."""
    cache = {}
    def wrapper(arg):
        if arg not in cache:
            cache[arg] = f(arg)
        return cache[arg]
    return wrapper


@memoize
def _parse_sitesym(sym: str) -> Tuple[FloatArray, FloatArray]:
    """Parse a single symmetry as an xyz string and return a 3x3
    rotation matrix and a 3x1 translation vector.
    """

    rot = np.zeros((3, 3), dtype=np.float64)
    trans = np.zeros((3, ), dtype=np.float64)

    for ind, element in enumerate(sym.split(',')):

        is_positive = True
        is_fraction = False
        sng_trans = None
        fst_trans = []
        snd_trans = []

        for char in element.lower():
            if char == '+':
                is_positive = True
            elif char == '-':
                is_positive = False
            elif char == '/':
                is_fraction = True
            elif char in 'xyz':
                rot_sgn = 1.0 if is_positive else -1.0
                rot[ind][ord(char) - ord('x')] = rot_sgn
            elif char.isdigit() or char == '.':
                if sng_trans is None:
                    sng_trans = 1.0 if is_positive else -1.0
                if is_fraction:
                    snd_trans.append(char)
                else:
                    fst_trans.append(char)

        if not fst_trans:
            e_trans = 0.0
        else:
            e_trans = sng_trans * float(''.join(fst_trans))

        if is_fraction:
            e_trans /= float(''.join(snd_trans))

        trans[ind] = e_trans

    return rot, trans


def _parse_sitesyms(symmetries: List[str]) -> Tuple[FloatArray, FloatArray]:
    """Parse a sequence of symmetries in xyz form and return rotation
    and translation arrays.
    """
    rotations = []
    translations = []
    for sym in symmetries:
        rot, trans = _parse_sitesym(sym)
        rotations.append(rot)
        translations.append(trans)
    return np.array(rotations), np.array(translations)


def _expand_asym_unit(
        asym_unit: FloatArray,
        rotations: FloatArray,
        translations: FloatArray,
        tol: float
) -> Tuple[FloatArray, IntArray]:
    """Expand the asymmetric unit by applying symmetries given by
    ``rotations`` and ``translations``.
    """

    asym_unit = asym_unit.astype(np.float64, copy=False)
    rotations = rotations.astype(np.float64, copy=False)
    translations = translations.astype(np.float64, copy=False)
    expanded_sites = _expand_sites(asym_unit, rotations, translations)
    frac_motif, invs = _reduce_expanded_sites(expanded_sites, tol)

    if not all(_unique_sites(frac_motif, tol)):
        frac_motif, invs = _reduce_expanded_equiv_sites(expanded_sites, tol)

    return frac_motif, invs


@numba.njit(cache=True)
def _expand_sites(
        asym_unit: FloatArray, rotations: FloatArray, translations: FloatArray
) -> FloatArray:
    """Expand the asymmetric unit by applying ``rotations`` and
    ``translations``, without yet removing points duplicated because
    they are invariant under a symmetry. Returns a 3D array shape
    (#points, #syms, dims).
    """

    m, dims = asym_unit.shape
    n_syms = len(rotations)
    expanded_sites = np.empty((m, n_syms, dims), dtype=np.float64)
    for i in range(m):
        p = asym_unit[i]
        for j in range(n_syms):
            expanded_sites[i, j] = np.dot(rotations[j], p) + translations[j]
    expanded_sites = np.mod(expanded_sites, 1)
    return expanded_sites


@numba.njit(cache=True)
def _reduce_expanded_sites(
        expanded_sites: FloatArray, tol: float
) -> Tuple[FloatArray, IntArray]:
    """Reduce the asymmetric unit after being expended by symmetries by
    removing invariant points. This is the fast version which works in
    the case that no two sites in the asymmetric unit are equivalent.
    If they are, the reduction is re-ran with
    _reduce_expanded_equiv_sites() to account for it.
    """

    all_unqiue_inds = []
    n_sites, _, dims = expanded_sites.shape
    multiplicities = np.zeros(shape=(n_sites, ))

    for i, sites in enumerate(expanded_sites):
        unique_inds = _unique_sites(sites, tol)
        all_unqiue_inds.append(unique_inds)
        multiplicities[i] = np.sum(unique_inds)

    m = int(np.sum(multiplicities))
    frac_motif = np.zeros(shape=(m, dims))
    inverses = np.zeros(shape=(m, ), dtype=np.int32)

    s = 0
    for i in range(n_sites):
        t = s + multiplicities[i]
        frac_motif[s:t, :] = expanded_sites[i][all_unqiue_inds[i]]
        inverses[s:t] = i
        s = t

    return frac_motif, inverses


def _reduce_expanded_equiv_sites(
        expanded_sites: FloatArray, tol: float
) -> Tuple[FloatArray, IntArray]:
    """Reduce the asymmetric unit after being expended by symmetries by
    removing invariant points. This is the slower version, called after
    the fast version if we find equivalent motif points which need to be
    removed.
    """

    sites = expanded_sites[0]
    unique_inds = _unique_sites(sites, tol)
    frac_motif = sites[unique_inds]
    inverses = [0] * len(frac_motif)

    for i in range(1, len(expanded_sites)):
        sites = expanded_sites[i]
        unique_inds = _unique_sites(sites, tol)

        points = []
        for site in sites[unique_inds]:
            diffs1 = np.abs(site - frac_motif)
            diffs2 = np.abs(diffs1 - 1)
            mask = np.all((diffs1 <= tol) | (diffs2 <= tol), axis=-1)

            if not np.any(mask):
                points.append(site)
            else:
                warnings.warn(
                    'has equivalent sites at positions '
                    f'{inverses[np.argmax(mask)]}, {i}'
                )

        if points:
            inverses.extend(i for _ in range(len(points)))
            frac_motif = np.concatenate((frac_motif, np.array(points)))

    return frac_motif, np.array(inverses, dtype=np.int64)


@numba.njit(cache=True)
def _unique_sites(asym_unit: FloatArray, tol: float) -> npt.NDArray[np.bool_]:
    """Uniquify (within tol) a list of fractional coordinates,
    considering all points modulo 1. Return an array of bools such that
    asym_unit[_unique_sites(asym_unit, tol)] is the uniquified list.
    """

    m, _ = asym_unit.shape
    where_unique = np.full(shape=(m, ), fill_value=True)
    for i in range(1, m):
        site_diffs1 = np.abs(asym_unit[:i, :] - asym_unit[i])
        site_diffs2 = np.abs(site_diffs1 - 1)
        sites_neq_mask = (site_diffs1 > tol) & (site_diffs2 > tol)
        if not np.all(np.sum(sites_neq_mask, axis=-1)):
            where_unique[i] = False
    return where_unique


def _has_disorder(label: str, occupancy) -> bool:
    """Return True if label ends with ? or occupancy is a number < 1."""
    try:
        occupancy = float(occupancy)
    except Exception:
        occupancy = 1
    return (occupancy < 1) or label.endswith('?')


def _atomic_symbols_from_labels(symbols: List[str]) -> List[str]:
    symbols_ = []
    for label in symbols:
        sym = ''
        if label and label not in ('.', '?'):
            match = re.search(r'([A-Za-z][A-Za-z]?)', label)
            if match is not None:
                sym = match.group()
            sym = list(sym)
            if len(sym) > 0:
                sym[0] = sym[0].upper()
            if len(sym) > 1:
                sym[1] = sym[1].lower()
            sym = ''.join(sym)
        symbols_.append(sym)
    return symbols_


def _get_syms_pymatgen(data: dict) -> Tuple[FloatArray, FloatArray]:
    """Parse symmetry operations given by data = block.data where block
    is a pymatgen CifBlock object. If the symops are not present the
    space group symbol/international number is parsed and symops are
    generated.
    """

    from pymatgen.symmetry.groups import SpaceGroup
    import pymatgen.io.cif

    # Try xyz symmetry operations
    for symmetry_label in _CIF_TAGS['symop']:
        xyz = data.get(symmetry_label)
        if not xyz:
            continue
        if isinstance(xyz, str):
            xyz = [xyz]
        return _parse_sitesyms(xyz)

    symops = []
    # Try spacegroup symbol
    for symmetry_label in _CIF_TAGS['spacegroup_name']:
        sg = data.get(symmetry_label)
        if not sg:
            continue
        sg = re.sub(r'[\s_]', '', sg)
        try:
            spg = pymatgen.io.cif.space_groups.get(sg)
            if not spg:
                continue
            symops = SpaceGroup(spg).symmetry_ops
            break
        except ValueError:
            pass
        try:
            for d in pymatgen.io.cif._get_cod_data():
                if sg == re.sub(r'\s+', '', d['hermann_mauguin']):
                    return _parse_sitesyms(d['symops'])
        except Exception:  # CHANGE
            continue
        if symops:
            break

    # Try international number
    if not symops:
        for symmetry_label in _CIF_TAGS['spacegroup_number']:
            num = data.get(symmetry_label)
            if not num:
                continue
            try:
                i = int(str2float(num))
                symops = SpaceGroup.from_int_number(i).symmetry_ops
                break
            except ValueError:
                continue

    if not symops:
        warnings.warn('no symmetry data found, defaulting to P1')
        return _parse_sitesyms(['x,y,z'])

    rotations = [op.rotation_matrix for op in symops]
    translations = [op.translation_vector for op in symops]
    rotations = np.array(rotations, dtype=np.float64)
    translations = np.array(translations, dtype=np.float64)
    return rotations, translations


def _frac_molecular_centres_ccdc(crystal, tol: float) -> FloatArray:
    """Return the geometric centres of molecules in the unit cell.
    Expects a ccdc Crystal object and returns fractional coordiantes.
    """

    frac_centres = []
    for comp in crystal.packing(inclusion='CentroidIncluded').components:
        coords = [a.fractional_coordinates for a in comp.atoms]
        frac_centres.append([sum(ax) / len(coords) for ax in zip(*coords)])
    frac_centres = np.mod(np.array(frac_centres, dtype=np.float64), 1)
    return frac_centres[_unique_sites(frac_centres, tol)]


def _heaviest_component_ccdc(molecule):
    """Remove all but the heaviest component of the asymmetric unit.
    Intended for removing solvents. Expects and returns a ccdc Molecule
    object.
    """

    component_weights = []
    for component in molecule.components:
        weight = 0
        for a in component.atoms:
            try:
                occ = float(a.occupancy)
            except:
                occ = 1
            try:
                weight += float(a.atomic_weight) * occ
            except ValueError:
                pass
        component_weights.append(weight)
    largest_component_ind = np.argmax(np.array(component_weights))
    molecule = molecule.components[largest_component_ind]
    return molecule


def str2float(string):
    """Remove uncertainty brackets from strings and return the float."""
    try:
        return float(re.sub(r'\(.+\)*', '', string))
    except TypeError:
        if isinstance(string, list) and len(string) == 1:
            return float(re.sub(r'\(.+\)*', '', string[0]))
    except ValueError as e:
        if string.strip() == '.':
            return 0.
        raise e
    raise ParseError(f'{string} cannot be converted to float')


def _snap_small_prec_coords(frac_coords: FloatArray, tol: float) -> FloatArray:
    """Find where frac_coords is within 1e-4 of 1/3 or 2/3, change to
    1/3 and 2/3. Recommended by pymatgen's CIF parser.
    """
    frac_coords[np.abs(1 - 3 * frac_coords) < tol] = 1 / 3.
    frac_coords[np.abs(1 - 3 * frac_coords / 2) < tol] = 2 / 3.
    return frac_coords
