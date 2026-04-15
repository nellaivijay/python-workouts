"""
Advanced Algorithms - Tree Traversals and Operations
"""

from typing import List, Optional, Callable
from collections import deque


class TreeNode:
    """Binary Tree Node"""
    
    def __init__(self, val: int = 0):
        self.val = val
        self.left: Optional[TreeNode] = None
        self.right: Optional[TreeNode] = None
    
    def __repr__(self):
        return f"TreeNode({self.val})"


class BinarySearchTree:
    """Binary Search Tree implementation"""
    
    def __init__(self):
        self.root: Optional[TreeNode] = None
    
    def insert(self, val: int):
        """Insert a value into the BST"""
        if not self.root:
            self.root = TreeNode(val)
            return
        
        self._insert_recursive(self.root, val)
    
    def _insert_recursive(self, node: TreeNode, val: int):
        """Helper method for recursive insertion"""
        if val < node.val:
            if node.left is None:
                node.left = TreeNode(val)
            else:
                self._insert_recursive(node.left, val)
        else:
            if node.right is None:
                node.right = TreeNode(val)
            else:
                self._insert_recursive(node.right, val)
    
    def search(self, val: int) -> bool:
        """Search for a value in the BST"""
        return self._search_recursive(self.root, val)
    
    def _search_recursive(self, node: Optional[TreeNode], val: int) -> bool:
        """Helper method for recursive search"""
        if not node:
            return False
        
        if val == node.val:
            return True
        elif val < node.val:
            return self._search_recursive(node.left, val)
        else:
            return self._search_recursive(node.right, val)
    
    def inorder_traversal(self) -> List[int]:
        """Inorder traversal (Left, Root, Right)"""
        result = []
        self._inorder_recursive(self.root, result)
        return result
    
    def _inorder_recursive(self, node: Optional[TreeNode], result: List[int]):
        """Helper method for inorder traversal"""
        if node:
            self._inorder_recursive(node.left, result)
            result.append(node.val)
            self._inorder_recursive(node.right, result)
    
    def preorder_traversal(self) -> List[int]:
        """Preorder traversal (Root, Left, Right)"""
        result = []
        self._preorder_recursive(self.root, result)
        return result
    
    def _preorder_recursive(self, node: Optional[TreeNode], result: List[int]):
        """Helper method for preorder traversal"""
        if node:
            result.append(node.val)
            self._preorder_recursive(node.left, result)
            self._preorder_recursive(node.right, result)
    
    def postorder_traversal(self) -> List[int]:
        """Postorder traversal (Left, Right, Root)"""
        result = []
        self._postorder_recursive(self.root, result)
        return result
    
    def _postorder_recursive(self, node: Optional[TreeNode], result: List[int]):
        """Helper method for postorder traversal"""
        if node:
            self._postorder_recursive(node.left, result)
            self._postorder_recursive(node.right, result)
            result.append(node.val)
    
    def level_order_traversal(self) -> List[List[int]]:
        """Level order traversal (BFS)"""
        if not self.root:
            return []
        
        result = []
        queue = deque([self.root])
        
        while queue:
            level_size = len(queue)
            current_level = []
            
            for _ in range(level_size):
                node = queue.popleft()
                current_level.append(node.val)
                
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            
            result.append(current_level)
        
        return result
    
    def find_min(self) -> Optional[int]:
        """Find minimum value in BST"""
        if not self.root:
            return None
        
        current = self.root
        while current.left:
            current = current.left
        return current.val
    
    def find_max(self) -> Optional[int]:
        """Find maximum value in BST"""
        if not self.root:
            return None
        
        current = self.root
        while current.right:
            current = current.right
        return current.val
    
    def get_height(self) -> int:
        """Get the height of the tree"""
        return self._get_height_recursive(self.root)
    
    def _get_height_recursive(self, node: Optional[TreeNode]) -> int:
        """Helper method to get height"""
        if not node:
            return 0
        
        left_height = self._get_height_recursive(node.left)
        right_height = self._get_height_recursive(node.right)
        
        return max(left_height, right_height) + 1
    
    def count_nodes(self) -> int:
        """Count total nodes in the tree"""
        return self._count_nodes_recursive(self.root)
    
    def _count_nodes_recursive(self, node: Optional[TreeNode]) -> int:
        """Helper method to count nodes"""
        if not node:
            return 0
        
        return (1 + 
                self._count_nodes_recursive(node.left) + 
                self._count_nodes_recursive(node.right))
    
    def is_valid_bst(self) -> bool:
        """Check if the tree is a valid BST"""
        return self._is_valid_bst_recursive(self.root, float('-inf'), float('inf'))
    
    def _is_valid_bst_recursive(self, node: Optional[TreeNode], 
                                min_val: float, max_val: float) -> bool:
        """Helper method to validate BST"""
        if not node:
            return True
        
        if node.val <= min_val or node.val >= max_val:
            return False
        
        return (self._is_valid_bst_recursive(node.left, min_val, node.val) and
                self._is_valid_bst_recursive(node.right, node.val, max_val))
    
    def delete(self, val: int):
        """Delete a value from the BST"""
        self.root = self._delete_recursive(self.root, val)
    
    def _delete_recursive(self, node: Optional[TreeNode], val: int) -> Optional[TreeNode]:
        """Helper method for deletion"""
        if not node:
            return None
        
        if val < node.val:
            node.left = self._delete_recursive(node.left, val)
        elif val > node.val:
            node.right = self._delete_recursive(node.right, val)
        else:
            # Node with only one child or no child
            if not node.left:
                return node.right
            if not node.right:
                return node.left
            
            # Node with two children: get inorder successor
            temp = self._find_min_node(node.right)
            node.val = temp.val
            node.right = self._delete_recursive(node.right, temp.val)
        
        return node
    
    def _find_min_node(self, node: TreeNode) -> TreeNode:
        """Find the node with minimum value"""
        current = node
        while current.left:
            current = current.left
        return current


def tree_traversals_iterative(root: TreeNode) -> dict:
    """All tree traversals using iterative approach"""
    result = {
        'inorder': [],
        'preorder': [],
        'postorder': []
    }
    
    # Inorder traversal (iterative)
    if root:
        stack = []
        current = root
        
        while current or stack:
            while current:
                stack.append(current)
                current = current.left
            
            current = stack.pop()
            result['inorder'].append(current.val)
            current = current.right
    
    # Preorder traversal (iterative)
    if root:
        stack = [root]
        
        while stack:
            node = stack.pop()
            result['preorder'].append(node.val)
            
            if node.right:
                stack.append(node.right)
            if node.left:
                stack.append(node.left)
    
    # Postorder traversal (iterative - using two stacks)
    if root:
        stack1 = [root]
        stack2 = []
        
        while stack1:
            node = stack1.pop()
            stack2.append(node)
            
            if node.left:
                stack1.append(node.left)
            if node.right:
                stack1.append(node.right)
        
        while stack2:
            result['postorder'].append(stack2.pop().val)
    
    return result


def create_sample_bst():
    """Create a sample Binary Search Tree"""
    bst = BinarySearchTree()
    values = [50, 30, 70, 20, 40, 60, 80]
    
    for val in values:
        bst.insert(val)
    
    return bst


def visualize_tree(node: TreeNode, level: int = 0, prefix: str = "Root: "):
    """Simple tree visualization"""
    if node is not None:
        print(" " * (level * 4) + prefix + str(node.val))
        if node.left is not None or node.right is not None:
            if node.left:
                visualize_tree(node.left, level + 1, "L--- ")
            else:
                print(" " * ((level + 1) * 4) + "L--- None")
            if node.right:
                visualize_tree(node.right, level + 1, "R--- ")
            else:
                print(" " * ((level + 1) * 4) + "R--- None")


def main():
    """Main function to demonstrate tree operations"""
    print("Tree Traversals and Operations")
    print("=" * 50)
    
    # Create sample BST
    print("\n1. Creating Binary Search Tree:")
    bst = create_sample_bst()
    print("   Inserted values: [50, 30, 70, 20, 40, 60, 80]")
    
    print("\n2. Tree Structure:")
    visualize_tree(bst.root)
    
    # Traversals
    print("\n3. Tree Traversals:")
    print(f"   Inorder (Left, Root, Right): {bst.inorder_traversal()}")
    print(f"   Preorder (Root, Left, Right): {bst.preorder_traversal()}")
    print(f"   Postorder (Left, Right, Root): {bst.postorder_traversal()}")
    print(f"   Level Order (BFS): {bst.level_order_traversal()}")
    
    # Iterative traversals
    print("\n4. Iterative Traversals:")
    iterative_result = tree_traversals_iterative(bst.root)
    print(f"   Inorder: {iterative_result['inorder']}")
    print(f"   Preorder: {iterative_result['preorder']}")
    print(f"   Postorder: {iterative_result['postorder']}")
    
    # Search operations
    print("\n5. Search Operations:")
    search_values = [40, 25, 70]
    for val in search_values:
        found = bst.search(val)
        print(f"   Search {val}: {'Found' if found else 'Not found'}")
    
    # Tree statistics
    print("\n6. Tree Statistics:")
    print(f"   Height: {bst.get_height()}")
    print(f"   Total nodes: {bst.count_nodes()}")
    print(f"   Minimum value: {bst.find_min()}")
    print(f"   Maximum value: {bst.find_max()}")
    
    # BST validation
    print("\n7. BST Validation:")
    print(f"   Is valid BST: {bst.is_valid_bst()}")
    
    # Delete operation
    print("\n8. Delete Operations:")
    print(f"   Tree before deletion: {bst.inorder_traversal()}")
    bst.delete(30)
    print(f"   After deleting 30: {bst.inorder_traversal()}")
    print(f"   New tree structure:")
    visualize_tree(bst.root)
    
    print("\n" + "=" * 50)
    print("Tree Algorithms Key Concepts:")
    print("✓ Inorder: Left -> Root -> Right (sorted for BST)")
    print("✓ Preorder: Root -> Left -> Right (copy tree)")
    print("✓ Postorder: Left -> Right -> Root (delete tree)")
    print("✓ Level Order: BFS traversal by levels")
    print("✓ BST properties: left < root < right")
    print("✓ Tree height: longest path from root to leaf")
    print("✓ Recursive vs iterative implementations")


if __name__ == "__main__":
    main()