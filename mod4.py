class BTNode:
    def __init__(self, leaf=False):
        self.leaf = leaf
        self.keys = []
        self.children = []

class BT:
    def __init__(self, degree=4):
        self.root = BTNode(leaf=True)
        self.degree = degree

    def search(self, key, node=None):
        if node is None:
            node = self.root
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1
        if i < len(node.keys) and key == node.keys[i]:
            return node, i
        elif node.leaf:
            return None, None
        else:
            return self.search(key, node.children[i])

    def insert(self, key):
        root = self.root
        if len(root.keys) == (2 * self.degree) - 1:
            new_root = BTNode()
            new_root.children.append(root)
            self.split_child(new_root, 0)
            self.insert_non_full(new_root, key)
            self.root = new_root
        else:
            self.insert_non_full(root, key)

    def insert_non_full(self, node, key):
        i = len(node.keys) - 1
        if node.leaf:
            node.keys.append(None)
            while i >= 0 and key < node.keys[i]:
                node.keys[i + 1] = node.keys[i]
                i -= 1
            node.keys[i + 1] = key
        else:
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1
            if len(node.children[i].keys) == (2 * self.degree) - 1:
                self.split_child(node, i)
                if key > node.keys[i]:
                    i += 1
            self.insert_non_full(node.children[i], key)

    def split_child(self, parent, index):
        degree = self.degree
        child = parent.children[index]
        new_child = BTNode(leaf=child.leaf)

        parent.keys.insert(index, child.keys[degree - 1])
        parent.children.insert(index + 1, new_child)

        new_child.keys = child.keys[degree:(2 * degree) - 1]
        child.keys = child.keys[0:degree - 1]

        if not child.leaf:
            new_child.children = child.children[degree:(2 * degree)]
            child.children = child.children[0:degree]

    def delete(self, key):
        root = self.root
        self.delete_recursive(root, key)

    def delete_recursive(self, node, key):
        degree = self.degree
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1

        if i < len(node.keys) and key == node.keys[i]:
            if node.leaf:
                del node.keys[i]
            else:
                if len(node.children[i]) >= degree:
                    predecessor = self.get_predecessor(node, i)
                    node.keys[i] = predecessor
                    self.delete_recursive(node.children[i], predecessor)
                elif len(node.children[i + 1]) >= degree:
                    successor = self.get_successor(node, i)
                    node.keys[i] = successor
                    self.delete_recursive(node.children[i + 1], successor)
                else:
                    self.merge_children(node, i)
                    self.delete_recursive(node.children[i], key)
        else:
            if node.leaf:
                return
            if len(node.children[i].keys) < degree:
                self.fill_child(node, i)
            if i > len(node.keys):
                self.delete_recursive(node.children[i - 1], key)
            else:
                self.delete_recursive(node.children[i], key)

    def fill_child(self, node, index):
        degree = self.degree
        if index != 0 and len(node.children[index - 1].keys) >= degree:
            self.borrow_from_left(node, index)
        elif index != len(node.keys) and len(node.children[index + 1].keys) >= degree:
            self.borrow_from_right(node, index)
        else:
            if index != len(node.keys):
                self.merge_children(node, index)
            else:
                self.merge_children(node, index - 1)

    def borrow_from_left(self, node, index):
        child = node.children[index]
        sibling = node.children[index - 1]

        child.keys.insert(0, node.keys[index - 1])
        node.keys[index - 1] = sibling.keys.pop()

        if not child.leaf:
            child.children.insert(0, sibling.children.pop())

    def borrow_from_right(self, node, index):
        child = node.children[index]
        sibling = node.children[index + 1]

        child.keys.append(node.keys[index])
        node.keys[index] = sibling.keys.pop(0)

        if not child.leaf:
            child.children.append(sibling.children.pop(0))

    def merge_children(self, node, index):
        child = node.children[index]
        sibling = node.children[index + 1]

        child.keys.append(node.keys[index])
        child.keys.extend(sibling.keys)
        node.keys.pop(index)
        node.children.pop(index + 1)

        if not child.leaf:
            child.children.extend(sibling.children)

    def get_predecessor(self, node, index):
        node = node.children[index]
        while not node.leaf:
            node = node.children[-1]
        return node.keys[-1]

    def get_successor(self, node, index):
        node = node.children[index + 1]
        while not node.leaf:
            node = node.children[0]
        return node.keys[0]

    def range(self, start_key, end_key):
        results = []
        self.range_query_recursive(self.root, start_key, end_key, results)
        return results

    def range_query_recursive(self, node, start_key, end_key, results):
        i = 0
        while i < len(node.keys) and node.keys[i] < start_key:
            i += 1

        if node.leaf:
            while i < len(node.keys) and node.keys[i] <= end_key:
                results.append(node.keys[i])
                i += 1
        else:
            while i < len(node.keys):
                self.range_query_recursive(node.children[i], start_key, end_key, results)
                if i < len(node.keys) and node.keys[i] <= end_key:
                    results.append(node.keys[i])
                i += 1
            if len(node.keys) > 0 and node.keys[-1] <= end_key:
                self.range_query_recursive(node.children[-1], start_key, end_key, results)

btree = BT(degree=3)
for key in [10, 20, 5, 6, 12, 30, 7, 17, 3, 9]:
    btree.insert(key)
print("Search for key 6:", btree.search(6))
print("Search for key 100:", btree.search(100))
print("Range query [5, 20]:", btree.range(5, 20))
btree.delete(6)
btree.delete(20)
print("After deletion of keys 6 and 20:", btree.range(0, 100))