def read_file():
  data = open('test_input', 'r').read().split('\n')
  first_line = data[0]
  return (first_line, data[2:])

def build_polymer_template(pairs):
  polymer_template = {}
  for pair in pairs:
    p, v = pair.split(' -> ')
    (l, r) = p
    polymer_template[(l, r)] = ((l, v), (v, r))
  return polymer_template

def get_polymer_pairs(polymer):
  return [(x, y) for x, y in zip(polymer, polymer[1:])]

# LinkedList will help?
class LinkedList(object):
  def __init__(self, pair, split_template):
    node = Node(pair)
    self.split_template = split_template
    self.head = node
  
  def add(self, pair):
    node = Node(pair)
    it = self.head
    while it.next_node != None:
      it = it.next_node
    it.next_node = node

  def print_nodes(self):
    it = self.head

    while it.next_node != None:
      print(it.pair, end = '')
      it = it.next_node
    
    print(it.pair)
  
  def split_each_node(self):
    it = self.head
    while it.next_node != None:
      it.split_node(self.split_template)
      it = it.next_node.next_node
    
    it.split_node(self.split_template)

  def join_pairs(self):
    it = self.head
    joined = []
    while it.next_node != None:
      (l, r) = it.pair
      joined.append(l)
      it = it.next_node
    
    (l, r) = it.pair
    joined.append(l)
    joined.append(r)
    return joined

class Node(object):
  def __init__(self, pair=None, next_node=None):
    self.pair = pair
    self.next_node = next_node

  def split_node(self, split_template):
    (pair_1, pair_2) = split_template[self.pair]
    self.pair = pair_1
    self.next_node = Node(pair_2, self.next_node)

# Read
polymer, pairs = read_file()

# Tasks
polymer = list(polymer)
polymer_template = build_polymer_template(pairs)
polymer_pairs = get_polymer_pairs(polymer)

first_polymer_pair = polymer_pairs[0]
linked_list = LinkedList(first_polymer_pair, polymer_template)

for polymer_pair in polymer_pairs[1:]:
  linked_list.add(polymer_pair)

for i in range(0, 4):
  linked_list.split_each_node()
  print(i)

new_polymer = ''.join(linked_list.join_pairs())
print(new_polymer)
