# Name: Ari Zeto
# OSU Email: zetoa@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6 (Portfolio)
# Due Date: March 17, 2023.
# Description: The program completes the HashMap class where a dynamic array
# is used to store the hash table and implements open addressing.
# The implementation allows such that this hash map can have key-values
# inserted, removed, grabbed, table resized, or other various needs.
# Additionally, methods to iterate over the hash map and returning the next
# item from the hash map are also defined.

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        This method updates the key/value pair in the hash map. If the given
        key already exists in the hash map, its associate value must be
        replaced by the new value. If the given key is not in the hash map, a
        new key/value pair must be added.

        Takes 'key' (str), 'value' (object) as parameters.

        Returns None.
        """

        # Resize to double its current capacity when called and if current
        # load factor is >= 0.5.
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity * 2)

        # Grab the capacity of the bucket.
        capacity_bucket = self._buckets.length()

        # Determine the index.
        hash_value = self._hash_function(key)
        index_value = hash_value % capacity_bucket

        # Define the hash entry.
        hash_entry = HashEntry(key, value)

        # Try inserting element into hash map, increment size (when None or
        # tombstone is placed).
        if self._buckets[index_value] is None or self._buckets[index_value].is_tombstone == True:
            self._buckets.set_at_index(index_value, hash_entry)
            self._size += 1 # Increment size.

        # Or, update at index, do not increment size.
        elif self._buckets[index_value].key == key:
            self._buckets.set_at_index(index_value, hash_entry)

        # Otherwise, loop through and find next spot by quadratic probing
        # to insert in locations.
        else:
            for j in range(1, self._buckets.length()): # Where j starts at 1.
                i = (index_value + j ** 2) % self._capacity # Where 'i' represents index value w/quadratic probing, wrap around.

                # Try inserting element, increment size (when None or tombstone
                # is placed).
                if self._buckets[i] is None or self._buckets[i].is_tombstone == True:
                    self._buckets.set_at_index(i, hash_entry)
                    self._size += 1  # Increment size.
                    return # Return since insertion is complete.

                # Update at index, do not increment size.
                elif self._buckets[i].key == key:
                    self._buckets.set_at_index(i, hash_entry)
                    return # Return since insertion is complete.


    def table_load(self) -> float:
        """
        This method returns the current hash table load factor.

        Takes no parameters.

        Returns the current hash table load factor.
        """

        # Determine the load factor.
        num_elements_stored = self.get_size()
        num_buckets = self.get_capacity()
        load_factor = num_elements_stored / num_buckets

        return load_factor

    def empty_buckets(self) -> int:
        """
        This method returns the number of empty buckets in the hash table.

        Takes no parameters.

        Returns an integer.
        """

        # Define counter for empty bucket.
        empty_buckets = 0

        # Loop over the buckets.
        for i in range(self._buckets.length()):
            if self._buckets[i] is None:
                empty_buckets += 1 # If bucket contains None, increment count.
        return empty_buckets

    def resize_table(self, new_capacity: int) -> None:
        """
        This method changes the capacity of the internal hash table. All
        existing key/value pairs must remain in the new hash map, and all hash
        table links must be rehashed.

        Takes 'new_capacity' (int) as parameter.

        Returns None.
        """

        # Return if the capacity is less than the size.
        if new_capacity < self.get_size():
            return

        # If the new capacity is not Prime, set new capacity to next prime.
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # Set the capacity.
        self._capacity = new_capacity

        # # Save old buckets, so we may loop over them.
        old_buckets = self._buckets

        # Create new dynamic array, setting buckets.
        new_da = DynamicArray()
        self._buckets = new_da

        # Fill buckets with 'None' to initialize.
        for _ in range(self._capacity):
            self._buckets.append(None)

        # Reset size for new buckets.
        self._size = 0

        # Loop over the old buckets and copy contents over from old hash map
        # to the new hash map.
        for i in range(old_buckets.length()):
            the_bucket = old_buckets.get_at_index(i)  # Grab bucket

            # Put the keys and values into the hashmap if bucket has items.
            if the_bucket is not None:
                grab_key = the_bucket.key
                grab_value = the_bucket.value
                self.put(grab_key, grab_value)

    def get(self, key: str) -> object:
        """
        This method returns the value associated with the given key. If the key
        is not in the hash map, the method returns None.

        Takes 'key' (str) as a parameter.

        Returns an object (value of given key).
        """

        # Grab the capacity of the bucket.
        capacity_bucket = self._buckets.length()

        # Determine the index.
        hash_value = self._hash_function(key)
        index_value = hash_value % capacity_bucket

        # If location is None, return None (no value).
        if self._buckets[index_value] is None:
            return None

        # Check if key is located at initial index, return Value.
        elif self._buckets[index_value].key == key:
            # Return None if tombstone is placed there.
            if self._buckets[index_value].is_tombstone == True:
                return None
            return self._buckets.get_at_index(index_value).value

        # Otherwise, loop through and find key at other possible indices.
        else:
            for j in range(1, self._buckets.length()): # Where j starts at '1'.
                i = (index_value + j ** 2) % self._capacity  # Where 'i' represents index value w/quadratic probing, wrap around.

                # If location is None, return None (no value)
                if self._buckets[i] is None:
                    return None

                # Check if key is located at possible indices, return value.
                elif self._buckets[i].key == key:
                    # Return None if tombstone is placed there.
                    if self._buckets[i].is_tombstone == True:
                        return None
                    return self._buckets.get_at_index(i).value


    def contains_key(self, key: str) -> bool:
        """
        This method returns True if the given key is in the hash map, otherwise
        it returns False. An empty hash map does not contain any keys.

        Takes 'key' (str) as parameter.

        Returns bool.
        """

        # Grab the capacity of the bucket.
        capacity_bucket = self._buckets.length()

        # Determine the index.
        hash_value = self._hash_function(key)
        index_value = hash_value % capacity_bucket

        # If location is None, return False.
        if self._buckets[index_value] is None:
            return False

        # Check if key is located at initial index, return True.
        elif self._buckets[index_value].key == key:
            # Return False if tombstone is placed there.
            if self._buckets[index_value].is_tombstone == True:
                return False
            return True

        # Otherwise, loop through and to find key at other possible indices.
        else:
            for j in range(1, self._buckets.length()): # Where 'j' starts at 1
                i = (index_value + j ** 2) % self._capacity  # Where 'i' represents index value w/quadratic probing, wrap around.

                # If location is None, return False.
                if self._buckets[i] is None:
                    return False

                # Check if key is located at possible indices, return True.
                elif self._buckets[i].key == key:
                    # Return False if tombstone is placed there.
                    if self._buckets[i].is_tombstone == True:
                        return False
                    return True


    def remove(self, key: str) -> None:
        """
        This method removes the given key and its associated value from the
        hash map. If the key is not in the hash map, the method does nothing.

        Takes 'key' (str) as parameter.

        Returns None.
        """

        # Grab the capacity of the bucket.
        capacity_bucket = self._buckets.length()

        # Determine the index.
        hash_value = self._hash_function(key)
        index_value = hash_value % capacity_bucket

        # If location is None, return.
        if self._buckets[index_value] is None:
            return

        # Check if key is located at index, remove by setting tombstone.
        elif self._buckets[index_value].key == key:

            # If the value there is already a tombstone, return (do nothing).
            if self._buckets[index_value].is_tombstone == True:
                return

            #  Set tombstone status, decrement size.
            self._buckets.get_at_index(index_value).is_tombstone = True
            self._size -= 1

        # Otherwise, loop through and to find key at other possible indices.
        else:
            for j in range(1, self._buckets.length()): # Where 'j' starts at 1.
                i = (index_value + j ** 2) % self._capacity  # Where 'i' represents index value w/quadratic probing, wrap around.

                # If location is None, return.
                if self._buckets[i] is None:
                    return

                # Check if key is located at possible indices, remove by
                # setting tombstone.
                elif self._buckets[i].key == key:

                    # If the value there is already a tombstone, return (do nothing).
                    if self._buckets[i].is_tombstone == True:
                        return

                    # Set tombstone status, decrement size.
                    self._buckets.get_at_index(i).is_tombstone = True
                    self._size -= 1
                    return # Don't continue looping after setting tombstone.


    def clear(self) -> None:
        """
        This method clears the contents of the hash map. It does not change
        the underlying table capacity.

        Takes no parameters.

        Returns None.
        """

        # Clear by setting new Hashmap and set prior buckets to new buckets.
        new_hash = HashMap(self._capacity, self._hash_function)
        self._buckets = new_hash._buckets
        self._size = 0 # Reset size.

    def get_keys_and_values(self) -> DynamicArray:
        """
        This method returns a dynamic array where each index contains a tuple
        of a key/value pair stored in the hash map. The order of the keys in
        the dynamic array does not matter.

        Takes no parameters.

        Returns dynamic array.
        """

        # Set new dynamic array, will contain tuple of key-values.
        new_da = DynamicArray()

        # Loop over the buckets.
        for i in range(self._buckets.length()):
            the_bucket = self._buckets.get_at_index(i)  # Grab bucket

            # If the bucket is not empty and is not a tombstone, grab key,
            # value, set as tuple, and append it the new dynamic array.
            if the_bucket is not None and the_bucket.is_tombstone == False:
                grab_key = the_bucket.key
                grab_value = the_bucket.value
                my_tuple = (grab_key, grab_value)
                new_da.append(my_tuple)

        return new_da

    def __iter__(self):
        """
        This method enables the hash map to iterate across itself.

        Takes no parameters.

        Returns self.
        """

        # Define and initialize index, used in __next()__.
        self._index = 0

        return self

    def __next__(self):
        """
        This method will return the next item in the hash map, iterating over
        the active items.

        Takes no parameters.

        Returns value.
        """

        # Based on an exploration in our class.
        try:
            # Iterate over the active items.
            while self._buckets[self._index] is None:
                self._index = self._index + 1 # Increment when None.
            value = self._buckets[self._index] # Define value.
        except DynamicArrayException:
            raise StopIteration

        self._index = self._index + 1

        return value


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    # print("\nPDF - resize example 2")
    # print("----------------------")
    # m = HashMap(79, hash_function_2)
    # keys = [i for i in range(1, 1000, 13)]
    # for key in keys:
    #     m.put(str(key), key * 42)
    # print(m.get_size(), m.get_capacity())
    #
    # for capacity in range(111, 1000, 117):
    #     m.resize_table(capacity)
    #
    #     if m.table_load() > 0.5:
    #         print(f"Check that the load factor is acceptable after the call to resize_table().\n"
    #               f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")
    #
    #     m.put('some key', 'some value')
    #     result = m.contains_key('some key')
    #     m.remove('some key')
    #
    #     for key in keys:
    #         # all inserted keys must be present
    #         result &= m.contains_key(str(key))
    #         # NOT inserted keys must be absent
    #         result &= not m.contains_key(str(key + 1))
    #     print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))
    #
    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')
    #
    # print("\nPDF - clear example 1")
    # print("---------------------")
    # m = HashMap(101, hash_function_1)
    # print(m.get_size(), m.get_capacity())
    # m.put('key1', 10)
    # m.put('key2', 20)
    # m.put('key1', 30)
    # print(m.get_size(), m.get_capacity())
    # m.clear()
    # print(m.get_size(), m.get_capacity())
    #
    # print("\nPDF - clear example 2")
    # print("---------------------")
    # m = HashMap(53, hash_function_1)
    # print(m.get_size(), m.get_capacity())
    # m.put('key1', 10)
    # print(m.get_size(), m.get_capacity())
    # m.put('key2', 20)
    # print(m.get_size(), m.get_capacity())
    # m.resize_table(100)
    # print(m.get_size(), m.get_capacity())
    # m.clear()
    # print(m.get_size(), m.get_capacity())
    #
    # print("\nPDF - get_keys_and_values example 1")
    # print("------------------------")
    # m = HashMap(11, hash_function_2)
    # for i in range(1, 6):
    #     m.put(str(i), str(i * 10))
    # print(m.get_keys_and_values())
    #
    # m.resize_table(2)
    # print(m.get_keys_and_values())
    #
    # m.put('20', '200')
    # m.remove('1')
    # m.resize_table(12)
    # print(m.get_keys_and_values())
    #
    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    # print("\nPDF - __iter__(), __next__() example 2")
    # print("---------------------")
    # m = HashMap(10, hash_function_2)
    # for i in range(5):
    #     m.put(str(i), str(i * 24))
    # m.remove('0')
    # m.remove('4')
    # print(m)
    # for item in m:
    #     print('K:', item.key, 'V:', item.value)
