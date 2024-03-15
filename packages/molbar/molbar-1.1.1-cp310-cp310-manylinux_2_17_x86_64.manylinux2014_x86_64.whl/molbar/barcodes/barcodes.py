
import numpy as np
import time
from decimal import Decimal, ROUND_HALF_UP
from molbar.molgraph.fraggraph import FragGraph
from molbar.molgraph.molgraph import MolGraph
from molbar.barcodes.spectrum import refine_spectrum
from collections import Counter
from importlib.metadata import version


def _get_barcode(molgraph: MolGraph) -> str:
    """
    Calculates the barcode based on the MolGraph object.

    Args:
        molgraph (MolGraph): A MolGraph object.

    Returns:
        A string containing the barcode of the molecule.
    """

    # Set all nodes to visible
    molgraph.set_nodes_visible(include_all=True)

    # Get the elements of the molecule
    elements = molgraph.return_node_data(attribute="elements")

    # Get the topology barcode
    start = time.time()

    topology_spectrum = _get_topology_barcode(molgraph)

    molgraph.topology_spectrum = topology_spectrum

    topology_spectrum_str = _get_rounded_spectrum_as_str(topology_spectrum)

    end = time.time()

    molgraph.topology_time = np.round(end-start, 6)

    # Get the heavy atom topology barcode

    heavy_atom_topology_spectrum = _get_heavy_atom_topology_barcode(molgraph)

    molgraph.heavy_atom_topology_spectrum = heavy_atom_topology_spectrum

    heavy_atom_topology_spectrum_str = _get_rounded_spectrum_as_str(heavy_atom_topology_spectrum)

    start = time.time()
    # Get the topography barcode

    topography_spectrum = _get_topography_barcode(molgraph)

    molgraph.topography_spectrum = topography_spectrum

    topography_spectrum_str = _get_rounded_spectrum_as_str(topography_spectrum)

    end = time.time()

    molgraph.topography_time = np.round(end-start, 6)

    start = time.time()
    # Get the absolute configuration barcode

    absconfiguration_spectrum = _get_absconf_barcode(molgraph)

    molgraph.absconfiguration_spectrum = absconfiguration_spectrum

    absconfiguration_spectrum_str = _get_rounded_spectrum_as_str(absconfiguration_spectrum)

    end = time.time()

    molgraph.chirality_time = np.round(end-start, 6)

    # Create the molecular formula
    molecular_formula = _get_molecular_formular(elements)

    # Create the topography barcode

    mb_version = version('molbar')

    return f"MolBar | {mb_version} | {molecular_formula} | {topology_spectrum_str} | {heavy_atom_topology_spectrum_str} | {topography_spectrum_str} | {absconfiguration_spectrum_str} "


def _get_molecular_formular(elements: list) -> str:
    """
    Creates the molecular formula from a list of elements.

    Args:
        elements (list): A list of elements.

    Returns:
        str: molecular formula
    """
    element_counts = Counter(elements).items()
    # Sort the elements by their count
    sorted_elements = _sort_element_counts(element_counts)
    # Create the molecular formula
    return ''.join(f'{element}{count}' if count > 1 else element for element, count in sorted_elements)


def _get_topology_barcodes(molgraph):
    """
    Calculates the topology barcodes only of a molecule.

    Args:
        molgraph (MolGraph): A MolGraph object.

    Returns:
        A list containing the barcode of the molecule.
    """

    molgraph.set_nodes_visible(include_all=True)

    elements = molgraph.return_node_data(attribute="elements")

    # Get the topology barcode
    start = time.time()

    topology_spectrum = _get_topology_barcode(molgraph)

    molgraph.topology_spectrum = topology_spectrum

    topology_spectrum_str = _get_rounded_spectrum_as_str(topology_spectrum)

    end = time.time()

    molgraph.topology_time = np.round(end-start, 6)

    # Get the heavy atom topology barcode

    heavy_atom_topology_spectrum = _get_heavy_atom_topology_barcode(molgraph)

    molgraph.heavy_atom_topology_spectrum = heavy_atom_topology_spectrum

    heavy_atom_topology_spectrum_str = _get_rounded_spectrum_as_str(heavy_atom_topology_spectrum)

    element_counts = Counter(elements).items()
    # Sort the elements by their count
    sorted_elements = _sort_element_counts(element_counts)
    # Create the molecular formula
    molecular_formula = ''.join(
        f'{element}{count}' if count > 1 else element for element, count in sorted_elements)
    # Create the topography barcode
    mb_version = version('molbar')

    return f"TopoBar | {mb_version} | {molecular_formula} | {topology_spectrum_str} | {heavy_atom_topology_spectrum_str}"


def _get_topology_barcode(molgraph: MolGraph) -> np.ndarray:
    """
    Calculates the topology barcode based on the MolGraph object.

    Args:
        molgraph (MolGraph): A MolGraph object.

    Returns:
        np.ndarray: A list containing the topology spectrum of the molecule.
    """

    molgraph.set_nodes_visible(include_all=True)

    n_atoms = molgraph.return_n_atoms()

    adjacency_matrix = molgraph.return_cn_matrix()

    atomic_numbers = molgraph.return_node_data(attribute="atomic_numbers")

    degrees = molgraph.get_degree()

    return _calculate_barcode(n_atoms, adjacency_matrix, atomic_numbers, degrees)


def _get_heavy_atom_topology_barcode(molgraph: MolGraph) -> np.ndarray:
    """
    Calculates the heavy atom topology barcode based on the MolGraph object.

    Args:
        molgraph (MolGraph): A MolGraph object.

    Returns:
        np.ndarray: A list containing the heavy atom topology spectrum of the molecule.
    """

    elements = molgraph.return_node_data(attribute="elements")

    heavy_atom_indices = [
        i for i, element in enumerate(elements) if element != "H"]

    molgraph.set_nodes_visible(visible_nodes=heavy_atom_indices)

    n_atoms = molgraph.return_n_atoms(include_all=False)

    adjacency_matrix = molgraph.return_cn_matrix(include_all=False)

    atomic_numbers = molgraph.return_node_data(attribute="atomic_numbers")

    degrees = molgraph.get_degree(include_all=False)

    return _calculate_barcode(n_atoms, adjacency_matrix, atomic_numbers, degrees)


def _get_topography_barcode(molgraph: MolGraph) -> np.ndarray:
    """
    Calculates the topography barcode based on the MolGraph object.

    Args:
        molgraph (MolGraph): A MolGraph object.

    Returns:
        np.ndarray: A list containing the topography spectrum of the molecule.
    """

    molgraph.set_nodes_visible(include_all=True)

    n_atoms = molgraph.return_n_atoms()

    cm_matrix = molgraph.unified_coulomb_matrix

    atomic_numbers = molgraph.return_node_data(attribute="atomic_numbers")

    degrees = molgraph.get_degree()

    return _calculate_barcode(n_atoms, cm_matrix, atomic_numbers, degrees)


def _get_absconf_barcode(molgraph: MolGraph) -> np.ndarray:
    """
    Calculates the absolute configuration barcode based on the MolGraph object.

    Args:

        molgraph (MolGraph): A MolGraph object.

    Returns:

        np.ndarray: A list containing the absolute configuration spectrum of the molecule.
    """
    molgraph.set_nodes_visible(include_all=True)

    fraggraph = FragGraph(molgraph)

    if fraggraph.n_fragments == 0:

        return np.array([])

    fragment_distance_matrix = fraggraph.get_fragment_distance_matrix()

    np.fill_diagonal(fragment_distance_matrix, 1)

    fragment_coulomb_matrix = 1/fragment_distance_matrix

    n_fragments = fraggraph.return_n_fragments()

    abs_conf_indices = fraggraph.get_abs_conf_indices()

    fragment_priorities = fraggraph.return_fragment_priorities()

    molgraph.fragment_priorities = np.array(fragment_priorities, dtype=int)

    return _calculate_absconf_barcode(n_fragments, fragment_coulomb_matrix, abs_conf_indices, fragment_priorities)


def _calculate_barcode(n_atoms, matrix, nuclear_charges, degrees) -> np.ndarray:
    """
    Calculates the adjacency spectrum of a molecule.

    Args:
        cn_matrix (np.ndarray): A matrix representing the coordination numbers of each pair of atoms.
        charges (list): A list of the charges for each atom in the molecule.
        cn (list): A list of the coordination numbers for each atom in the molecule.

    Returns:
        An array containing the adjacency spectrum of the molecule, rounded to one decimal place and
        multiplied by 10 and converted to integers.
    """

    # Calculate the matrix diagonal values
    matrix_diagonal = (degrees+1)*nuclear_charges

    # Create the diagonal barcode matrix
    diagonal_barcode_matrix = np.diag(matrix_diagonal)

    # Create the off-diagonal barcode matrix
    off_diagonal_barcode_matrix = np.zeros((n_atoms, n_atoms))
    off_diagonal_barcode_matrix[:, :] = matrix_diagonal
    off_diagonal_barcode_matrix = 0.5 * \
        (off_diagonal_barcode_matrix + off_diagonal_barcode_matrix.transpose())

    # Create the barcode matrix
    barcode_matrix = off_diagonal_barcode_matrix * matrix + diagonal_barcode_matrix

    # Calculate the eigenvalues of the barcode matrix and round them to one decimal point

    spectrum = np.linalg.eigvalsh(barcode_matrix)*10

    return spectrum

def _calculate_absconf_barcode(n_fragments, matrix, abs_conf_indices, priorities):

    barcode_matrix = np.zeros((n_fragments, n_fragments))

    matrix_diagonal = abs_conf_indices * priorities

    atomic_matrix = np.zeros((n_fragments, n_fragments))

    atomic_matrix[:, :] = matrix_diagonal

    atomic_matrix = 0.5 * (atomic_matrix + atomic_matrix.transpose())

    np.fill_diagonal(atomic_matrix, matrix_diagonal)

    barcode_matrix = matrix * atomic_matrix

    spectrum = np.linalg.eigvalsh(barcode_matrix)*10

    return spectrum


def _sort_element_counts(element_counts):
    # Sort the element_counts list by the first element, which is the element symbol
    element_counts_sorted = sorted(element_counts, key=lambda x: x[0])

    # Move the tuple with the "H" element symbol to the end of the list
    for i in range(len(element_counts_sorted)):
        if element_counts_sorted[i][0] == "H":
            element_counts_sorted.append(element_counts_sorted.pop(i))
            break

    return element_counts_sorted

def _get_rounded_spectrum_as_str(spectrum):

    decimal_spectrum = [Decimal(eps).quantize(Decimal('1.000'), rounding=ROUND_HALF_UP) for eps in spectrum]

    rounded_spectrum = [eps.quantize(Decimal('1'), rounding=ROUND_HALF_UP) for eps in decimal_spectrum]
    
    spectrum_str = " ".join([str(eps) for eps in rounded_spectrum])

    if "-0" in spectrum_str:

        spectrum_str = spectrum_str.replace("-0", "0")

    return spectrum_str
