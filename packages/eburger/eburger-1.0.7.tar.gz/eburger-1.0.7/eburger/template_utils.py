import copy
import re
from typing import Union


def join_lists_unique(list1: list, list2: list) -> list:
    """
    Join two lists of dictionaries without duplicates, based on the 'id' key of the dictionaries.

    :param list1: First list of dictionaries.
    :param list2: Second list of dictionaries.
    :return: A list of dictionaries without duplicates.
    """
    # Create a set to track unique ids
    seen_ids = set()
    combined_list = []

    # Function to add dictionaries to the combined list if their id is not seen
    def add_unique_dicts_from_list(lst):
        for d in lst:
            # Check if the dictionary has an 'id' key and it's not seen before
            if "id" in d and d["id"] not in seen_ids:
                combined_list.append(d)
                seen_ids.add(d["id"])

    # Add unique dictionaries from both lists
    add_unique_dicts_from_list(list1)
    add_unique_dicts_from_list(list2)

    return combined_list


def is_entry_unique(results: list, file_path: str, lines: str) -> bool:
    """
    Checks if an entry with the specified file_path and lines already exists in the results.

    :param results: List of dictionaries containing the current results.
    :param file_path: The file path to be checked.
    :param lines: The lines to be checked.
    :return: True if no entry with the same file_path and lines exists, False otherwise.
    """
    return not any(
        result["file"] == file_path and result["lines"] == lines for result in results
    )


def get_nodes_by_types(
    node: dict,
    node_types: Union[str, list],
    filter_key: str = None,
    filter_value: str = None,
) -> list:
    """
    Finds nodes of specific types within the given node or AST.

    :param node: The node or AST to search.
    :param node_types: The type(s) of nodes to find.
    :param filter_key: A JSON key to find and filter by.
    :param filter_value: filter_key value to search.
    :return: A list of nodes of the specified types.
    """

    if isinstance(node_types, str):
        node_types = [node_types]

    def search_nodes(current_node, result):
        if isinstance(current_node, dict):
            if current_node.get("nodeType") in node_types:
                result.append(current_node)
            for value in current_node.values():
                if isinstance(value, (dict, list)):
                    search_nodes(value, result)
        elif isinstance(current_node, list):
            for item in current_node:
                search_nodes(item, result)

    results = []
    search_nodes(node, results)

    # Only after results were colelcted, apply filter if filter_key and filter_value are provided
    if filter_key is not None:
        results_filtered = []
        for result in results:
            if filter_key is None or result.get(filter_key) == filter_value:
                results_filtered.append(result)
        results = results_filtered

    return results


def get_nodes_by_signature(node: dict, pattern: str, use_regex: bool = False):
    """
    Searches for nodes with a specific typeString within the given node or AST.

    :param node: The node or AST to search.
    :param pattern: The typeString to search for (regex).
    :param use_regex: Whether or not to use regex for the search.
    :return: A list of nodes that have the specified typeString.
    """
    matching_nodes = []
    if use_regex:
        compiled_pattern = re.compile(pattern)

    def search_nodes(current_node):
        if isinstance(current_node, dict):
            # Check if the current node matches the typeString
            node_type_string = current_node.get("typeDescriptions", {}).get(
                "typeString"
            )
            if node_type_string:
                if use_regex:
                    if compiled_pattern.search(node_type_string):
                        matching_nodes.append(current_node)
                else:
                    if pattern == node_type_string:
                        matching_nodes.append(current_node)
            # Recursively search in child nodes
            for value in current_node.values():
                if isinstance(value, (dict, list)):
                    search_nodes(value)
        elif isinstance(current_node, list):
            for item in current_node:
                search_nodes(item)

    search_nodes(node)
    return matching_nodes


def find_node_ids_first_parent_of_type(
    ast: dict, node_id: int, parent_type: dict
) -> Union[dict, None]:
    """
    Finds the first parent of a specified type for a given node ID in the AST.

    :param ast: The AST to search.
    :param node_id: The ID of the node whose parent is to be found.
    :param parent_type: The nodeType of the parent node to find.
    :return: The first parent node of the specified type, or None if not found.
    """

    def search_node(current_node, target_id, parent_node=None):
        if isinstance(current_node, dict):
            # Check if the current node is the target
            if current_node.get("id") == target_id:
                return parent_node
            # Iterate over child nodes
            for key, value in current_node.items():
                if isinstance(value, (list, dict)):
                    result = search_node(
                        value,
                        target_id,
                        (
                            current_node
                            if current_node.get("nodeType") == parent_type
                            else parent_node
                        ),
                    )
                    if result:
                        return result
        elif isinstance(current_node, list):
            for item in current_node:
                if isinstance(item, (list, dict)):
                    result = search_node(item, target_id, parent_node)
                    if result:
                        return result
        return None

    return search_node(ast, node_id)


def function_def_has_following_check_statements(
    function_def: dict, id_key: str
) -> bool:
    """
    Verifies if there are nodes after the given node_id that do some sort of validations.

    :param function_def: FunctionDefinition node to analyze
    :param id_key: String representing the JSON key to search the node within the statements as.
    :return: A boolean indicating if a check was found or not.
    """
    if function_def.get("nodeType") != "FunctionDefinition":
        return False

    statements = function_def.get("body", {}).get("statements", [])
    check_started = False

    for statement in statements:
        # If we have already started checking and found a validation, return True
        if check_started:
            # Flatten expression statements to their core components
            if statement.get("nodeType") == "ExpressionStatement":
                statement = statement.get("expression")

            # Check for require statements
            require_stmts = get_nodes_by_types(
                statement, "Identifier", filter_key="name", filter_value="require"
            )
            if require_stmts:
                return True

            # Check for direct reverts
            revert_stmts = get_nodes_by_types(
                statement, "Identifier", filter_key="name", filter_value="revert"
            )

            if revert_stmts:
                return True

        # If we find the target node, start the check
        if statement.get(id_key) == function_def.get(id_key):
            check_started = True

    # If we go through all statements following the target node without finding a validation, return False
    return False


def deep_clone_node(node: dict):
    """
    Deep clone an AST node for template level manipulations.

    :param node: AST Node to clone.
    """
    return copy.deepcopy(node)
