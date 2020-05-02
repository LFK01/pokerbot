import os
import logging
import sys

from working_tools import input_file_parser, tree_visualizer
from working_tools.abstraction_generator import abstraction_manager
from working_tools.game_solver.external_sampling import normalize_table
from working_tools.game_solver.solver import solver

FILE_NAME = 'kuhn.txt'

if __name__ == '__main__':

    logging.basicConfig()

    pokerbot_logger = logging.getLogger('pokerbot')
    pokerbot_logger.setLevel(logging.WARNING)

    # tree will be the root node of the entire tree
    # parse the file to compute the tree structure
    tree = input_file_parser.parse_tree(os.path.join(os.getcwd(), 'text_files', 'inputs', FILE_NAME))

    # info_sets will contain the complete infostructure of the game
    # parse_infoset reads the file and returns the infostructure
    info_sets = input_file_parser.parse_infoset(os.path.join(os.getcwd(), 'text_files', 'inputs', FILE_NAME), tree)

    # parse again
    # compressed_tree = input_file_parser.parse_tree(os.path.join(os.getcwd(), 'text_files', 'inputs', FILE_NAME))

    # compressed_infosets = input_file_parser.parse_infoset(os.path.join(os.getcwd(), 'text_files', 'inputs', FILE_NAME),
    #                                                       compressed_tree)

    # visualize the game tree
    # original = sys.stdout
    # sys.stdout = open('tree.txt', 'w')
    # tree_visualizer.visualize_game_tree(tree, 0)
    # sys.stdout = original
    # visualize the infostructure of the tree
    # tree_visualizer.visualize_info_structure(tree, info_sets)

    abstraction_set = abstraction_manager.create_abstraction(tree, '1')
    abstraction_set.extend(abstraction_manager.create_abstraction(tree, '2'))
    # tree_visualizer.visualize_game_tree(compressed_tree, 0)

    print('INITIAL NUMBER OF INFOSETS:', end=' ')
    print(info_sets.get_number_of_infosets())
    print('FINAL NUMBER OF INFOSETS:', end=' ')
    print(len(abstraction_set))
    # original = sys.stdout
    # sys.stdout = open('redirect.txt', 'w')
    print('+++ABSTRACTION SET+++')
    # visualization of the new infostructure
    for infoset in abstraction_set:
        # for infoset_list in abstraction_level:
        print(infoset.name)
        # for node in infoset.info_nodes.values():
        #     print(node.history, end=' ')
        print('-----')
    print('++++++++++++++++++++++')
    # sys.stdout = original

    abs_set_2 = []
    for infoset in info_sets.info_sets1:
        abs_set_2.append(infoset)
    for infoset in info_sets.info_sets2:
        abs_set_2.append(infoset)
    utilities, strategy_table = solver(abs_set_2, 100000, 2, tree)
    strategy_table = normalize_table(strategy_table)
    print(utilities)
    print(strategy_table)
