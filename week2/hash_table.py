import random, sys, time

###########################################################################
#                                                                         #
# Implement a hash table from scratch! (⑅•ᴗ•⑅)                            #
#                                                                         #
# Please do not use Python's dictionary or Python's collections library.  #
# The goal is to implement the data structure yourself.                   #
#                                                                         #
###########################################################################

# Hash function.
#
# |key|: string
# Return value: a hash value
def calculate_hash(key):
    """
    Calculate hash using the given key.
    Using hint3 from slides. (Think about alice and elica for this code.)
    """
    assert type(key) == str
    hash = 0
    for c in key:
        hash = (hash * 31 + ord(c)) % 1000000007 #文字の順番を区別する、素数で衝突を減らす
    return hash

# An item object that represents one key - value pair in the hash table.
class Item:
    # |key|: The key of the item. The key must be a string.
    # |value|: The value of the item.
    # |next|: The next item in the linked list. If this is the last item in the
    #         linked list, |next| is None.
    def __init__(self, key, value, next):
        assert type(key) == str
        self.key = key
        self.value = value
        self.next = next


# The main data structure of the hash table that stores key - value pairs.
# The key must be a string. The value can be any type.
#
# |self.bucket_size|: The bucket size.#バケットのサイズ
# |self.buckets|: An array of the buckets. self.buckets[hash % self.bucket_size]
#                 stores a linked list of items whose hash value is |hash|.#実際の保存領域
# |self.item_count|: The total number of items in the hash table.
class HashTable:

    # Initialize the hash table.
    def __init__(self):
        # Set the initial bucket size to 97. A prime number is chosen to reduce
        # hash conflicts.
        self.bucket_size = 97
        self.buckets = [None] * self.bucket_size
        self.item_count = 0

    # Put an item to the hash table. If the key already exists, the
    # corresponding value is updated to a new value.
    #
    # |key|: The key of the item.
    # |value|: The value of the item.
    # Return value: True if a new item is added. False if the key already exists
    #               and the value is updated.

    def put(self, key, value, check=True):
        assert type(key) == str
        if check:
            self.expand_hash()
            self.check_size() # Note: Don't remove this code.
        bucket_index = calculate_hash(key) % self.bucket_size #キーがどのバケットに入っているか
        item = self.buckets[bucket_index] #そのバケットに入っているアイテム（連結リストの先頭）を取得
        while item:
            if item.key == key:
                item.value = value
                return False
            item = item.next
        new_item = Item(key, value, self.buckets[bucket_index])
        self.buckets[bucket_index] = new_item
        self.item_count += 1
        return True

    # Get an item from the hash table.
    #
    # |key|: The key.
    # Return value: If the item is found, (the value of the item, True) is
    #               returned. Otherwise, (None, False) is returned.
    def get(self, key):
        assert type(key) == str
        self.check_size() # Note: Don't remove this code.
        bucket_index = calculate_hash(key) % self.bucket_size #キーがどのバケットに入っているか
        item = self.buckets[bucket_index] #そのバケットに入っているアイテム（連結リストの先頭）を取得
        while item:
            if item.key == key:
                return (item.value, True)
            item = item.next
        return (None, False)

    # Delete an item from the hash table.
    #
    # |key|: The key.
    # Return value: True if the item is found and deleted successfully. False
    #               otherwise.
    def delete(self, key):
        assert type(key) == str
        self.check_size()  # Note: Don't remove this code.
        bucket_index = calculate_hash(key) % self.bucket_size

        prev = None
        curr = self.buckets[bucket_index]
        while curr is not None:
            if curr.key == key:
                if prev is None:
                    self.buckets[bucket_index] = curr.next
                else:
                    prev.next = curr.next
                self.item_count -= 1
                self.shrink_hash()
                return True
            prev = curr
            curr = curr.next
        return False

        pass

    def resize(self, new_size):
        """Resize the hash function"""
        new_size = next_prime(new_size)
        old_buckets = self.buckets
        self.buckets = [None] * new_size
        self.bucket_size = new_size
        self.item_count = 0

        for bucket in old_buckets:
            item = bucket
            while item is not None:
                self.put(item.key, item.value, check=False)
                item = item.next

    def expand_hash(self):
        """
        Double the hash table size if the load factor exceeds 70%.

        This function checks the current load factor (item_count / bucket_size),
        and if it's greater than 0.7, it resizes the hash table to twice its current size
        to maintain efficient performance (average-case O(1) operations).
        """
        load_factor = self.item_count / self.bucket_size
        if load_factor > 0.7:
            self.resize(self.bucket_size * 2)

    def shrink_hash(self):
        """
        Halve the hash table size if the load factor drops below 30%.

        This function checks whether the current load factor (item_count / bucket_size)
        is less than 0.3. If so, and if the current bucket size is greater than the
        initial size (97), it shrinks the table by resizing it to half its current size.

        Shrinking the table helps save memory when the table is under-utilized,
        while maintaining a reasonable load factor for performance.
        :return:
        """
        load_factor = self.item_count / self.bucket_size
        if self.bucket_size > 97 and load_factor < 0.3:
            self.resize(self.bucket_size // 2)


    # Return the total number of items in the hash table.
    def size(self):
        return self.item_count

    # Check that the hash table has a "reasonable" bucket size.
    # The bucket size is judged "reasonable" if it is smaller than 100 or
    # the buckets are 30% or more used.
    #
    # Note: Don't change this function.
    def check_size(self):
        assert (self.bucket_size < 100 or
                self.item_count >= self.bucket_size * 0.3)


def next_prime(n):
    """Return the next prime number"""
    def is_prime(x):
        """Return True if the number is prime number otherwise, return False."""
        if x <= 1:
            return False
        for i in range(2, int(x ** 0.5) + 1):
            if x % i == 0:
                return False
        return True
    while not is_prime(n):
        n += 1
    return n


# Test the functional behavior of the hash table.
def functional_test():
    hash_table = HashTable()

    assert hash_table.put("aaa", 1) == True
    assert hash_table.get("aaa") == (1, True)
    assert hash_table.size() == 1

    assert hash_table.put("bbb", 2) == True
    assert hash_table.put("ccc", 3) == True
    assert hash_table.put("ddd", 4) == True
    assert hash_table.get("aaa") == (1, True)
    assert hash_table.get("bbb") == (2, True)
    assert hash_table.get("ccc") == (3, True)
    assert hash_table.get("ddd") == (4, True)
    assert hash_table.get("a") == (None, False)
    assert hash_table.get("aa") == (None, False)
    assert hash_table.get("aaaa") == (None, False)
    assert hash_table.size() == 4

    assert hash_table.put("aaa", 11) == False
    assert hash_table.get("aaa") == (11, True)
    assert hash_table.size() == 4

    assert hash_table.delete("aaa") == True
    assert hash_table.get("aaa") == (None, False)
    assert hash_table.size() == 3

    assert hash_table.delete("a") == False
    assert hash_table.delete("aa") == False
    assert hash_table.delete("aaa") == False
    assert hash_table.delete("aaaa") == False

    assert hash_table.delete("ddd") == True
    assert hash_table.delete("ccc") == True
    assert hash_table.delete("bbb") == True
    assert hash_table.get("aaa") == (None, False)
    assert hash_table.get("bbb") == (None, False)
    assert hash_table.get("ccc") == (None, False)
    assert hash_table.get("ddd") == (None, False)
    assert hash_table.size() == 0

    assert hash_table.put("abc", 1) == True
    assert hash_table.put("acb", 2) == True
    assert hash_table.put("bac", 3) == True
    assert hash_table.put("bca", 4) == True
    assert hash_table.put("cab", 5) == True
    assert hash_table.put("cba", 6) == True
    assert hash_table.get("abc") == (1, True)
    assert hash_table.get("acb") == (2, True)
    assert hash_table.get("bac") == (3, True)
    assert hash_table.get("bca") == (4, True)
    assert hash_table.get("cab") == (5, True)
    assert hash_table.get("cba") == (6, True)
    assert hash_table.size() == 6

    assert hash_table.delete("abc") == True
    assert hash_table.delete("cba") == True
    assert hash_table.delete("bac") == True
    assert hash_table.delete("bca") == True
    assert hash_table.delete("acb") == True
    assert hash_table.delete("cab") == True
    assert hash_table.size() == 0
    print("Functional tests passed!")


# Test the performance of the hash table.
#
# Your goal is to make the hash table work with mostly O(1).
# If the hash table works with mostly O(1), the execution time of each iteration
# should not depend on the number of items in the hash table. To achieve the
# goal, you will need to 1) implement rehashing (Hint: expand / shrink the hash
# table when the number of items in the hash table hits some threshold) and
# 2) tweak the hash function (Hint: think about ways to reduce hash conflicts).
def performance_test():
    hash_table = HashTable()

    for iteration in range(100):
        begin = time.time()
        random.seed(iteration)
        for i in range(10000):
            rand = random.randint(0, 100000000)
            hash_table.put(str(rand), str(rand))
        random.seed(iteration)
        for i in range(10000):
            rand = random.randint(0, 100000000)
            hash_table.get(str(rand))
        end = time.time()
        print("%d %.6f" % (iteration, end - begin))

    for iteration in range(100):
        random.seed(iteration)
        for i in range(10000):
            rand = random.randint(0, 100000000)
            hash_table.delete(str(rand))

    assert hash_table.size() == 0
    print("Performance tests passed!")


if __name__ == "__main__":
    functional_test()
    performance_test()
