import sys

sys.setrecursionlimit(5000)

def read_file():
  return open('input', 'r').read().split('\n')

class LeafNode:
  def __init__(self, value):
    self.value = value
    self.id = None
    self.left = None
    self.right = None

class Node:
  def __init__(self, left = None, right = None, is_root = False):
    self.left = left
    self.right = right
    self.ids = {}
    self.id = 0
    self.top_id = 0

  def merge_into_self(self, node):
    if not self.left and not self.right:
      self.left = node.left
      self.right = node.right
    else:
      new_node = Node(self.left, self.right)
      self.left = new_node
      self.right = node
    self.reindex()

  def find_parent_to(self, node):
    node_id = node.id
    current_node = self
    previous_node = self
    which = None
    while current_node.id != node_id:
      if node_id < current_node.id:
        previous_node = current_node
        current_node = current_node.left
        which = 'left'
      else:
        previous_node = current_node
        current_node = current_node.right
        which = 'right'
      if current_node == None:
        return None, None
    return previous_node, which

  def change_to_zero_leaf(self, node):
    parent, which = self.find_parent_to(node)
    if parent:
      setattr(self.ids[parent.id], which, LeafNode(0))
      return
    raise Exception('Indexing failed, zero leaf error')
    
  def add_to_leaf_on_left(self, val, current_node):
    idx = current_node.id
    for i in range(idx - 1, 0, -1):
      if type(self.ids[i]) == LeafNode:
        self.ids[i].value += val
        return self.ids[i].value
    
  def add_to_leaf_on_right(self, val, current_node):
    idx = current_node.id
    for i in range(idx + 1, len(self.ids) + 1):
      if type(self.ids[i]) == LeafNode:
        self.ids[i].value += val
        return self.ids[i].value

  def reindex(self):
    self.ids = {}
    self.top_id = 0
    Node.inorder(self, self.index_one)

  def index_one(self, node):
    self.top_id += 1
    node.id = self.top_id
    self.ids[node.id] = node

  def reduce_node(self):
    self.explode_required = True

    while self.explode_required:
      self.explode(self)
      if not self.explode_required:
        self.split(self)

  def split(self, node):
    if node == None:
      return False

    if self.explode_required: return True
    self.explode_required |= self.split(node.left)

    if type(node) == LeafNode:
      if node.value >= 10:
        self.explode_required = True
        x = node.value // 2
        y = x + node.value % 2
        parent, which = self.find_parent_to(node)
        if parent and which:
          setattr(parent, which, Node(LeafNode(x), LeafNode(y)))
        else:
          raise Exception("Can't split!")
        self.reindex()

    self.explode_required |= self.split(node.right)
    return self.explode_required

  def explode(self, node, depth = 0):
    if type(node) == LeafNode:
      return False

    self.explode(node.left, depth + 1)
  
    if depth == 4:
      if node.left and node.right:
        x, y = node.left.value, node.right.value
        left_value = self.add_to_leaf_on_left(x, node.left)
        right_value = self.add_to_leaf_on_right(y, node.right)
        self.change_to_zero_leaf(node)
        self.reindex()
        return True
      else:
        raise Exception('Tree explosion error')

    self.explode(node.right, depth + 1)
    self.explode_required = False
  
  @staticmethod
  def magnitude(node):
    stack = []
    operations = []
    last_node_visited = None
    # Post order iterative - forming a RPN
    while len(stack) or node != None:
      if node != None:
        stack.append(node)
        node = node.left
      else:
        peek_node = stack[-1]
        if peek_node.right != None and last_node_visited != peek_node.right:
          node = peek_node.right
        else:
          if type(peek_node) == LeafNode:
            operations.append(peek_node.value)
          else:
            operations.append("+")
          last_node_visited = stack.pop()

    # Reverse Polish notation format
    result = 0
    stack = []
    for op in operations:
      if op != "+":
        stack.append(op)
      else:
        n1 = stack.pop()
        n2 = stack.pop()
        stack.append(n1 * 2 + n2 * 3)
    return stack[0]

  @staticmethod
  def leafs_to_list(node):
    leafs = []
    stack = []
    # In order iterative
    while len(stack) or node != None:
      if node != None:
        stack.append(node)
        node = node.left
      else:
        node = stack.pop()
        if type(node) == LeafNode:
          leafs.append(node.value)
        node = node.right
    return leafs

  @staticmethod
  def print_node(node):
    if type(node) == LeafNode:
      print(f'{node.value} ', end='')

  @staticmethod
  def inorder(node, do):
    if node == None:
      return
  
    Node.inorder(node.left, do)
    do(node)
    Node.inorder(node.right, do)

  @staticmethod
  def new_node(val):
    if type(val) == list:
      return Node.build_node_from_list(val)
    elif type(val) == int:
      return LeafNode(val)
    else:
      raise Exception('Invalid type')
  
  @staticmethod
  def build_node_from_list(lst):
    if type(lst) is list:
      left = Node.new_node(lst[0])
      right = Node.new_node(lst[1])
      node = Node(left, right)
      return node
    else:
      raise Exception('Too deep!')

# Part 1
data = read_file()
root_node = Node(is_root = True)

i = 0
for line in data:
  new_node = Node.build_node_from_list(eval(line))
  root_node.merge_into_self(new_node)
  root_node.reduce_node()
  # Node.inorder(root_node, Node.print_node)
  # print('')

leafs_as_list = Node.leafs_to_list(root_node)
# print(leafs_as_list)

final_magnitude = Node.magnitude(root_node)
print(final_magnitude)

# Part 2
highest_magnitude = 0
import itertools
for l1, l2 in itertools.permutations(data, 2):
  top_node = Node(is_root = True)
  node1 = Node.build_node_from_list(eval(l1))
  node2 = Node.build_node_from_list(eval(l2))
  top_node.merge_into_self(node1)
  top_node.merge_into_self(node2)
  top_node.reduce_node()
  final_magnitude = Node.magnitude(top_node)
  if final_magnitude > highest_magnitude:
    highest_magnitude = final_magnitude
    print(final_magnitude)
