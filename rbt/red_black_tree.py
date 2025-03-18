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
        self.NIL = Node(None, Node.BLACK)  # Sentinel NIL node (Black)
        self.NIL.left = self.NIL
        self.NIL.right = self.NIL
        self.NIL.parent = None
        self.root = self.NIL

    def insert(self, key):
        """Inserts a node while maintaining Red-Black properties."""
        # Step 1: Standard BST insert
        new_node = Node(key)
        new_node.left = self.NIL
        new_node.right = self.NIL
        
        y = None
        x = self.root
        
        # Find the position to insert the new node
        while x != self.NIL:
            y = x
            if new_node.key < x.key:
                x = x.left
            else:
                x = x.right
        
        # Set the parent of the new node
        new_node.parent = y
        
        # Insert the new node into the tree
        if y is None:  # Tree was empty
            self.root = new_node
        elif new_node.key < y.key:
            y.left = new_node
        else:
            y.right = new_node
        
        # Step 2: Fix Red-Black properties
        self._fix_insert(new_node)
    
    def find(self, key):
        """Find a node with the given key in the tree."""
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
        """Delete a node with the given key from the tree."""
        # Find the node to delete
        z = self.find(key)
        if z is None:
            return  # Key not found
        
        y = z  # y will be the node to be removed from the tree
        y_original_color = y.color
        
        # Case 1: z has no left child
        if z.left == self.NIL:
            x = z.right
            self._transplant(z, z.right)
        # Case 2: z has no right child
        elif z.right == self.NIL:
            x = z.left
            self._transplant(z, z.left)
        # Case 3: z has both children
        else:
            y = self._minimum(z.right)  # Find successor
            y_original_color = y.color
            x = y.right
            
            if y.parent == z:  # y is a direct child of z
                x.parent = y
            else:
                self._transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            
            self._transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        
        # Fix Red-Black properties if we removed a black node
        if y_original_color == Node.BLACK:
            self._fix_delete(x)
    
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
    
    def _left_rotate(self, x):
        """Perform a left rotation at node x."""
        y = x.right  # Set y
        
        # Turn y's left subtree into x's right subtree
        x.right = y.left
        if y.left != self.NIL:
            y.left.parent = x
        
        # Link x's parent to y
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        
        # Put x on y's left
        y.left = x
        x.parent = y
    
    def _right_rotate(self, x):
        """Perform a right rotation at node x."""
        y = x.left  # Set y
        
        # Turn y's right subtree into x's left subtree
        x.left = y.right
        if y.right != self.NIL:
            y.right.parent = x
        
        # Link x's parent to y
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        
        # Put x on y's right
        y.right = x
        x.parent = y
    
    def _fix_insert(self, k):
        """Fix Red-Black properties after insertion."""
        # While we have a red-red conflict
        while k != self.root and k.parent and k.parent.color == Node.RED:
            if k.parent == k.parent.parent.right:  # Parent is right child of grandparent
                u = k.parent.parent.left  # Uncle
                
                if u.color == Node.RED:
                    # Case 1: Uncle is red - recolor
                    u.color = Node.BLACK
                    k.parent.color = Node.BLACK
                    k.parent.parent.color = Node.RED
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        # Case 2: Uncle is black, k is left child - right rotate parent
                        k = k.parent
                        self._right_rotate(k)
                    
                    # Case 3: Uncle is black, k is right child - left rotate grandparent
                    k.parent.color = Node.BLACK
                    k.parent.parent.color = Node.RED
                    self._left_rotate(k.parent.parent)
            else:  # Parent is left child of grandparent
                u = k.parent.parent.right  # Uncle
                
                if u.color == Node.RED:
                    # Case 1: Uncle is red - recolor
                    u.color = Node.BLACK
                    k.parent.color = Node.BLACK
                    k.parent.parent.color = Node.RED
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        # Case 2: Uncle is black, k is right child - left rotate parent
                        k = k.parent
                        self._left_rotate(k)
                    
                    # Case 3: Uncle is black, k is left child - right rotate grandparent
                    k.parent.color = Node.BLACK
                    k.parent.parent.color = Node.RED
                    self._right_rotate(k.parent.parent)
        
        # Ensure root is black
        self.root.color = Node.BLACK
    
    def _fix_delete(self, x):
        """Fix Red-Black properties after deletion."""
        while x != self.root and x.color == Node.BLACK:
            if x == x.parent.left:  # x is left child
                w = x.parent.right  # Sibling
                
                if w.color == Node.RED:
                    # Case 1: Sibling is red
                    w.color = Node.BLACK
                    x.parent.color = Node.RED
                    self._left_rotate(x.parent)
                    w = x.parent.right
                
                if w.left.color == Node.BLACK and w.right.color == Node.BLACK:
                    # Case 2: Sibling is black, both of sibling's children are black
                    w.color = Node.RED
                    x = x.parent
                else:
                    if w.right.color == Node.BLACK:
                        # Case 3: Sibling is black, sibling's left child is red, right child is black
                        w.left.color = Node.BLACK
                        w.color = Node.RED
                        self._right_rotate(w)
                        w = x.parent.right
                    
                    # Case 4: Sibling is black, sibling's right child is red
                    w.color = x.parent.color
                    x.parent.color = Node.BLACK
                    w.right.color = Node.BLACK
                    self._left_rotate(x.parent)
                    x = self.root  # Exit the loop
            else:  # x is right child (mirror cases)
                w = x.parent.left  # Sibling
                
                if w.color == Node.RED:
                    # Case 1: Sibling is red
                    w.color = Node.BLACK
                    x.parent.color = Node.RED
                    self._right_rotate(x.parent)
                    w = x.parent.left
                
                if w.right.color == Node.BLACK and w.left.color == Node.BLACK:
                    # Case 2: Sibling is black, both of sibling's children are black
                    w.color = Node.RED
                    x = x.parent
                else:
                    if w.left.color == Node.BLACK:
                        # Case 3: Sibling is black, sibling's right child is red, left child is black
                        w.right.color = Node.BLACK
                        w.color = Node.RED
                        self._left_rotate(w)
                        w = x.parent.left
                    
                    # Case 4: Sibling is black, sibling's left child is red
                    w.color = x.parent.color
                    x.parent.color = Node.BLACK
                    w.left.color = Node.BLACK
                    self._right_rotate(x.parent)
                    x = self.root  # Exit the loop
        
        # Ensure x is black
        x.color = Node.BLACK
    
    def _transplant(self, u, v):
        """Replace subtree rooted at u with subtree rooted at v."""
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent
    
    def _minimum(self, node):
        """Find the node with the minimum key in the subtree rooted at node."""
        current = node
        while current.left != self.NIL:
            current = current.left
        return current
    
    # Additional methods for validation and debugging
    
    def height(self, node=None):
        """Calculate the height of the tree or subtree."""
        if node is None:
            node = self.root
        if node == self.NIL:
            return 0
        return 1 + max(self.height(node.left), self.height(node.right))
    
    def black_height(self, node=None):
        """Calculate the black height of the tree or subtree."""
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
        """Validate that the tree follows Red-Black properties."""
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
        """Count black nodes from this node to a leaf."""
        if node == self.NIL:
            return 1  # NIL nodes are BLACK
        
        # Get the child with the minimum height
        height = min(self._count_black_height(node.left), self._count_black_height(node.right))
        return height + (1 if node.color == Node.BLACK else 0)