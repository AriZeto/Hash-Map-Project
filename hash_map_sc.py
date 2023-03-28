# Name: Ari Zeto
# OSU Email: zetoa@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6 (Portfolio)
# Due Date: March 17, 2023.
# Description: The program completes the HashMap class where a dynamic array
# is used to store the hash table and implements chaining.
# The implementation allows such that this hash map can have key-values
# inserted, removed, grabbed, table resized, or other various needs.
# Additionally, a function outside the class is designed to find the mode and
# frequency of items in a dynamic array.

from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

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
        Increment from given number and the find the closest prime number
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
        key already exists in the hash map, it's associated value must be
        replaced by the new value. If the given key is not in the hash map,
        a new key/value pair must be added.

        Takes 'key' (str), 'value' (object) as parameters.

        Returns None.
        """

        # Resize to double its current capacity when called and if current
        # load factor is >= 1.
        if self.table_load() >= 1:
            self.resize_table(self._capacity * 2)

        # Grab the capacity of the bucket.
        capacity_bucket = self._buckets.length()

        # Determine the index for where the key value pair will go.
        hash_value = self._hash_function(key)
        index_value = hash_value % capacity_bucket

        # Check if index position in bucket contains key in Node.
        the_node = self._buckets[index_value].contains(key)
        if the_node is not None: # If node exists, replace w/ new value.
            the_node.value = value
        else:
            # Insert the key value pair into the bucket, increment size.
            self._buckets[index_value].insert(key, value)
            self._size += 1


    def empty_buckets(self) -> int:
        """
        This method returns the number of empty buckets in the hash table.

        Takes no parameters.

        Returns the number of empty buckets in hash table.
        """

        # Define counter for empty bucket.
        empty_buckets = 0

        # Loop over the bucket.
        for i in range(self._buckets.length()):
            if self._buckets[i].length() == 0:
                empty_buckets += 1 # If length of bucket is 0, increment count.

        return empty_buckets


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

    def clear(self) -> None:
        """
        This method clears the contents of the hash map. Does not change the
        underlying hash table capacity.

        Takes no parameters.

        Returns None.
        """

        # Clear by setting new Hashmap and set prior buckets to new buckets.
        new_hash = HashMap(self._capacity, self._hash_function)
        self._buckets = new_hash._buckets
        self._size = 0 # Reset size.

    def resize_table(self, new_capacity: int) -> None:
        """
        This method changes the capacity of the internal hash table. ALl
        existing key/value pairs must remain in the new hash map, and all
        hash table links must be rehashed.

        Takes 'new_capacity' as parameter (int).

        Returns None.
        """

        # Return if the capacity is less than 1.
        if new_capacity < 1:
            return

        # If the new capacity is not Prime, set new capacity to next prime.
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # Set capacity.
        self._capacity = new_capacity

        # # Save old buckets.
        old_buckets = self._buckets

        # Create new dynamic array and set buckets to it.
        new_da = DynamicArray()
        self._buckets = new_da

        # Fill with linked lists.
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        # Reset size for new buckets.
        self._size = 0

        # Copy contents over from old buckets to new hash map.
        for i in range(old_buckets.length()):
            the_bucket = old_buckets.get_at_index(i) # Grab bucket
            if the_bucket.length() != 0: # If bucket is not empty.

                # Define iterator for linked list to use on bucket, then
                # define pointer for the current node using iterator.
                linked_list_iterator = iter(the_bucket)
                current_node = next(linked_list_iterator)

                # Loop through each item in the bucket to gather key, rehash.
                while current_node is not None:

                    # Grab the key, value since Node, to be used for 'put()'.
                    grab_key = current_node.key
                    grab_value = current_node.value
                    current_node = current_node.next # Set next node.

                    # Rehash the key by using 'put()'.
                    self.put(grab_key, grab_value)


    def get(self, key: str):
        """
        This method returns the value associated with the given key. If the key
        is not in the hash map, return None.

        Takes 'key' (str) as a parameter.

        Returns an object.
        """

        # Grab the capacity of the bucket.
        capacity_bucket = self._buckets.length()

        # Determine the index for where the key value pair will go.
        hash_value = self._hash_function(key)
        index_value = hash_value % capacity_bucket

        # Check if index position in bucket contains key in Node.
        the_node = self._buckets[index_value].contains(key)

        # If the key is in a bucket, return node's value, None otherwise.
        if the_node is not None and the_node.key == key:
            return the_node.value


    def contains_key(self, key: str) -> bool:
        """
        This method returns True if the given key is in the hash map, otherwise
        returns False. An empty hash map does not contain any keys.

        Takes 'key' (str) as parameter.

        Returns bool.
        """

        # Grab the capacity of the bucket.
        capacity_bucket = self._buckets.length()

        # Determine the index for where the key value pair will go.
        hash_value = self._hash_function(key)
        index_value = hash_value % capacity_bucket

        # Check if index position in bucket contains key in Node.
        the_node = self._buckets[index_value].contains(key)

        # If some bucket contains the key passed in, return True.
        if the_node is not None and the_node.key == key:
            return True

        # Return False if the key is not found.
        return False


    def remove(self, key: str) -> None:
        """
        This method removes the given key and its associated value from the
        hash map. If the key is not in the hash map, this method does nothing.

        Takes 'key' (str) as parameter.

        Returns None.
        """

        # Grab the capacity of the bucket.
        capacity_bucket = self._buckets.length()

        # Determine the index for where the key value pair will go.
        hash_value = self._hash_function(key)
        index_value = hash_value % capacity_bucket

        # If the key is not in the bucket.
        if not self._buckets[index_value].contains(key):
            return

        # Find node at the index value is and remove the node/ key-value pair.
        self._buckets[index_value].remove(key)

        # Decrement size.
        self._size -= 1


    def get_keys_and_values(self) -> DynamicArray:
        """
        This method returns a dynamic array where each index contains a tuple
        of a key/value pair stored in the hash map. Order of keys in array
        does not matter.

        Takes no parameters.

        Returns a dynamic array.
        """

        # Set dynamic array that will contain tuple.
        new_da = DynamicArray()

        # Loop through buckets to find keys & values.
        for i in range(self._buckets.length()):
            the_bucket = self._buckets.get_at_index(i) # Grab bucket
            if the_bucket.length() != 0: # If bucket is not empty.

                # Define iterator for linked list to use on bucket, then
                # define pointer for the current node using iterator.
                linked_list_iterator = iter(the_bucket)
                current_node = next(linked_list_iterator)

                # Loop through each item in the bucket to gather key-value.
                while current_node is not None:

                    # Grab the key, value since Node.
                    grab_key = current_node.key
                    grab_value = current_node.value

                    # Define a tuple containing the key and value.
                    my_tuple = (grab_key, grab_value)

                    # Append the tuple to the dynamic array.
                    new_da.append(my_tuple)

                    # Set next node.
                    current_node = current_node.next

        return new_da


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    This function receives a dynamic array (not guaranteed to be sorted) that
    returns a tuple containing a dynamic array comprising the mode of the
    values, and an integer representing the highest frequency. This function
    runs at O(n) time complexity.

    Takes 'da' (dynamic array) as a parameter.

    Returns a tuple containing a dynamic array comprised of mode, then frequency.
    """

    # if you'd like to use a hash map,
    # use this instance of your Separate Chaining HashMap
    map = HashMap()

    # Array to be returned.
    new_da = DynamicArray()

    # Define counter for highest frequency.
    highest_freq_seen = 0

    # Looping over the length of the da to fill hash map with items (keys) and
    # frequencies (values).
    for i in range(da.length()):
        an_item = da.get_at_index(i)  # Grab item (key).

        # If there is no key, initialize frequency to 1.
        if not map.contains_key(an_item):
            map.put(an_item, 1) # Initialize frequency to '1'.

            # Set highest frequency based on frequency seen in loop.
            if 1 > highest_freq_seen:
                highest_freq_seen = 1

        # If the key already exists in the hash map.
        else:
            current_freq = map.get(an_item) # Returns a value (frequency, starts at 1).
            map.put(an_item, current_freq + 1) # Increment frequency

            # Set highest frequency based on frequency seen in loop.
            if current_freq + 1 > highest_freq_seen:
                highest_freq_seen = current_freq + 1

    # Grab keys and values from filled map, returns dynamic array.
    # Need to loop over this.
    items_freq_da = map.get_keys_and_values()

    # Loop through new dynamic array from 'get_keys_and_values', append to
    # the new dynamic array.
    for j in range(items_freq_da.length()):
        the_item = items_freq_da[j][0] # get keys
        the_freq = items_freq_da[j][1] # get values

        # Only append if the frequency is the highest frequency seen.
        if the_freq == highest_freq_seen:
            new_da.append(the_item)

    # Return the new da consisting of the mode, as well as return highest freq.
    return new_da, highest_freq_seen

# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    # print("\nPDF - put example 1")
    # print("-------------------")
    # m = HashMap(53, hash_function_1)
    # for i in range(150):
    #     m.put('str' + str(i), i * 100)
    #     if i % 25 == 24:
    #         print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())
    #
    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())
    #
    # print("\nPDF - empty_buckets example 1")
    # print("-----------------------------")
    # m = HashMap(101, hash_function_1)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key1', 10)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key2', 20)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key1', 30)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key4', 40)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    #
    # print("\nPDF - empty_buckets example 2")
    # print("-----------------------------")
    # m = HashMap(53, hash_function_1)
    # for i in range(150):
    #     m.put('key' + str(i), i * 100)
    #     if i % 30 == 0:
    #         print(m.empty_buckets(), m.get_size(), m.get_capacity())
    #
    # print("\nPDF - table_load example 1")
    # print("--------------------------")
    # m = HashMap(101, hash_function_1)
    # print(round(m.table_load(), 2))
    # m.put('key1', 10)
    # print(round(m.table_load(), 2))
    # m.put('key2', 20)
    # print(round(m.table_load(), 2))
    # m.put('key1', 30)
    # print(round(m.table_load(), 2))
    #
    # print("\nPDF - table_load example 2")
    # print("--------------------------")
    # m = HashMap(53, hash_function_1)
    # for i in range(50):
    #     m.put('key' + str(i), i * 100)
    #     if i % 10 == 0:
    #         print(round(m.table_load(), 2), m.get_size(), m.get_capacity())
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
    # print("\nPDF - resize example 0")
    # print("----------------------")
    # m = HashMap(97, hash_function_1)
    # # m.resize_table(1)
    # # m.resize_table(3)
    # # m.resize_table(2)
    #
    # print("\nPDF - resize example 1")
    # print("----------------------")
    # m = HashMap(23, hash_function_1)
    # m.put('key1', 10)
    # print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    # m.resize_table(30)
    # print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    #
    # print("\nPDF - resize example 2")
    # print("----------------------")
    # m = HashMap(79, hash_function_2)
    # keys = [i for i in range(1, 1000, 13)]
    # for key in keys:
    #     m.put(str(key), key * 42)
    # print(m.get_size(), m.get_capacity())
    #
    # # # # # I ADDED THIS LINE:
    # # # # # m.resize_table(2)
    #
    # for capacity in range(111, 1000, 117):
    #     m.resize_table(capacity)
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

    # print("\nPDF - get example 1")
    # print("-------------------")
    # m = HashMap(31, hash_function_1)
    # print(m.get('key'))
    # m.put('key1', 10)
    # print(m.get('key1'))

    # print("\nPDF - get example 2")
    # print("-------------------")
    # m = HashMap(151, hash_function_2)
    # for i in range(200, 300, 7):
    #     m.put(str(i), i * 10)
    # print(m.get_size(), m.get_capacity())
    # for i in range(200, 300, 21):
    #     print(i, m.get(str(i)), m.get(str(i)) == i * 10)
    #     print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)
    #
    # print("\nPDF - contains_key example 1")
    # print("----------------------------")
    # m = HashMap(53, hash_function_1)
    # print(m.contains_key('key1'))
    # m.put('key1', 10)
    # m.put('key2', 20)
    # m.put('key3', 30)
    # print(m.contains_key('key1'))
    # print(m.contains_key('key4'))
    # print(m.contains_key('key2'))
    # print(m.contains_key('key3'))
    # m.remove('key3')
    # print(m.contains_key('key3'))

    # print("\nPDF - contains_key example 2")
    # print("----------------------------")
    # m = HashMap(79, hash_function_2)
    # keys = [i for i in range(1, 1000, 20)]
    # for key in keys:
    #     m.put(str(key), key * 42)
    # print(m.get_size(), m.get_capacity())
    # result = True
    # for key in keys:
    #     # all inserted keys must be present
    #     result &= m.contains_key(str(key))
    #     # NOT inserted keys must be absent
    #     result &= not m.contains_key(str(key + 1))
    # print(result)
    #
    # print("\nPDF - remove example 1")
    # print("----------------------")
    # m = HashMap(53, hash_function_1)
    # print(m.get('key1'))
    # m.put('key1', 10)
    # print(m.get('key1'))
    # m.remove('key1')
    # print(m.get('key1'))
    # m.remove('key4')
    #
    # print("\nPDF - get_keys_and_values example 1")
    # print("------------------------")
    # m = HashMap(11, hash_function_2)
    # for i in range(1, 6):
    #     m.put(str(i), str(i * 10))
    # print(m.get_keys_and_values())
    #
    # m.put('20', '200')
    # m.remove('1')
    # m.resize_table(2)
    # print(m.get_keys_and_values())
    #
    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
