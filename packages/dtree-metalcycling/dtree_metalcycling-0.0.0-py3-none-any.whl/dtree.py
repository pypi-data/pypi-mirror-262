"""
Linux 'tree' but for Python
"""

# %% Modules

from colorama import Fore

# %% Global variables

BRANCH    = "├── "
SEPARATOR = "│   "
CLOSING   = "└── "
SPACING   = "    "
TEMP = None

# %% Modules

def dtree(dictionary, node_name = None, max_depth = None, print_datatypes = True, depth = 0, fill = ""):
    """
    Prints the tree representation of a dictionary and its children

    Input parameters:
    - dictionary <dict> (needed): Dictionary to be used to create the tree
    - node_name <str> (optional): Name of the dictionary to be used as the root node
    - max_depth <int> (optional): Maximum depth of the tree to be printed (e.g., 'max_depth = 0' only prints the root, 'max_depth = 1' prints the root and its immediate children)
    - print_datatypes <bool> (optional): Print the datatype of the leaf nodes in the tree (i.e., nodes at 'max_depth' are considered leaf nodes) and the datatype of the dictionary keys
    """

    # Make sure the inputs are valid

    assert isinstance(dictionary, dict), "Argument passed MUST be a dictionary"

    if max_depth:
        assert max_depth >= 0, "Argument must be greater or equal to zero"

    # If 'max_depth = 0', return the name of the root node, if no name is given it doesn't print anything

    if isinstance(max_depth, int) and max_depth == 0:
        if node_name:
            if print_datatypes:
                print("%s%s:%s %s<dict>%s" % (Fore.GREEN, node_name, Fore.WHITE, Fore.RED, Fore.WHITE))
            else:
                print("%s%s%s" % (Fore.GREEN, node_name, Fore.WHITE))
        else:
            return 

    # Initialize output

    global TEMP

    if TEMP == None:
        TEMP = Fore.WHITE

    # Print the name of the root node

    if depth == 0:
        if node_name:
            TEMP += Fore.GREEN + node_name + Fore.WHITE + "\n"

    # Return if maximum depth is reached

    if depth == max_depth:
        return 

    # Print children and recurse if necessary

    num_keys = len(dictionary)
    kdx = 0

    for key, value in dictionary.items():
        TEMP += fill

        if kdx == num_keys - 1:
            TEMP += CLOSING
        else:
            TEMP += BRANCH

        if isinstance(value, dict):
            if max_depth == None or depth < max_depth - 1:
                TEMP += "%s%s%s\n" % (Fore.GREEN, str(key), Fore.WHITE)
                dtree(value, node_name, max_depth, print_datatypes = print_datatypes, fill = fill + SEPARATOR if kdx < num_keys - 1 else fill + SPACING, depth = depth + 1)
            else:
                if print_datatypes:
                    TEMP += "%s%s:%s %s<dict>%s\n" % (Fore.GREEN, str(key), Fore.WHITE, Fore.RED, Fore.WHITE)
                else:
                    TEMP += "%s%s%s\n" % (Fore.GREEN, str(key), Fore.WHITE)

        else:
            if print_datatypes:
                TEMP += "%s%s:%s <%s>%s\n" % (Fore.BLUE, str(key), Fore.RED, type(value).__name__, Fore.WHITE)
            else:
                TEMP += "%s%s%s\n" % (Fore.BLUE, str(key), Fore.WHITE)

        kdx += 1

    if depth == 0:
        output = str(TEMP[:-1])
        TEMP = None
        print(output)
    else:
        return

# % Testing

if __name__ == "__main__":
    dictionary = { "A": { "B": { "C": 0, "D": "str" }, "E": None }, "F": { "G": 0.0, "H": set([]) } }
    dtree(dictionary, "with_name")

# %% End of script
