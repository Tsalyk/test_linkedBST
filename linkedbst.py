"""
File: linkedbst.py
Author: Ken Lambert
"""

from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
from random import choice, shuffle
from time import time
from math import log
from sys import setrecursionlimit


setrecursionlimit(10000)


def _LinearSearch(lst: list, element):
    """
    Returns index of the value in list using linear search
    """
    for i in range (len(lst)):
        if lst[i] == element:
            return i
    return -1


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            string = ""
            if node != None:
                string += recurse(node.right, level + 1)
                string += "| " * level
                string += str(node.data) + "\n"
                string += recurse(node.left, level + 1)
            return string

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        curr = self._root
        parent = None

        if curr is None:
            self._root = BSTNode(item)
            self._size += 1
            return

        while curr:
            parent = curr

            if item < curr.data:
                curr = curr.left
            else:
                curr = curr.right

        if item < parent.data:
            parent.left = BSTNode(item)
        else:
            parent.right = BSTNode(item)

        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def lift_max_in_left_subtree_to_top(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            current_node = top.left
            while not current_node.right == None:
                parent = current_node
                current_node = current_node.right
            top.data = current_node.data
            if parent == top:
                top.left = current_node.left
            else:
                parent.right = current_node.left

        # Begin main part of the method
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
        item_removed = None
        pre_root = BSTNode(None)
        pre_root.left = self._root
        parent = pre_root
        direction = 'L'
        current_node = self._root
        while not current_node == None:
            if current_node.data == item:
                item_removed = current_node.data
                break
            parent = current_node
            if current_node.data > item:
                direction = 'L'
                current_node = current_node.left
            else:
                direction = 'R'
                current_node = current_node.right

        # Return None if the item is absent
        if item_removed == None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not current_node.left == None \
                and not current_node.right == None:
            lift_max_in_left_subtree_to_top(current_node)
        else:

            # Case 2: The node has no left child
            if current_node.left == None:
                new_child = current_node.right

                # Case 3: The node has no right child
            else:
                new_child = current_node.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = new_child
            else:
                parent.right = new_child

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = pre_root.left
        return item_removed

    def replace(self, item, new_item):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                old_data = probe.data
                probe.data = new_item
                return old_data
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''
        def height1(top):
            '''
            Helper function
            :param top:
            :return:
            '''
            if top is None:
                return -1

            return 1 + max(height1(top.left), height1(top.right))

        return height1(self._root)

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        def helper(root):
            '''
            Helper method to determine whether the tree is balanced
            '''
            if root is None:
                return 0

            left_height = helper(root.left)
            if left_height == -1:
                return -1

            right_height = helper(root.right)
            if right_height == -1:
                return -1

            if abs(left_height - right_height) > 1:
                return -1

            return max(left_height, right_height) + 1

        return helper(self._root) > -1 and\
               self.height() < 2 * log((len(self) + 1), 2) - 1

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        def find_helper(root, elements=[]):

            if root is None:
                return

            find_helper(root.left, elements)
            find_helper(root.right, elements)

            if root.data in range(low, high+1):
                elements.append(root.data)

            return elements

        return find_helper(self._root)

    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        if self.is_balanced():
            return

        nodes = [el for el in self.inorder()]
        self.clear()

        def rebalance_helper(nodes, start=0, end=len(nodes)-1):
            if start > end:
                return

            middle = (start+end) // 2

            self.add(nodes[middle])

            rebalance_helper(nodes, start, middle-1)
            rebalance_helper(nodes, middle+1, end)

        return rebalance_helper(nodes)

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        def helper_successor(root, larger=[]):
            if root is None:
                return

            if root.data > item:
                helper_successor(root.left, larger)
                larger.append(root.data)
            else:
                helper_successor(root.right, larger)

            if larger:
                return min(larger)
            else:
                return

        return helper_successor(self._root)

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        def helper_predeccessor(root, smaller=[]):
            if root is None:
                return

            if root.data < item:
                helper_predeccessor(root.right, smaller)
                smaller.append(root.data)
            else:
                helper_predeccessor(root.left, smaller)

            if smaller:
                return max(smaller)
            else:
                return

        return helper_predeccessor(self._root)

    @staticmethod
    def built_in_search(words: list):
        """
        Returns time of searching 10000 random words using
        built in list type methods
        """
        found_words = []
        now = time()
        

        while len(found_words) != 10000:
            found_words.append(_LinearSearch(words, choice(words)))

        print("Time of the search 10000 random words using built "
             f"in list methods: {time()-now}")

        return found_words

    @staticmethod
    def ordered_binary_search(words: list):
        """
        Returns time of searching 10000 random words using
        binary search in ordered tree
        """
        found_words = []
        tree = LinkedBST()

        for word in words:
            tree.add(word)
            if len(tree) > 10000:
                break

        now = time()

        while len(found_words) != 10000:
            found_words.append(tree.find(choice(words)))
        
        print("Time of the search 10000 sorted random words using "
             f"binary tree search method: {time()-now}")

        return found_words

    @staticmethod
    def not_ordered_binary_search(words: list):
        """
        Returns time of searching 10000 random words using
        binary search in not ordered tree
        """
        words = words.copy()
        shuffle(words)
        found_words = []
        tree = LinkedBST()

        for word in words:
            tree.add(word)
            if len(tree) > 10000:
                break

        now = time()

        while len(found_words) != 10000:
            found_words.append(tree.find(choice(words)))
        
        print("Time of the search 10000 not sorted random words using "
             f"binary tree search method: {time()-now}")

        return found_words

    @staticmethod
    def balanced_binary_search(words: list):
        """
        Returns time of searching 10000 random words using
        binary search in balanced tree
        """
        found_words = []
        tree = LinkedBST()

        for word in words:
            tree.add(word)
            if len(tree) > 10000:
                break
        tree.rebalance()

        now = time()

        while len(found_words) != 10000:
            found_words.append(tree.find(choice(words)))
        
        print("Time of the search 10000 random words using "
             f"balanced binary tree search method: {time()-now}")

        return found_words

    def demo_bst(self, path: str):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        words = []
        with open(path, "r", encoding="utf-8") as file:
            word = file.readline()
            while word:
                words.append(word.strip().strip())
                word = file.readline()

        self.built_in_search(words)
        self.ordered_binary_search(words)
        self.not_ordered_binary_search(words)
        self.balanced_binary_search(words)
