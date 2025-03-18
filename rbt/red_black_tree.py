class Node:
    """Represents a single node in the Red-Black Tree."""
    
    RED = "RED"
    BLACK = "BLACK"

    def __init__(self, key, color=RED):
        self.key = key
        self.color = color  # Nodes are initially RED
        self.left = None
        self.right = None
        self.parent = None


class RedBlackTree:
    """Red-Black Tree with insert, search, delete, and serialization."""

    def __init__(self):
        self.NIL = Node("NIL", Node.BLACK)  # Sentinel NIL node (Black)
        self.root = self.NIL

    def insert(self, key):
        """Inserts a node while maintaining Red-Black properties."""
        new_node = Node(key)
        new_node.left = self.NIL
        new_node.right = self.NIL
        parent = None
        current = self.root

        while current != self.NIL:
            parent = current
            if new_node.key < current.key:
                current = current.left
            else:
                current = current.right

        new_node.parent = parent
        if parent is None:
            self.root = new_node
        elif new_node.key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node

        new_node.color = Node.RED
        self._fix_insert(new_node)

    def find(self, key):
        current = self.root
        while current != self.NIL:
            if key == current.key:
                return current
            elif key < current.key:
                current = current.left
            else:
                current = current.right
        return None

    def delete(self, key):
        node = self.find(key)
        if node is None:
            return

        original_color = node.color
        if node.left == self.NIL:
            replacement = node.right
            self._transplant(node, node.right)
        elif node.right == self.NIL:
            replacement = node.left
            self._transplant(node, node.left)
        else:
            successor = self._minimum(node.right)
            original_color = successor.color
            replacement = successor.right
            if successor.parent == node:
                replacement.parent = successor
            else:
                self._transplant(successor, successor.right)
                successor.right = node.right
                successor.right.parent = successor

            self._transplant(node, successor)
            successor.left = node.left
            successor.left.parent = successor
            successor.color = node.color

        if original_color == Node.BLACK:
            self._fix_delete(replacement)

    def __str__(self):
        """Serializes the tree to a comma-separated string."""
        return self._serialize(self.root)

    def _serialize(self, node):
        """Helper function to serialize the tree into a string using commas."""
        if node == self.NIL:
            return "NIL"
        left_str = self._serialize(node.left)
        right_str = self._serialize(node.right)
        return f"{node.key}({node.color}),{left_str},{right_str}"

    def _fix_insert(self, node):
        """Fixes Red-Black Tree violations after insertion."""
        while node.parent and node.parent.color == Node.RED:
            grandparent = node.parent.parent
            if node.parent == grandparent.left:
                uncle = grandparent.right
                if uncle.color == Node.RED:  # Case 1: Uncle is RED
                    node.parent.color = Node.BLACK
                    uncle.color = Node.BLACK
                    grandparent.color = Node.RED
                    node = grandparent
                else:
                    if node == node.parent.right:  # Case 2: Left-Right Case
                        node = node.parent
                        self._left_rotate(node)
                    # Case 3: Left-Left Case
                    node.parent.color = Node.BLACK
                    grandparent.color = Node.RED
                    self._right_rotate(grandparent)
            else:
                uncle = grandparent.left
                if uncle.color == Node.RED:  # Case 1: Uncle is RED
                    node.parent.color = Node.BLACK
                    uncle.color = Node.BLACK
                    grandparent.color = Node.RED
                    node = grandparent
                else:
                    if node == node.parent.left:  # Case 2: Right-Left Case
                        node = node.parent
                        self._right_rotate(node)
                    # Case 3: Right-Right Case
                    node.parent.color = Node.BLACK
                    grandparent.color = Node.RED
                    self._left_rotate(grandparent)

        self.root.color = Node.BLACK

    def _left_rotate(self, node):
        """Performs a left rotation around a given node."""
        right_child = node.right
        node.right = right_child.left
        if right_child.left != self.NIL:
            right_child.left.parent = node
        right_child.parent = node.parent
        if node.parent is None:
            self.root = right_child
        elif node == node.parent.left:
            node.parent.left = right_child
        else:
            node.parent.right = right_child
        right_child.left = node
        node.parent = right_child

    def _right_rotate(self, node):
        """Performs a right rotation around a given node."""
        left_child = node.left
        node.left = left_child.right
        if left_child.right != self.NIL:
            left_child.right.parent = node
        left_child.parent = node.parent
        if node.parent is None:
            self.root = left_child
        elif node == node.parent.right:
            node.parent.right = left_child
        else:
            node.parent.left = left_child
        left_child.right = node
        node.parent = left_child

    def _fix_delete(self, node):
        """Fixes Red-Black Tree violations after deletion."""
        while node != self.root and node.color == Node.BLACK:
            if node == node.parent.left:
                sibling = node.parent.right
                if sibling.color == Node.RED:
                    sibling.color = Node.BLACK
                    node.parent.color = Node.RED
                    self._left_rotate(node.parent)
                    sibling = node.parent.right
                if sibling.left.color == Node.BLACK and sibling.right.color == Node.BLACK:
                    sibling.color = Node.RED
                    node = node.parent
                else:
                    if sibling.right.color == Node.BLACK:
                        sibling.left.color = Node.BLACK
                        sibling.color = Node.RED
                        self._right_rotate(sibling)
                        sibling = node.parent.right
                    sibling.color = node.parent.color
                    node.parent.color = Node.BLACK
                    sibling.right.color = Node.BLACK
                    self._left_rotate(node.parent)
                    node = self.root
            else:
                sibling = node.parent.left
                if sibling.color == Node.RED:
                    sibling.color = Node.BLACK
                    node.parent.color = Node.RED
                    self._right_rotate(node.parent)
                    sibling = node.parent.left
                if sibling.left.color == Node.BLACK and sibling.right.color == Node.BLACK:
                    sibling.color = Node.RED
                    node = node.parent
                else:
                    if sibling.left.color == Node.BLACK:
                        sibling.right.color = Node.BLACK
                        sibling.color = Node.RED
                        self._left_rotate(sibling)
                        sibling = node.parent.left
                    sibling.color = node.parent.color
                    node.parent.color = Node.BLACK
                    sibling.left.color = Node.BLACK
                    self._right_rotate(node.parent)
                    node = self.root
        node.color = Node.BLACK

    def _transplant(self, old, new):
        """Replaces one subtree with another."""
        if old.parent is None:
            self.root = new
        elif old == old.parent.left:
            old.parent.left = new
        else:
            old.parent.right = new
        new.parent = old.parent

    def _minimum(self, node):
        """Finds the leftmost (smallest) node."""
        while node.left != self.NIL:
            node = node.left
        return node

    def height(self, node=None):
        """Calculate the height of the tree or subtree"""
        if node is None:
            node = self.root
        if node == self.NIL:
            return 0
        return 1 + max(self.height(node.left), self.height(node.right))

    def black_height(self, node=None):
        """Calculate the black height of the tree or subtree"""
        if node is None:
            node = self.root
        if node == self.NIL:
            return 1  # NIL nodes are BLACK
        
        left_height = self.black_height(node.left)
        right_height = self.black_height(node.right)
        
        # Verify that black heights match for a valid RB tree
        if left_height != right_height:
            print(f"Warning: Black height mismatch at node {node.key}")
        
        # Add 1 if this node is BLACK
        return left_height + (1 if node.color == Node.BLACK else 0)

    def validate(self):
        """Validate that the tree follows Red-Black properties"""
        if self.root == self.NIL:
            return True
        
        # Property 1: Every node is either red or black
        # (enforced by Node.RED and Node.BLACK constants)
        
        # Property 2: The root is black
        if self.root.color != Node.BLACK:
            print("Violation: Root is not black")
            return False
        
        # Check other properties with helper function
        return self._validate_node(self.root)

    def _validate_node(self, node):
        if node == self.NIL:
            return True
        
        # Property 3: Every NIL (leaf) is black
        # (enforced by NIL initialization)
        
        # Property 4: If a node is red, both its children are black
        if node.color == Node.RED:
            if node.left.color != Node.BLACK or node.right.color != Node.BLACK:
                print(f"Violation: Red node {node.key} has red child")
                return False
        
        # Property 5: For each node, all paths to descendants have the same black height
        left_black_height = self._count_black_height(node.left)
        right_black_height = self._count_black_height(node.right)
        if left_black_height != right_black_height:
            print(f"Violation: Black height mismatch at node {node.key}")
            return False
        
        # Recursively check children
        return self._validate_node(node.left) and self._validate_node(node.right)

    def _count_black_height(self, node):
        """Count black nodes from this node to a leaf"""
        if node == self.NIL:
            return 1  # NIL nodes are BLACK
        
        # Get the child with the minimum height
        height = min(self._count_black_height(node.left), self._count_black_height(node.right))
        return height + (1 if node.color == Node.BLACK else 0)