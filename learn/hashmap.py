def new(num_buckets=256):
    """Initializes a Map with the given number of buckets."""
    aMap = []
    for i in range(num_buckets):
        aMap.append([])
    return aMap

def hash_key(aMap, key):
    """Given a key this will create a number and then convert an
    index for the aMap's buckets."""
    return hash(key) % len(aMap)

def get_bucket(aMap, key):
    """Given the key, find its corresponding index and return
    the bucket of that index within the aMap."""
    index = hash_key(aMap, key)
    return aMap[index]

def get_slot(aMap, key, default=None):
    """
    Returns the index, key, and value of a slot in a bucket.
    Returns -1, key, and default (None if not set) when not found.
    """
    bucket = get_bucket(aMap, key)
    if bucket:
        for i, kv in enumerate(bucket):
            k, v = kv
            if k == key:
                return i, k, v
    return -1, key, default

def get(aMap, key, default=None):
    """Gets the value in a bucket for the given key, or the default"""
    return get_slot(aMap, key, default)[2]

def set(aMap, key, value):
    """Sets the key to the value, replacing any existing value."""
    i, k, v = get_slot(aMap, key)
    # bucket has to be defined here because it is possible that
    # it will never be initialized until the append statement.
    bucket = get_bucket(aMap, key)

    # If the key is found in the bucket
    if i >= 0:
        bucket[i][1] = value
        return
    # If the key could not be found in the bucket.
    bucket.append((key, value))

def delete(aMap, key):
    """Deletes the given key from the Map."""
    bucket = get_bucket(aMap, key)
    for i in xrange(len(bucket)):
        if bucket[i][0] == key:
            del bucket[i]
    """
    # Alternate Solution:
    i, k, v = get_slot(aMap, key)
    if i >= 0:
        bucket = get_bucket(aMap, key)
        return bucket.pop(i)[1]
    """

def list(aMap):
    """Prints out what's in the Map."""
    for bucket in aMap:
        for k, v in bucket:
            print "key:", k, "value:", v