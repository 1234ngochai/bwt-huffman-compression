import sys

class Node:
    def __init__(self, start=None, end=None, suffix_index=None):
        # Initialize a list with slots for each character in the ASCII range [36, 126]
        self.children = [None] * (126 - 36 + 1) ## for alphabetical order
        self.start = start  # Start index of the edge label leading to this node
        self.end = end  # End index of the edge label leading to this node
        self.suffix_index = suffix_index  # Only set for leaf nodes
        self.suffix_link = None  # Suffix link to another node

    def is_leaf(self):
        return all(child is None for child in self.children)

    def add_child(self, char, node):
        self.children[ord(char) - 36] = node

    def get_child(self, char):
        return self.children[ord(char) - 36]

    def iter_children(self):
        for index, child in enumerate(self.children):
            if child is not None:
                yield chr(index + 36), child

def extend_suffix_tree(root, s, phase_index, suffix_start,activeNode, last_internal_node=None):

    ## this activeNode is my attemp to do active node but wasn't successfull
    ## I have another version that tried to implement trick 2, but it was
    ## not able to run due some bug




    # if activeNode:
    #    
    #     current = activeNode.suffix_link
    # 
    #     if current.start:
    #         index = current.start
    #     else:
    #         index = suffix_start
    # else:
    #     current = root
    #     index = suffix_start

    ## set the current to root
    current = root
    ## set the extension
    index = suffix_start

    #extension -> phase index 
    while index <= phase_index:
        # grab the current char to compare
        char = s[index]
        # check the first char in the current children to decide if we want to traverse or not
        child = current.get_child(char)
        # set the active node to the current node that we are on
        activeNode = current
        # if their isn't a match with the current char
        if child is None:
            # create a leaf, and this leaf will have the end bound at the last character, followed trick 4, so we can removed rules 1
            # no need to extend any leaf anymore
            new_leaf = Node(index, len(s) - 1, suffix_start) 
            current.add_child(char, new_leaf)
            # active node set to current node
            activeNode = current
            # if we see an internal node before this
            if last_internal_node:
                # then make the last internal node suffix link pointed to this current
                last_internal_node.suffix_link = current
                last_internal_node = None
                
            break


        else:
            # if we are traversing this edges, then set the current node as active node
            activeNode = current
            current = current.get_child(char)
            # calculate the edge length, for let us know what is the end of this edges
            edge_length = current.end - current.start + 1
            position = 0

            # while we still in the bound of the edges and the phase
            while position < edge_length and index <= phase_index:
                # if we saw a mismatch while traversing this, split
                if s[current.start + position] != s[index]:
                    split_point = current.start + position #split point = missmatch position
                    # this will be the rest of the edges
                    existing_continuation = Node(split_point, current.end, current.suffix_index)
                    # will inherit all the children from it parent node
                    existing_continuation.children = current.children
                    #make new suffix node
                    new_suffix_node = Node(index, len(s) - 1, suffix_start)

                    #reset the current endbound to the missmatch position
                    current.end = split_point - 1
                    current.children = [None] * (126 - 36 + 1)
                    # add 2 newly created children
                    current.add_child(s[split_point], existing_continuation)
                    current.add_child(s[index], new_suffix_node)

                    # The current node is now an internal node and does not represent a specific suffix
                    current.suffix_index = None

                    # if we see an internal node before this
                    if last_internal_node:
                        # then make the last internal node suffix link pointed to this current
                        last_internal_node.suffix_link = current

                    #keep track of this current node, as it have become the new internal node
                    last_internal_node = current

                    return root, last_internal_node, False, index,activeNode
                
                #if we traversed an edges, rule 3
                elif index == phase_index:
                    # if their an pending internal node, point it to this current node
                    if last_internal_node :
                        last_internal_node.suffix_link = activeNode
                        last_internal_node = None
                        #also trick 3, return right when we meet rule tree
                        return root, last_internal_node, True,suffix_start-1,activeNode ## suffix_start-1 indicating the current lastj
                    
                position += 1
                index += 1


    return root, last_internal_node, False, index,activeNode

## this is my attemp to do the skip count, I undo quite a bit of my word since I was panic when I 
## saw a bug in my code, so I can only show you this bit
def skip_count_traverse(current, s, start_index, remainder):
    index = start_index
    total_skipped = 0

    while total_skipped < remainder and current is not None:
        # Find the child node that matches the next character in the substring
        child_char = s[index]
        child = current.get_child(child_char)
        
        if child is None:
            # No further path matches the substring, stop traversal
            break

        # Calculate the length of the edge to this child node
        edge_length = child.end - child.start + 1

        if total_skipped + edge_length <= remainder:
            # The remainder is sufficient to traverse the entire edge to the child
            total_skipped += edge_length
            index += edge_length
            current = child  # Update the current node to this child
        else:
            # The remainder is not enough to traverse the entire edge; stop at a position within the edge
            needed_length = remainder - total_skipped
            index += needed_length
            total_skipped += needed_length
            return current, index  # Return the current node and the index where the traversal stopped

    # Return the current node (which might be a child node where the path ends) and the index
    return current, index


def build_suffix_tree(s):
    root = Node()
    root.suffix_link = root ## pointing the root's suffix link to itself
    last_internal_node = None
    activeNode = None  # Initialize activeNode
    start_index = 0  # Start index for the phases
    index = 0

    for i in range(len(s)):
        phase_ended_early = False
        j = start_index  # Start from the index where the lastj phase ended early or 0
        while j <= i:
            root, last_internal_node, phase_ended_early, index,activeNode = extend_suffix_tree(root, s, i, j, activeNode, last_internal_node)
            if phase_ended_early: ## if end early
                start_index = index ## update the last j
                break 
            j += 1  # Otherwise, continue with the next suffix start

    return root


## helper function to help me visuallize this 
# def print_suffix_tree(node, s, depth=0):
#     indent = ' ' * (depth * 2)

#     if node.start is not None and node.end is not None:
#         label = s[node.start:node.end + 1]
#     else:
#         label = "[Root node]" 

#     if node.suffix_link:
#         link_label = s[node.suffix_link.start:node.suffix_link.end + 1] if node.suffix_link.start is not None else "Root"
#         link_label = f"{link_label} (from {node.suffix_link.start} to {node.suffix_link.end})"
#     else:
#         link_label = "None"

#     is_leaf = "Leaf" if node.is_leaf() else "Internal"
#     print(f"{indent}{label} [{is_leaf}, Suffix Link -> {link_label}]")

#     for char_index, child in enumerate(node.children):
#         if child:
#             print_suffix_tree(child, s, depth + 1)


def collect_suffix_array(node, s, suffix_array=None):
    ## a DFS through the tree
    if suffix_array is None:
        suffix_array = []
    ## if we reach a leaf, append it suffix index, since the tree was make
    ## in alphabetical order, so we can just append the index indicating the suffix, and it will be sorted
    if node.is_leaf():
        suffix_array.append(node.suffix_index)
    # recursive call
    for _, child in node.iter_children():
        collect_suffix_array(child, s, suffix_array)
    return suffix_array


def read_file(filename):
    with open(filename, 'r') as file:
        return file.read().strip()

def write_results(filename, results):
    with open(filename, 'w') as file:
        for result in results:
            file.write(f"{result}\n")

def main(string_filename, positions_filename):
    s = read_file(string_filename)
    root = build_suffix_tree(s)
    suffix_array = collect_suffix_array(root,s)


    ## we have the suffix array and the input, map them together.
    positions = list(map(int, read_file(positions_filename).split()))
    position_ranks = {suffix_array[i]: i + 1 for i in range(len(suffix_array))}  # Create a map of suffix start to rank

    # adjusting for based 1
    ranks = [position_ranks[pos - 1] for pos in positions]  # Adjust for 1-based index
    write_results("output_q1.txt", ranks)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python q1.py <stringFileName> <positionsFileName>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])

