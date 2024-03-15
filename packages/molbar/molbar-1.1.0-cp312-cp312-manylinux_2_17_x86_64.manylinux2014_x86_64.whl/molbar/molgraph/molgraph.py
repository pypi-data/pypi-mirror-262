import networkx as nx
import numpy as np
from scipy.stats import rankdata
from molbar.io.filereader import FileReader
from molbar.molgraph.nodes.nodes import Nodes
from molbar.molgraph.edges.edges import Edges
from molbar.molgraph.edges.coordination import Coordination
from molbar.molgraph.edges.bond_order import BondOrder
from molbar.molgraph.cycles import Cycle
from molbar.molgraph.nodes.vsepr import VSEPR
from molbar.molgraph.edges.dihedral import Dihedral
from molbar.molgraph.repulsion import Repulsion
from molbar.molgraph.nodes.priorities import Priorities


class MolGraph(nx.Graph, FileReader, Nodes, Edges, Coordination, BondOrder, Priorities, Cycle, Repulsion, VSEPR, Dihedral):
    """
    MolGraph is a subclass of networkx.Graph. It inherits all methods from networkx.Graph and adds additional methods for the construction of molecular graphs.
    """

    def __init__(self, data=None, **attr):
        """
        Constructs MolGraph object.
        Args:
            data (optional): Additional data needed for the construction fo the Networkx graph. Defaults to None.
        """

        super().__init__(data, **attr)

        self.constraints = {}

        self.unified_distance_matrix = np.array([])

        self.cycle_nodes = []

        self.visible_repulsion_nodes = []

        self.fragment_data = {}

        self.is_2D = False

    def from_file(self, filepath: str) -> None:
        """
        Reads a file and constructs a MolGraph object from coordinates.

        Args:
            filepath (str): Path to file containing coordinates. Either .xyz, .coord, .sdf or .mol file.

        Raises:
            XYZNotFound: If the file does not exist.
            NotXYZFormat: If the input geometry is not in .xyz format.
        """

        self.filepath = filepath

        # Load tabulated chemical data from data file such as electronegativity, atomic radius, etc.
        self.element_data = self._load_data()

        # Read file and return number of atoms, coordinates and elements
        n_atoms, coordinates, elements = self.read_file()

        nodes = list(range(n_atoms))

        for node, coordinate, element in zip(nodes, coordinates, elements):

            # Get specific element data for each atom from tabulated element_data
            element_data = self._get_data_for_element(element)

            # Add node to graph
            self.add_node(node, coordinates=coordinate,
                          elements=element, visible=True, **element_data)

    def from_coordinates(self, coordinates: np.ndarray, elements: np.ndarray) -> None:
        """
        Constructs a MolGraph object from coordinates given by np.ndarray and elements given by np.ndarray.

        Args:
            coordinates (np.ndarray): Coordinates of the molecule of shape (n_atoms, 3).
            elements (np.ndarray): Elements of the molecule of shape (n_atoms,).

        Raises:
            ValueError: If coordinates and elements do not have the same length.
        """

        if len(coordinates) != len(elements):

            raise ValueError("geometry and atoms must have the same length")

        nodes = list(range(len(coordinates)))

        # Load tabulated chemical data from data file such as electronegativity, atomic radius, etc.
        self.element_data = self._load_data()

        for node, coordinate, element in zip(nodes, coordinates, elements):

            # Get specific element data for each atom from tabulated element_data
            element_data = self._get_data_for_element(element)

            # Add node to graph
            self.add_node(node, coordinates=coordinate,
                          elements=element, visible=True, **element_data)

    def return_n_atoms(self, include_all=False) -> int:
        """
        Returns the number of atoms in the molecule.

        Args:
            include_all (bool, optional): If all nodes and not only the visible nodes should be considered. The default value is False

        Returns:
            int: _description_
        """

        if include_all:

            return self.number_of_nodes()

        return len([node for node, data in self.nodes(data=True) if data.get("visible") == True])

    def return_cn_matrix(self, include_all=False) -> np.ndarray:
        """
        Returns the coordination matrix/adjacency matrix of the molecule.

        Args:
            include_all (bool, optional): If all nodes and not only the visible nodes should be considered. The default value is False

        Returns:
            np.ndarray: Coordination matrix/adjacency matrix of the molecule.
        """

        if include_all:

            return nx.to_numpy_array(self)
        else:

            nodes = self.return_visible_nodes()

            cn_matrix = np.zeros((len(nodes), len(nodes)))

            for node1, node2, data in self.edges(data=True):

                if data["visible"] == True:

                    if (node1 in nodes) and (node2 in nodes):

                        cn_matrix[nodes.index(node1), nodes.index(node2)] = 1

                        cn_matrix[nodes.index(node2), nodes.index(node1)] = 1

            return cn_matrix

    def get_degree(self, include_all=False) -> np.ndarray:
        """
        Returns the degree of each node in the molecule.

        Args:
            include_all (bool, optional): If all nodes and not only the visible nodes should be considered. The default value is False

        Returns:
            np.ndarray: Degree of each node in the molecule.
        """

        if include_all:

            return np.array([degree for node, degree in self.degree()])

        subgraph = nx.Graph()

        subgraph.add_nodes_from(self.return_visible_nodes())

        subgraph.add_edges_from(self.return_visible_edges(nodes_visible=True))

        return np.array([degree for node, degree in subgraph.degree()])

    def connected_components(self) -> list:
        """
        Returns the connected nodes of the molecule.

        Returns:
            list: List of connected nodes.

        """

        visible_edges = self.return_visible_edges(nodes_visible=True)

        visible_nodes = self.return_visible_nodes()

        subgraph = nx.Graph()

        subgraph.add_nodes_from(self.return_visible_nodes())

        subgraph.add_edges_from(visible_edges)

        connected_components = list(
            [list(fragment) for fragment in nx.connected_components(subgraph)])
        
        connected_components_data = []

        # Sort connected components by size and priority to account for pseudochirality later.
        for fragment in connected_components:

            adjacent_nodes = self.return_adjacent_nodes(core_nodes=fragment)

            self.set_nodes_visible(visible_nodes=fragment+adjacent_nodes)

            try:

                priorities = rankdata(self.return_node_data(attribute="priorities"), method="min")

                sum_priorities = np.sum(priorities)

            except TypeError:

                return connected_components

            n_atoms_in_fragment = len(fragment) + len(adjacent_nodes)

            self.set_nodes_visible(visible_nodes=visible_nodes)

            if n_atoms_in_fragment > 2:

                connected_components_data.append((fragment, n_atoms_in_fragment, sum_priorities))

        sorted_components = sorted(
            connected_components_data, key=lambda x: (x[1], x[2]), reverse=True)

        return [fragment[0] for fragment in sorted_components]

    def rigid_fragmentation(self, include_all=False) -> None:
        """

        Fragmentates the molecule into rigid parts by considering cycles and multiple bonds as rigid fragments.

        Args:

            include_all (bool, optional): If all nodes and not only the visible nodes should be considered. The default value is False

        """

        if include_all:

            self.set_nodes_visible(include_all=True)

        self.set_edges_unvisible(
            attributes=["rigid", "cycle_id"], values=[False, None])
        
        self.set_edges_unvisible(
            attributes=["stick"], values=[True], default_all_visible=False)

        fragments = self.connected_components()

        self.set_edges_visible(include_all=True)

        fragment_id = 0

        for fragment in fragments:
            
            self.set_nodes_visible(visible_nodes=fragment)

            self.add_node_data(attribute="fragment_id", new_data=[
                               fragment_id]*len(fragment))

            fragment_id += 1

        self.set_nodes_visible(include_all=True)
