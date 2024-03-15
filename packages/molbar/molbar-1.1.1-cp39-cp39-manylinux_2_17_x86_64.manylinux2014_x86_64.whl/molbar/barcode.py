import sys
import copy
import time
import numpy as np
from tqdm import tqdm
from typing import Union
from joblib import Parallel, delayed
from molbar.helper.input import _get_constraints, _transform_constraints
from molbar.molgraph.molgraph import MolGraph
from molbar.topography.unification import unify_fragments
from molbar.barcodes.barcodes import _get_barcode, _get_topology_barcodes
from molbar.helper.debug import _prepare_debug_data, _get_debug_path
from molbar.exceptions.error import MolBarGenerationError

def idealize_structure_from_file(file: str, return_data=False, timing=False, input_constraint=None,  write_trj=False) -> Union[list, str]:

    """
    Idealizes a whole molecule with the MolBar force field and returns the final energy, coordinates and elements.
    
    Args:

          file (str): The path to the input file to be processed.
          return_data (bool): Whether to print MolBar data.
          timing (bool): Whether to print the duration of this calculation.
          input_constraint (str): The path to the input file containing the constraint for the calculation. See documentation for more information.
          write_trj (bool, optional): Whether to write a trajectory of the unification process. Defaults to False.
      Returns:
          n_atoms (int): Number of atoms in the molecule.
          energy (float): Final energy of the molecule after idealization.
          coordinates (list): Final coordinates of the molecule after idealization.
          elements (list): Elements of the molecule.
          data (dict): Molbar data.
    """
 
    if input_constraint:

        input_constraint = _get_constraints(input_constraint)

        input_constraint = _transform_constraints(file, input_constraint)

    else:

        input_constraint = {}

    input_constraint["unique_repulsion"] = True

    start = time.time()
    result = _idealize_structure(file=file, single_constraint=input_constraint, debug=return_data, from_file=True, write_trj=write_trj)
    end = time.time()

    if timing:
            
            print("Duration [s]: " +
                str(np.round(end-start, 3)), file=sys.stderr)
            
    return result

def idealize_structure_from_coordinates(coordinates: list, elements: list, return_data=False, timing=False, input_constraint=None) -> Union[list, str]:
    """
    Idealizes a whole molecule with the MolBar force field and returns the final energy, coordinates and elements.

    Args:
        coordinates (list): Cartesian coordinates of the molecule.
        elements (list): Elements of the molecule.
        return_data (bool, optional): Whether to return more information. Defaults to False.
        timing (bool, optional): Whether to print timing information. Defaults to False.
        input_constraint (dict, optional): The constraint for the calculation. See documentation for more information. Defaults to None.
    Returns:
        n_atoms (int): Number of atoms in the molecule.
        energy (float): Final energy of the molecule after idealization.
        coordinates (list): Final coordinates of the molecule after idealization.
        elements (list): Elements of the molecule.
        data (dict):  MolBar data.
    """

    if not input_constraint:

        input_constraint = {}

    start = time.time()
    result = _idealize_structure(coordinates=coordinates, elements=elements, single_constraint=input_constraint, debug=return_data, write_trj=False)
    end = time.time()

    if timing:
            
            print("Duration [s]: " +
                str(np.round(end-start, 3)), file=sys.stderr)
            
    return result


def get_molbars_from_coordinates(list_of_coordinates: list, list_of_elements: list, return_data=False, threads=1, timing=False, input_constraints=None, progress=False,  mode="mb") -> Union[list, Union[str, dict]]:
    """
    Sets up the MolGraph object for the calculation of the molecular barcode for a list of coordinates with a list of constraints.
    And runs the calculation in parallel if more than one thread is used.

    Args:

          list_of_coordinates (list): A list of molecular geometries provided by atomic Cartesian coordinates with shape (n_molecules, n_atoms, 3).
          list_of_elements (list): A list of element lists for each molecule in the list_of_coordinates with shape (n_molecules, n_atoms).
          return_data (bool): Whether to return MolBar data.
          threads (int): Number of threads to use for the calculation. If you need to process multiple molecules at once, it is recommended to use this function and specify the number of threads that can be used to process multiple molecules simultaneously.
          timing (bool):  Whether to print the duration of this calculation.
          input_constraints (list, optional): A list of constraints for the calculation. Each constraint in that list is a Python dict as shown in the documentation.
          progress (bool): Whether to show a progress bar.
          mode (str): Whether to calculate the molecular barcode ("mb") or the topology part of the molecular barcode ("topo").

      Returns:

          Union[list, Union[str, dict]]: Either MolBar or the MolBar and MolBar data.

    """
    
    if not input_constraints:

        input_constraints = [{}]*len(list_of_elements)
        
    if progress:

        results = Parallel(n_jobs=threads)(delayed(_run_calc_for_coordinates)(file=str(i), coordinates=coord, elements=elem, single_constraint=copy.deepcopy(single_constraint), debug=return_data, timing=timing,
                                                                              mode=mode) for i, single_constraint, coord, elem in tqdm(zip(range(len(list_of_coordinates)), input_constraints, list_of_coordinates, list_of_elements), total=len(list_of_elements), file=sys.stdout))

    else:

        results = Parallel(n_jobs=threads)(delayed(_run_calc_for_coordinates)(file=str(i), coordinates=coord, elements=elem, single_constraint=copy.deepcopy(single_constraint), debug=return_data, timing=timing,
                                                                              mode=mode) for i, single_constraint, coord, elem in zip(range(len(list_of_coordinates)), input_constraints, list_of_coordinates, list_of_elements))

    return results


def get_molbar_from_coordinates(coordinates: list, elements: list, return_data=False, timing=False, input_constraint=None, mode="mb") -> Union[str, dict]:
    """
    Sets up the MolGraph object for the calculation of the molecular barcode for a single set of coordinates with a single constraint.

    Args:

          coordinates (list): Molecular geometry provided by atomic Cartesian coordinates with shape (n_atoms, 3).
          elements (list): A list of elements in that molecule.
          return_data (bool): Whether to return MolBar data.
          timing (bool): Whether to print the duration of this calculation.
          input_constraint (dict, optional): A dict of extra constraints for the calculation. See documentation for more information. USED ONLY IN EXCEPTIONAL CASES.
          mode (str): Whether to calculate the molecular barcode ("mb") or only the topology part of the molecular barcode ("topo").

      Returns:

          Union[str, dict]: Either MolBar or the MolBar and MolBar data.

    """

    if not input_constraint:

        input_constraint = {}

    return _run_calc_for_coordinates("", coordinates, elements, single_constraint=input_constraint, debug=return_data, timing=timing, mode=mode)


def get_molbars_from_files(files: list, return_data=False, threads=1, timing=False, input_constraints=None, progress=False, mode="mb", write_trj=False) ->Union[list, Union[str, dict]]:
    """
    Sets up the MolGraph object for the calculation of the molecular barcode for a list of files with a list of constraints.
    And runs the calculation in parallel if more than one thread is used.

    Args:

          files (list): The list of paths to the files containing the molecule information (either .xyz/.sdf/.mol format).
          return_data (bool): Whether to return MolBar data.
          threads (int): Number of threads to use for the calculation. If you need to process multiple molecules at once, it is recommended to use this function and specify the number of threads that can be used to process multiple molecules simultaneously.
          timing (bool):  Whether to print the duration of this calculation.
          input_constraints (list, optional): A list of file paths to the input files for the calculation. Each constrained is specified by a file path to a .yml file, as shown in the documentation.
          progress (bool): Whether to show a progress bar.
          mode (str): Whether to calculate the molecular barcode ("mb") or the topology part of the molecular barcode ("topo").
          write_trj (bool, optional): Whether to write a trajectory of the unification process. Defaults to False.

      Returns:

          Union[list, Union[str, dict]]: Either MolBar or the MolBar and MolBar data.

    """

    if not input_constraints:

        input_constraints = [None]*len(files)

    if progress:
        results = Parallel(n_jobs=threads)(delayed(_run_calc_for_file)(file=file, single_constraint=copy.deepcopy(single_constraint), debug=return_data, timing=timing,
                                                                       mode=mode, write_trj=write_trj) for single_constraint, file in tqdm(zip(input_constraints, files), total=len(files), file=sys.stdout))
    else:
        results = Parallel(n_jobs=threads)(delayed(_run_calc_for_file)(file=file, single_constraint=copy.deepcopy(single_constraint), debug=return_data,
                                                                       timing=timing, mode=mode, write_trj=write_trj) for single_constraint, file in zip(input_constraints, files))
    return results


def get_molbar_from_file(file: str, return_data=False, timing=False, input_constraint=None, mode="mb", write_trj=False) -> Union[str, dict]:

    """
    Sets up the MolGraph object for the calculation of the molecular barcode for a single file with a single constraint.

    Args:
          file (str): The path to the file containing the molecule information (either .xyz/.sdf/.mol format).
          return_data (bool): Whether to return MolBar data.
          timing (bool): Whether to print the duration of this calculation.
          input_constraint (dict, optional): A dict of extra constraints for the calculation. See documentation for more information. USED ONLY IN EXCEPTIONAL CASES.
          mode (str): Whether to calculate the molecular barcode ("mb") or only the topology part of the molecular barcode ("topo").
          write_trj (bool, optional): Whether to write a trajectory of the unification process. Defaults to False.
      
      Returns:

          Union[str, dict]: Either MolBar or the MolBar and MolBar data.

    """

    return _run_calc_for_file(file=file, single_constraint=input_constraint, debug=return_data, timing=timing, mode=mode, write_trj=write_trj)


def _run_calc_for_coordinates(file: str, coordinates: list, elements: list, single_constraint={}, debug=False, mode="mb", timing=False) -> Union[list, str]:
    """
    Sets up the MolGraph object for the calculation of the molecular barcode for a single set of coordinates with a single constraint.

    Args:
        coordinates (list): Cartesian coordinates of the molecule.
        elements (list): Elements of the molecule.
        single_constraint (dict, optional): Constraint for the calculation. Defaults to {}. See documentation for more information.
        debug (bool, optional): Weather to print debugging information. Defaults to False.
        mode (str, optional): Whether to calculate the molecular barcode ("mb") or the topology part of the molecular barcode ("topo"). Defaults to "mb".
        timing (bool, optional): Whether to print timing information. Defaults to False.

    Raises:
        MolBarGenerationError: If the calculation fails.

    Returns:
        Union[list, str]: Either list with filename and molecular barcode or only molecular barcode.
    """

    start = time.time()

    try:

        if mode == "mb":

            barcode, debug_data = _get_molbar(coordinates=coordinates, elements=elements,
                                  single_constraint=single_constraint, debug=debug, from_file=False, write_trj=False)

        else:

            barcode, debug_data = _get_topobar(coordinates=coordinates, elements=elements,
                                   single_constraint=single_constraint, debug=debug, from_file=False)

    except:

        raise MolBarGenerationError(file)

    end = time.time()

    if timing:

        print("Duration [s]: " +
              str(np.round(end-start, 3)), file=sys.stderr)

    if debug == True:

        return barcode, debug_data
    
    else:

        return barcode


def _run_calc_for_file(file, single_constraint=None, debug=False, mode="mb", timing=False, write_trj=False) -> Union[list, str]:

    if not single_constraint:

        input_constraint = {}

    else:

        input_constraint = _get_constraints(single_constraint)

        input_constraint = _transform_constraints(file, input_constraint)

    start = time.time()

    try:

        if mode == "mb":

            barcode, debug_data = _get_molbar(
                file, single_constraint=input_constraint, debug=debug, from_file=True, write_trj=write_trj)

        elif mode == "topo":

            barcode, debug_data = _get_topobar(
                file, single_constraint=input_constraint, debug=debug, from_file=True)

    except:

        raise MolBarGenerationError(file)

    end = time.time()

    if timing:

        print("Duration [s]: " +
              str(np.round(end-start, 3)), file=sys.stderr)
        
    if debug == True:

        return barcode, debug_data
    
    else:

        return barcode


def _get_molbar(file=None, coordinates=None, elements=None, single_constraint=None, debug=False, from_file=False, write_trj=False) -> Union[list, str]:
    """
    Sets up the MolGraph object for the calculation of the molecular barcode for a single file with a single constraint.
    Args:
        file (str): The path to the input file to be processed.
        single_constraint (dict): A dictionary containing the constraint for the calculation. See documentation for more information.
        debug (bool): Whether to print debugging information.
        multiple (bool, optional): If filename should be returned. Needed for several files processed at once. Defaults to False.
        write_trj (bool, optional): Whether to write a trajectory of the unification process. Defaults to False.

    Returns:
        Union[list, str]: Either list with filename and molecular barcode or only molecular barcode.
    """

    # Initialize MolGraph object.
    molgraph = MolGraph()

    molgraph.file = file

    molgraph._commandline = write_trj

    if single_constraint == False:

        single_constraint = {}

    # Set the constraint for the calculation.
    molgraph.constraints = single_constraint

    if from_file:
        # Read the input file.
        molgraph.from_file(filepath=file)

    else:

        molgraph.from_coordinates(coordinates=coordinates, elements=elements)

    molgraph.set_nodes_visible(include_all=True)

    molgraph.define_edges()

    # Set all nodes to visible.
    molgraph.set_nodes_visible(include_all=True)

    start = time.time()

    molgraph.assign_bond_orders()

    end = time.time()

    molgraph.bo_time = np.round(end-start, 6)

    # Set all nodes to visible.
    molgraph.set_nodes_visible(include_all=True)

    # Calculate the atomic priorities.
    start = time.time()

    molgraph.calculate_priorities()

    end = time.time()

    molgraph.prio_time = np.round(end-start, 6)

    start = time.time()

    molgraph.detect_cycles()

    end = time.time()

    molgraph.cycle_time = np.round(end-start, 6)

    # Set all nodes to visible.
    molgraph.set_nodes_visible(include_all=True)

    molgraph._get_repulsion_pairs()

    molgraph.set_nodes_visible(include_all=True)

    # Calculate the VSEPR geometry of each nodes.
    molgraph.classify_nodes_geometry(is_adjacent_visible=True)

    # Define angle constraints and internal dihedral constraints based on VSEPR geometry.
    molgraph.constrain_nodes_angles(is_adjacent_visible=True)

    # Set all nodes to visible.
    molgraph.set_nodes_visible(include_all=True)

    # Define dihedral constraints based on double bonds.
    molgraph._add_db_dihedral_constraints()

    molgraph.set_nodes_visible(include_all=True)

    molgraph._add_allene_dihedral_constraints()

    molgraph.set_nodes_visible(include_all=True)

    # Define dihedral constraints based on cycles.
    molgraph._add_cycle_dihedral_constraints()

    molgraph.set_nodes_visible(include_all=True)

    # Set all nodes to visible.
    molgraph.set_nodes_visible(include_all=True)

    # Fragmentation of the molecule based on rigidity analysis.
    molgraph.rigid_fragmentation(include_all=True)

    molgraph.set_nodes_visible(include_all=True)

    molgraph.set_edges_visible(include_all=True)

    # Get debug path based on file path.
    debug_path = _get_debug_path(file)

    # Unification of fragemnts based on force field.
    start = time.time()

    molgraph = unify_fragments(
        molgraph, write_trj=write_trj, debug_path=debug_path)

    end = time.time()

    molgraph.ff_time = np.round(end-start, 6)

    molbar_str = _get_barcode(molgraph)

    if debug:

        debug_data = _prepare_debug_data(molbar_str, molgraph)

    else:

        debug_data = {}

    return molbar_str, debug_data


def _get_topobar(file=None, coordinates=None, elements=None, single_constraint=None, debug=False, from_file=False) -> Union[list, str]:
    """
    Sets up the MolGraph object for the calculation of the topology part of the molecular barcode for a single file with a single constraint.
    Args:
        file (str): The path to the input file to be processed.
        single_constraint (dict): A dictionary containing the constraint for the calculation. See documentation for more information.
        debug (bool): Whether to print debugging information.
        multiple (bool, optional): If filename should be returned. Needed for several files processed at once. Defaults to False.

    Returns:
        Union[list, str]: Either list with filename and molecular barcode or only molecular barcode.
    """

    # Initialize MolGraph object.
    molgraph = MolGraph()

    # Set the constraint for the calculation.
    molgraph.constraints = single_constraint

    if from_file:
        # Read the input file.
        molgraph.from_file(filepath=file)
    else:
        molgraph.from_coordinates(coordinates=coordinates, elements=elements)

    # Define edges from coordinates of input file.
    molgraph.define_edges()

    # Set all nodes to visible.
    molgraph.set_nodes_visible(include_all=True)

    topobar_str = _get_topology_barcodes(molgraph)

    if debug:

        debug_data = _prepare_debug_data(topobar_str, molgraph)

    else:

        debug_data = {}

    return topobar_str, debug_data
    

def _idealize_structure(file=None, coordinates=None, elements=None, single_constraint=None, debug=False, from_file=False, write_trj=False) -> Union[list, str]:
    """
    Sets up the MolGraph object to idealize a whole molecule with the force field.
    Args:
        file (str): The path to the input file to be processed.
        single_constraint (dict): A dictionary containing the constraint for the calculation. See documentation for more information.
        debug (bool): Whether to print debugging information.
        multiple (bool, optional): If filename should be returned. Needed for several files processed at once. Defaults to False.

    Returns:
        Union[list, str]: Either list with filename and molecular barcode or only molecular barcode.
    """

     # Initialize MolGraph object.
    molgraph = MolGraph()

    molgraph._commandline = write_trj

    if single_constraint == False:

        single_constraint = {}

    # Set the constraint for the calculation.
    molgraph.constraints = single_constraint

    if from_file:
        # Read the input file.
        molgraph.from_file(filepath=file)

    else:

        molgraph.from_coordinates(coordinates=coordinates, elements=elements)

    molgraph.set_nodes_visible(include_all=True)

    if molgraph.constraints.get("set_edges") != False:

        molgraph.define_edges()

    molgraph._add_bond_constraints()

    # Set all nodes to visible.
    molgraph.set_nodes_visible(include_all=True)

    # Calculate bond orders if allowed by constraints.
    if molgraph.constraints.get("bond_order_assignment") != False:

        start = time.time()

        molgraph.assign_bond_orders()

        end = time.time()

        molgraph.bo_time = np.round(end-start, 6)

    # Set all nodes to visible.
    molgraph.set_nodes_visible(include_all=True)

    # Calculate the atomic priorities.
    start = time.time()

    molgraph.calculate_priorities()

    end = time.time()

    molgraph.prio_time = np.round(end-start, 6)

    # Detects cycles if allowed by constraints.
    if molgraph.constraints.get("cycle_detection") != False:

        start = time.time()

        molgraph.detect_cycles()

        end = time.time()

        molgraph.cycle_time = np.round(end-start, 6)

    # Set all nodes to visible.
    molgraph.set_nodes_visible(include_all=True)

    if molgraph.constraints.get("set_angles") != False:

        # Calculate the VSEPR geometry of each nodes.
        molgraph.classify_nodes_geometry(is_adjacent_visible=True)

        # Define angle constraints and internal dihedral constraints based on VSEPR geometry.
        molgraph.constrain_nodes_angles(is_adjacent_visible=True)

    # Set all nodes to visible.
    molgraph.set_nodes_visible(include_all=True)

    if molgraph.constraints.get("set_dihedrals") != False:

        # Define dihedral constraints based on double bonds.
        molgraph._add_db_dihedral_constraints()

        # Define dihedral constraints based on cycles.
        molgraph._add_cycle_dihedral_constraints()

    molgraph.set_nodes_visible(include_all=True)

    molgraph.set_edges_visible(include_all=True)

    if molgraph.constraints.get("set_repulsion") != False:

        molgraph._get_repulsion_pairs()

    # Set all nodes to visible.
    molgraph.set_nodes_visible(include_all=True)

    # All atoms are one fragment
    molgraph.add_node_data(attribute="fragment_id", new_data=[
        0]*molgraph.return_n_atoms())

    molgraph.set_nodes_visible(include_all=True)

    molgraph.set_edges_visible(include_all=True)

    # Get debug path based on file path.
    debug_path = _get_debug_path(file)

    # Unification of fragemnts based on force field.
    start = time.time()
    molgraph = unify_fragments(
        molgraph, write_trj=write_trj, debug_path=debug_path)
    
    end = time.time()

    molgraph.ff_time = np.round(end-start, 6)
    
    if debug:

        debug_data = _prepare_debug_data("", molgraph)

    else:

        debug_data = {}

    n_atoms = molgraph.return_n_atoms()

    final_energy = molgraph.fragments_data[0]["final_energy"]

    final_geometry = molgraph.fragments_data[0]["final_geometry"]

    elements = molgraph.fragments_data[0]["elements"]

    return final_energy, final_geometry, elements, n_atoms, debug_data


if __name__ == "__main__":
    from molbar.io.filereader import FileReader
    from molbar.helper.printer import Printer
    constrain_l =  [{'atoms': [1, 2], 'value': 1.5},
                {'atoms': [2, 3], 'value': 1.5},
                {'atoms': [3, 4], 'value': 1.46},
                {'atoms': [4, 5], 'value': 1.46},
                {'atoms': [1, 6], 'value': 1.5},
                {'atoms': [5, 6], 'value': 1.5},
                {'atoms': [1, 7], 'value': 1.07},
                {'atoms': [2, 8], 'value': 1.07},
                {'atoms': [3, 9], 'value': 1.07},
                {'atoms': [5, 10], 'value': 1.07},
                {'atoms': [6, 11], 'value': 1.07},
                {'atoms': [12, 13], 'value': 1.5},
                {'atoms': [13, 14], 'value': 1.5},
                {'atoms': [13, 15], 'value': 1.5},
                {'atoms': [15, 16], 'value': 1.5},
                {'atoms': [16, 17], 'value': 1.5},
                {'atoms': [17, 18], 'value': 1.5},
                {'atoms': [18, 19], 'value': 1.5},
                {'atoms': [15, 20], 'value': 1.5},
                {'atoms': [19, 20], 'value': 1.5},
                {'atoms': [12, 21], 'value': 1.07},
                {'atoms': [12, 22], 'value': 1.07},
                {'atoms': [12, 23], 'value': 1.07},
                {'atoms': [14, 24], 'value': 1.07},
                {'atoms': [14, 25], 'value': 1.07},
                {'atoms': [14, 26], 'value': 1.07},
                {'atoms': [16, 27], 'value': 1.07},
                {'atoms': [17, 28], 'value': 1.07},
                {'atoms': [18, 29], 'value': 1.07},
                {'atoms': [19, 30], 'value': 1.07},
                {'atoms': [20, 31], 'value': 1.07},
                {'atoms': [4, 13], 'value': 1.5}]

    extra_constraints = {'bond_order_assignment': True,
                        'cycle_detection': True,
                        'set_edges': False,  # False if no bonds should be constrained automatically.
                        'set_angles': False,  # False if no angles should be constrained automatically.
                        'set_dihedrals': False,  # False if no dihedrals should be constrained automatically.
                        'set_repulsion': False,  # False if no coulomb term should be used automatically.
                        'repulsion_charge': 100.0,
                        # Charged used for the Coulomb term in the Force field, every atom-atom pair uses the same charge, only reasonable opt mode (standalone force-field optimization). Defaults to 100.0
                        'constraints': {'bonds': constrain_l}
                        # atoms: list of atoms that define the dihedral, value is the ideal dihedral angle in degrees, atom indexing starts with 1.
                        }

    n_atoms, coordinates, ele = FileReader("/Users/nilsvanstaalduinen/students/ying/xtbtopo.mol").read_file()
    final_energy, final_geometry, elements, n_atoms, debug_data = idealize_structure_from_coordinates(coordinates, ele, input_constraint=extra_constraints, return_data=True)
    Printer(n_atoms, "", final_geometry, elements,"final_geometry.xyz").print()
