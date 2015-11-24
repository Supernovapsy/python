#!/usr/bin/python
import json   # Used when TRACE=jsonp
import os     # Used to get the TRACE environment variable
import re     # Used when TRACE=jsonp
import sys    # Used to smooth over the range / xrange issue.

# Python 3 doesn't have xrange, and range behaves like xrange.
if sys.version_info >= (3,):
    xrange = range

# Circuit verification library.

class Wire(object):
  """A wire in an on-chip circuit.
  
  Wires are immutable, and are either horizontal or vertical.
  """
  
  def __init__(self, name, x1, y1, x2, y2):
    """Creates a wire.
    
    Raises an ValueError if the coordinates don't make up a horizontal wire
    or a vertical wire.
    
    Args:
      name: the wire's user-visible name
      x1: the X coordinate of the wire's first endpoint
      y1: the Y coordinate of the wire's first endpoint
      x2: the X coordinate of the wire's last endpoint
      y2: the Y coordinate of the wire's last endpoint
    """
    # Normalize the coordinates.
    if x1 > x2:
      x1, x2 = x2, x1
    if y1 > y2:
      y1, y2 = y2, y1
    
    self.name = name
    # The use of tuples makes the wire immutable. The 4 coordinates alone define the wire.
    self.x1, self.y1 = x1, y1
    self.x2, self.y2 = x2, y2
    self.object_id = Wire.next_object_id()
    
    if not (self.is_horizontal() or self.is_vertical()):
      # __repr__() defines str()
      raise ValueError(str(self) + ' is neither horizontal nor vertical')
  
  def is_horizontal(self):
    """True if the wire's endpoints have the same Y coordinates."""
    return self.y1 == self.y2
  
  def is_vertical(self):
    """True if the wire's endpoints have the same X coordinates."""
    return self.x1 == self.x2
  
  def intersects(self, other_wire):
    """True if this wire intersects another wire."""
    # NOTE: we assume that wires can only cross, but not overlap.
    if self.is_horizontal() == other_wire.is_horizontal():
      return False 
    
    if self.is_horizontal():
      h = self
      v = other_wire
    else:
      h = other_wire
      v = self
    return v.y1 <= h.y1 and h.y1 <= v.y2 and h.x1 <= v.x1 and v.x1 <= h.x2
  
  def __repr__(self):
    # :nodoc: nicer formatting to help with debugging
    return('<wire ' + self.name + ' (' + str(self.x1) + ',' + str(self.y1) + 
           ')-(' + str(self.x2) + ',' + str(self.y2) + ')>')
  
  def as_json(self):
    """Dict that obeys the JSON format restrictions, representing the wire."""
    return {'id': self.name, 'x': [self.x1, self.x2], 'y': [self.y1, self.y2]}

  # Next number handed out by Wire.next_object_id()
  _next_id = 0
  
  @staticmethod
  def next_object_id():
    """Returns a unique numerical ID to be used as a Wire's object_id."""
    id = Wire._next_id
    Wire._next_id += 1
    return id

class WireLayer(object):
  """The layout of one layer of wires in a chip."""
  
  def __init__(self):
    """Creates a layer layout with no wires."""
    self.wires = {}
  
  def wires(self):
    """The wires in the layout."""
    self.wires.values()
  
  def add_wire(self, name, x1, y1, x2, y2):
    """Adds a wire to a layer layout.
    
    Args:
      name: the wire's unique name
      x1: the X coordinate of the wire's first endpoint
      y1: the Y coordinate of the wire's first endpoint
      x2: the X coordinate of the wire's last endpoint
      y2: the Y coordinate of the wire's last endpoint
    
    Raises an exception if the wire isn't perfectly horizontal (y1 = y2) or
    perfectly vertical (x1 = x2)."""
    # Operation is O(1) since self.wires is a dict.
    if name in self.wires:
        raise ValueError('Wire name ' + name + ' not unique')
    # A wire layer stores its wires inside a dict.
    self.wires[name] = Wire(name, x1, y1, x2, y2)
  
  def as_json(self):
    """Dict that obeys the JSON format restrictions, representing the layout."""
    return { 'wires': [wire.as_json() for wire in self.wires.values()] }
  
  @staticmethod
  def from_file(file):
    """Builds a wire layer layout by reading a textual description from a file.
    
    Args:
      file: a File object supplying the input
    
    Returns a new Simulation instance."""

    layer = WireLayer()
    
    while True:
      command = file.readline().split()
      if command[0] == 'wire':
        coordinates = [float(token) for token in command[2:6]]
        layer.add_wire(command[1], *coordinates)
      elif command[0] == 'done':
        break
      
    return layer

class RangeIndexOld(object):
  """Array-based range index implementation."""
  
  def __init__(self):
    """Initially empty range index."""
    self.data = []
  
  def add(self, key):
    """Inserts a key in the range index."""
    if key is None:
        raise ValueError('Cannot insert nil in the index')
    self.data.append(key)
  
  def remove(self, key):
    """Removes a key from the range index."""
    self.data.remove(key)
  
  def list(self, first_key, last_key):
    """List of values for the keys that fall within [first_key, last_key]."""
    return [key for key in self.data if first_key <= key <= last_key]
  
  def count(self, first_key, last_key):
    """Number of keys that fall within [first_key, last_key]."""
    result = 0
    for key in self.data:
      if first_key <= key <= last_key:
        result += 1
    return result

class BSTnode(object):
  def __init__(self, key):
    self.key = key
    self.disconnect()
  
  def disconnect(self):
    self.p, self.right, self.left = None, None, None

class setBST(object):
  """Define setBST to not allow elements with duplicate keys."""
  def __init__(self):
    self.root = None

  def find(self, key):
    node = self.root
    while node != None:
      if key == node.key:
        return node
      elif key < node.key:
        node = node.left
      else:
        node = node.right
    return None

  def add(self, key):
    newNode = BSTnode(key)
    node = self.root
    if node is None:
      self.root = newNode
      return
    while True:
      if key < node.key:
        if node.left == None:
          newNode.p = node
          node.left = newNode
          return
        node = node.left
      elif key > node.key:
        if node.right == None:
          newNode.p = node
          node.right = newNode
          return
        node = node.right
      else:
        raise Exception("setBST(to be inherited by RangeIndex) cannot handle multiple nodes with the same key.")
    return newNode

  def _transplant(self, b, a):
    """Transplants b and its children to a's position, and displace a from its position."""
    if a is None:
      raise Exception("Cannot transplant an element to an empty tree")
    
    # Setting the bond between b and a.p completes the transplant.
    # The other pointers are untouched.
    if a.p is None:
      self.root = b
    else: # This can be simplified into an elif and then an else.
      if a.p.left == a:
        a.p.left = b
      else:
        a.p.right = b
    if b:
      b.p = a.p  

  def find_min(self, node):
    if node == 0:
      node = self.root
    while node and node.left != None:
      node = node.left
    return node

  def delete(self, key):
    node = self.find(key)
    if not node:
        return
    if node.left is None:
      self._transplant(node.right, node)
      '''if node.p.left == node:
        node.p.left = node.right
      else:
        node.p.right = node.right
      node.right.p = node.p'''
    elif node.right is None:
      self._transplant(node.left, node)
      '''if node.p.left == node:
        node.p.left = node.left
      else:
        node.p.right = node.left
      node.left.p'''
    else:
      successor = self.find_min(node.right)
      # Step 1
      successor.left = node.left
      node.left.p = successor
      # Step 2&3: has the subtlety where this action is only needed if node's right child is not its successor.
      if node.right != successor:
        self._transplant(successor.right, successor)
        node.right.p = successor
        successor.right = node.right
      # Step 4
      self._transplant(successor, node)

  def _element_count(self, node = 0):
    """Counts the number of elements in the tree.
    
    0 is used as the sentinel value for determining whether the current call is the highest level call."""
    if node == 0:
      node = self.root
    if node:
      return 1 + self._element_count(node.left) + self._element_count(node.right)
    else:
      return 0

def rn_height(node):
  return node.height if node else 0

def rn_size(node):
  return node.size if node else 0

class RangeNode(BSTnode):
  def __init__(self, key):
    # The secondary way of calling a non-static method is the only way to refer to the base class method.
    BSTnode.__init__(self, key)
    # Default sizes assuming that this element forms a tree by itself.
    self.size = 1 # Augmented value
    self.height = 1 # Augmented value for AVL.

# LIMITATION: Does not support objects with the same keys, but this is not needed for the problem at hand.
class RangeIndex(setBST):
  def rank(self, key):
    current = self.root
    rank_count = 0
    if current is None:
      return rank_count

    while current and current.key != key:
      if key > current.key:
        rank_count += rn_size(current.left) + 1
        current = current.right
      else:
        current = current.left

    if current:
      assert(current.key == key)
      return rank_count + rn_size(current.left) + 1
    else: # Reaching here should only be possible if KeyWirePairL or KeyWirePairH is used. An element with a matching key should always be found.
      return rank_count

  def list(self, l, h):
    lca = self.lca(l, h)
    result = []
    self._node_list(lca, l, h, result)
    return result

  def count(self, l, h):
    ret = self.rank(h) - self.rank(l)
    return ret + 1 if self.find(l) else ret

  def _node_list(self, node, l, h, result):
    # Using a while loop would need a queue or stack to store the nodes still to process.
    if node is not None:
      if node.key >= l and node.key <= h:
        result.append(node.key)
        self._node_list(node.left, l, h, result)
        self._node_list(node.right, l, h, result)
      elif node.key < l:
        self._node_list(node.right, l, h, result)
      else:
        self._node_list(node.left, l, h, result)

  def lca(self, l, h):
    node = self.root
    '''
    stopped_at_left = False
    stopped_at_right = False
    '''
    # >= and <= if commented out parts are present.
    # The condition below works if there are no duplicate keys.
    # This condition ensures that if the tree is not empty and if the keys being queried is actually
    # in the tree, then the function will always return a valid node.
    while node and (l > node.key or h < node.key):
      '''
      if l.key == node.key:
        stopped_at_left = True
      elif h.key == node.key:
        stopped_at_right = True
      '''
      if l < node.key:
        node = node.left
      elif l > node.key:
        node = node.right
      # This else statement would not be here if the commented out parts are present.
      # Having this statement means that if the node doesn't have any child wanted, then
      # we have reached the left or right limit of the tree and should stop.
      else:
        break
    '''
      else:
        raise Exception("Either l or h is not found in the tree. Error!")
    verify = RangeNode(0)
    if stopped_at_left:
      verify = self.find(h, node)
    elif stopped_at_right:
      verify = self.find(l, node)

    return node if verify else None
    '''
    return node

  def add(self, key):
    newNode = RangeNode(key)
    node = self.root
    if node is None:
      self.root = newNode
      return
    while True:
      if key < node.key:
        if node.left == None:
          newNode.p = node
          node.left = newNode
          break
        node = node.left
      elif key > node.key:
        if node.right == None:
          newNode.p = node
          node.right = newNode
          break
        node = node.right
      else:
        raise Exception("setBST(to be inherited by RangeIndex) cannot handle multiple nodes with the same key.")
    RangeIndex._update_height_and_size(newNode)
    self._rebalance(newNode)
    return newNode

  def delete(self, key):
    node = self.find(key)
    if not node:
        return
    node_to_rebalance = node.p
    if node.left is None:
      self._transplant(node.right, node)
      '''if node.p.left == node:
        node.p.left = node.right
      else:
        node.p.right = node.right
      node.right.p = node.p'''
    elif node.right is None:
      self._transplant(node.left, node)
      '''if node.p.left == node:
        node.p.left = node.left
      else:
        node.p.right = node.left
      node.left.p'''
    else:
      successor = self.find_min(node.right)
      # Step 1
      successor.left = node.left
      node.left.p = successor
      # Step 2&3: has the subtlety where this action is needed only if node's right child is its successor.
      if node.right != successor:
        self._transplant(successor.right, successor)
        node.right.p = successor
        successor.right = node.right
        node_to_rebalance = successor.p # This is true if node.right is not the successor.
      else:
        # If node.right is the succesor, keep the pointers between successor and its right child the same.
        # However, need to rebalance from this point.
        node_to_rebalance = successor
      # Step 4
      self._transplant(successor, node)
    # Update the attributes of the node to be balanced, and then rebalance the tree from that node.
    RangeIndex._update_height_and_size(node_to_rebalance)
    self._rebalance(node_to_rebalance)

  def _left_rotate(self, a):
    # Pointers that need to be changed:
    # a.p.left or a.p.right
    # y.left, y.p
    # y.left.p
    # a.p, a.right
    y = a.right
    if not y:
      raise Exception("Cannot left rotate if right child is None")

    self._transplant(y.left, y)
    self._transplant(y, a)
    y.left = a
    a.p = y
    RangeIndex._update_height_and_size(a)

  def _right_rotate(self, a):
    y = a.left
    if not y:
      raise Exception("Cannot right rotate if left child is None")

    self._transplant(y.right, y)
    self._transplant(y, a)
    y.right = a
    a.p = y
    RangeIndex._update_height_and_size(a)

  def _rebalance(self, a):
    while a:
      if rn_height(a.left) - rn_height(a.right) == 2:
        if rn_height(a.left.right) > rn_height(a.left.left):
          self._left_rotate(a.left)
        self._right_rotate(a)
      elif rn_height(a.right) - rn_height(a.left) == 2:
        if rn_height(a.right.left) > rn_height(a.right.right):
          self._right_rotate(a.right)
        self._left_rotate(a)
      a = a.p
  
  @staticmethod
  def _update_height_and_size(node):
    while node:
      node.size = 1 + rn_size(node.left) + rn_size(node.right)
      node.height = max(rn_height(node.left), rn_height(node.right)) + 1
      node = node.p

class TracedRangeIndex(RangeIndex):
  """Augments RangeIndex to build a trace for the visualizer."""
  
  def __init__(self, trace):
    """Sets the object receiving tracing info."""
    RangeIndex.__init__(self)
    self.trace = trace
  
  def add(self, key):
    self.trace.append({'type': 'add', 'id': key.wire.name})
    RangeIndex.add(self, key)
  
  def remove(self, key):
    self.trace.append({'type': 'delete', 'id': key.wire.name})
    RangeIndex.remove(self, key)
  
  def list(self, first_key, last_key):
    result = RangeIndex.list(self, first_key, last_key)
    self.trace.append({'type': 'list', 'from': first_key.key,
                       'to': last_key.key,
                       'ids': [key.wire.name for key in result]}) 
    return result
  
  def count(self, first_key, last_key):
    result = RangeIndex.count(self, first_key, last_key)
    self.trace.append({'type': 'list', 'from': first_key.key,
                       'to': last_key.key, 'count': result})
    return result

class ResultSet(object):
  """Records the result of the circuit verifier (pairs of crossing wires)."""
  
  def __init__(self):
    """Creates an empty result set."""
    self.crossings = []
  
  def add_crossing(self, wire1, wire2):
    """Records the fact that two wires are crossing."""
    self.crossings.append(sorted([wire1.name, wire2.name]))
  
  def write_to_file(self, file):
    """Write the result to a file."""
    for crossing in self.crossings:
      file.write(' '.join(crossing))
      file.write('\n')

class TracedResultSet(ResultSet):
  """Augments ResultSet to build a trace for the visualizer."""
  
  def __init__(self, trace):
    """Sets the object receiving tracing info."""
    ResultSet.__init__(self)
    self.trace = trace
    
  def add_crossing(self, wire1, wire2):
    self.trace.append({'type': 'crossing', 'id1': wire1.name,
                       'id2': wire2.name})
    ResultSet.add_crossing(self, wire1, wire2)

class KeyWirePair(object):
  """Wraps a wire and the key representing it in the range index.
  
  Once created, a key-wire pair is immutable."""
  
  def __init__(self, key, wire):
    """Creates a new key for insertion in the range index."""
    self.key = key
    if wire is None:
      raise ValueError('Use KeyWirePairL or KeyWirePairH for queries')
    self.wire = wire
    self.wire_id = wire.object_id

  def __lt__(self, other):
    # :nodoc: Delegate comparison to keys.
    return (self.key < other.key or
            (self.key == other.key and self.wire_id < other.wire_id))
  
  def __le__(self, other):
    # :nodoc: Delegate comparison to keys.
    return (self.key < other.key or
            (self.key == other.key and self.wire_id <= other.wire_id))  

  def __gt__(self, other):
    # :nodoc: Delegate comparison to keys.
    return (self.key > other.key or
            (self.key == other.key and self.wire_id > other.wire_id))
  
  def __ge__(self, other):
    # :nodoc: Delegate comparison to keys.
    return (self.key > other.key or
            (self.key == other.key and self.wire_id >= other.wire_id))

  def __eq__(self, other):
    # :nodoc: Delegate comparison to keys.
    return self.key == other.key and self.wire_id == other.wire_id
  
  def __ne__(self, other):
    # :nodoc: Delegate comparison to keys.
    return not (self.key == other.key and self.wire_id == other.wire_id)

  def __hash__(self):
    # :nodoc: Delegate comparison to keys.
    return hash([self.key, self.wire_id])

  def __repr__(self):
    # :nodoc: nicer formatting to help with debugging
    return '<key: ' + str(self.key) + ' wire: ' + str(self.wire) + '>'

class KeyWirePairL(KeyWirePair):
  """A KeyWirePair that is used as the low end of a range query.
  
  This KeyWirePair is smaller than all other KeyWirePairs with the same key."""
  def __init__(self, key):
    self.key = key
    self.wire = None
    self.wire_id = -1000000000

class KeyWirePairH(KeyWirePair):
  """A KeyWirePair that is used as the high end of a range query.
  
  This KeyWirePair is larger than all other KeyWirePairs with the same key."""
  def __init__(self, key):
    self.key = key
    self.wire = None
    # HACK(pwnall): assuming 1 billion objects won't fit into RAM.
    self.wire_id = 1000000000
    
class CrossVerifier(object):
  """Checks whether a wire network has any crossing wires."""

  eventTypeN = 3
  
  def __init__(self, layer):
    """Verifier for a layer of wires.
    
    Once created, the verifier can list the crossings between wires (the 
    wire_crossings method) or count the crossings (count_crossings)."""

    self.events = []
    # Populates events into a list, and returns the max and min x values.
    min_x, max_x = self._events_from_layer(layer)
    self.events.sort(key = lambda a: a[1])
    self.events.sort(key = lambda a: a[0])
  
    # The data structure which will be used to quickly get all the horizontal wires crossing a particular vertical wire.
    self.index = RangeIndex()
    self.result_set = ResultSet()
    self.performed = False
  
  def count_crossings(self):
    """Returns the number of pairs of wires that cross each other."""
    if self.performed:
      raise 
    self.performed = True
    return self._compute_crossings(True)

  def wire_crossings(self):
    """An array of pairs of wires that cross each other."""
    if self.performed:
      raise 
    self.performed = True
    return self._compute_crossings(False)

  def _events_from_layer(self, layer):
    """Populates the sweep line events from the wire layer."""
    min_x = 1000000
    max_x = -1000000
    for wire in layer.wires.values():
      # Three types of events where the order matters. These can be sorted by counting sort.
      if wire.is_horizontal():
        min_x = min(min_x, wire.x1)
        max_x = max(max_x, wire.x2)
        self.events.append([wire.x1, 0, wire.object_id, 'add', wire])
        self.events.append([wire.x2, 2, wire.object_id, 'delete', wire])
      else:
        self.events.append([wire.x1, 1, wire.object_id, 'query', wire])
    return min_x, max_x

  def _compute_crossings(self, count_only):
    """Implements count_crossings and wire_crossings."""
    if count_only:
      result = 0
    else:
      result = self.result_set

    for event in self.events:
      event_x, event_type, wire = event[0], event[3], event[4]
      
      # This is the order in which the events are processed:
      # 1: Add horizontal wires currently being sweeped at the x location queried
      # (since events of the same x always begin with all add events, as long as
      # horizontal wires are added as they are seen, no crossings will be missed.
      # 2. Query the horizontal wires currently in the range index with the x position
      # of the vertical wire being seen at an x location.
      # 3. Remove the horizontal wires ending at the current x position being sweeped.
      # 
      # Essentially, all events should be processed in order of x positions. When the
      # x positions of events do overlap, add must be done first, then query, then remove.
      if event_type == 'add':
        # Only this pair of values are needed for the AVL tree to find the position of the element in O(logn) time.
        self.index.add(KeyWirePair(wire.y1, wire))
      elif event_type == 'query':
        self.trace_sweep_line(event_x)
        if count_only:
          result += self.index.count(KeyWirePairL(wire.y1), KeyWirePairH(wire.y2))
        else:
          cross_wires = self.index.list(KeyWirePairL(wire.y1), KeyWirePairH(wire.y2))
          for cross_wire in cross_wires:
            result.add_crossing(wire, cross_wire.wire)
      elif event_type == 'delete':
        self.index.delete(KeyWirePair(wire.y1, wire))

    return result
  
  def trace_sweep_line(self, x):
    """When tracing is enabled, adds info about where the sweep line is.
    
    Args:
      x: the coordinate of the vertical sweep line
    """
    # NOTE: this is overridden in TracedCrossVerifier
    pass

class TracedCrossVerifier(CrossVerifier):
  """Augments CrossVerifier to build a trace for the visualizer."""
  
  def __init__(self, layer):
    CrossVerifier.__init__(self, layer)
    self.trace = []
    self.index = TracedRangeIndex(self.trace)
    self.result_set = TracedResultSet(self.trace)
    
  def trace_sweep_line(self, x):
    self.trace.append({'type': 'sweep', 'x': x})
    
  def trace_as_json(self):
    """List that obeys the JSON format restrictions with the verifier trace."""
    return self.trace

# Command-line controller.
if __name__ == '__main__':
    import sys
    layer = WireLayer.from_file(sys.stdin)
    verifier = CrossVerifier(layer)
    
    if os.environ.get('TRACE') == 'jsonp':
      verifier = TracedCrossVerifier(layer)
      result = verifier.wire_crossings()
      json_obj = {'layer': layer.as_json(), 'trace': verifier.trace_as_json()}
      sys.stdout.write('onJsonp(')
      json.dump(json_obj, sys.stdout)
      sys.stdout.write(');\n')
    elif os.environ.get('TRACE') == 'list':
      verifier.wire_crossings().write_to_file(sys.stdout)
    else:
      sys.stdout.write(str(verifier.count_crossings()) + "\n")
