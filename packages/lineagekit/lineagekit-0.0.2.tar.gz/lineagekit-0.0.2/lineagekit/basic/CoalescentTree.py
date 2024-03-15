from __future__ import annotations
from GenGraph import *


class CoalescentTree(GenGraph):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_largest_clade_by_size(self) -> [int]:
        """!
        @brief Returns the largest clade in the tree by its total size.
        """
        clades = self.get_connected_components()
        largest_clade = max(clades, key=len)
        return largest_clade

    def get_largest_clade_by_probands(self) -> [int]:
        """!
        @brief Returns the largest clade in the tree by the number of probands.
        """
        probands = self.get_sink_vertices()

        def intersection_size(clade):
            return len(probands.intersection(clade))

        clades = self.get_connected_components()
        largest_clade = max(clades, key=lambda clade: intersection_size(clade))
        return largest_clade

    def get_root_for_clade(self, clade: [int]) -> int:
        """!
        @brief Returns the root of the given clade.
        """
        max_level_vertex = max(clade, key=lambda x: self.get_vertex_level(x))
        max_level = self.get_vertex_level(max_level_vertex)
        root_vertices = [x for x in clade if x in self.get_levels()[max_level]]
        if len(root_vertices) != 1:
            raise Exception("Invalid clade value")
        assert root_vertices[0] == max_level_vertex
        return root_vertices[0]

    def remove_unary_nodes(self):
        """!
        @brief Removes all the unary nodes in the coalescent tree and recalculates the levels of the coalescent tree.
        """
        for level in self.get_levels()[1:].__reversed__():
            intermediate_nodes = []
            for vertex in level:
                # Since the first level is omitted, all the vertices processed here must have children
                children = self.get_children(vertex)
                if len(children) == 1:
                    child = vertex
                    while len(children) == 1:
                        intermediate_nodes.append(child)
                        [child] = children
                        children = self.get_children(child)
                        if not children:
                            break
                    parents = self.get_parents(vertex)
                    if parents:
                        [parent] = parents
                        self.add_edge(child=child, parent=parent)
                        self.remove_edges_to_parents(child)
                        self.add_edge(child=child, parent=parent)
            self.remove_nodes_from(intermediate_nodes)
        assert not [x for x in self.nodes if len(self.get_children(x)) == 1]

    def write_levels(self, file, levels):
        """!
        @brief Writes the given levels to a file.
        @param file The file to which the levels will be written to.
        @param levels The levels to be saved.
        """
        for level in levels:
            for vertex in level:
                parents = self.get_parents(vertex)
                if parents:
                    [parent] = parents
                    file.write(f"{vertex} {parent}\n")

    @staticmethod
    def get_coalescent_tree(tree: Tree, probands: Iterable[int] = None) -> CoalescentTree:
        """
        @brief Utility function to get a coalescent tree from a tskit tree.
        @param tree The tskit tree.
        @param probands The probands for which the ascending genealogy should be calculated. Do not specify the value
        if all the vertices without children should be considered probands.
        @return The resulting tree.
        """
        genealogical_graph = GenGraph.get_graph_from_tree(tree, probands)
        return CoalescentTree(genealogical_graph)

    @staticmethod
    def get_coalescent_tree_from_file(filepath: str, probands: Iterable[int] = None) -> CoalescentTree:
        """!
        @brief Utility function to get a coalescent tree from a file.
        """
        pedigree: GenGraph = GenGraph.get_haploid_graph_from_file(filepath=filepath, probands=probands)
        result = CoalescentTree(pedigree=pedigree)
        return result
