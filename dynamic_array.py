# Name: Adam Spivak
# OSU Email: Spivaka@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 2
# Due Date: 10-28-24
# Description: Practices using Dynamic Arrays by implementing functionality
# # to manage it different operations.


from static_array import StaticArray


class DynamicArrayException(Exception):
    """
    Custom exception class to be used by Dynamic Array
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class DynamicArray:
    def __init__(self, start_array=None):
        """
        Initialize new dynamic array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._size = 0
        self._capacity = 4
        self._data = StaticArray(self._capacity)

        # populate dynamic array with initial values (if provided)
        # before using this feature, implement append() method
        if start_array is not None:
            for value in start_array:
                self.append(value)

    def __str__(self) -> str:
        """
        Return content of dynamic array in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = "DYN_ARR Size/Cap: "
        out += str(self._size) + "/" + str(self._capacity) + ' ['
        out += ', '.join([str(self._data[_]) for _ in range(self._size)])
        return out + ']'

    def __iter__(self):
        """
        Create iterator for loop
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._index = 0
        return self

    def __next__(self):
        """
        Obtain next value and advance iterator
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        try:
            value = self[self._index]
        except DynamicArrayException:
            raise StopIteration

        self._index += 1
        return value

    def get_at_index(self, index: int) -> object:
        """
        Return value from given index position
        Invalid index raises DynamicArrayException
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if index < 0 or index >= self._size:
            raise DynamicArrayException
        return self._data[index]

    def set_at_index(self, index: int, value: object) -> None:
        """
        Store value at given index in the array
        Invalid index raises DynamicArrayException
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if index < 0 or index >= self._size:
            raise DynamicArrayException
        self._data[index] = value

    def __getitem__(self, index) -> object:
        """
        Same functionality as get_at_index() method above,
        but called using array[index] syntax
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self.get_at_index(index)

    def __setitem__(self, index, value) -> None:
        """
        Same functionality as set_at_index() method above,
        but called using array[index] syntax
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.set_at_index(index, value)

    def is_empty(self) -> bool:
        """
        Return True is array is empty / False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size == 0

    def length(self) -> int:
        """
        Return number of elements stored in array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return the capacity of the array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    def print_da_variables(self) -> None:
        """
        Print information contained in the dynamic array.
        Used for testing purposes.
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        print(f"Length: {self._size}, Capacity: {self._capacity}, {self._data}")

    # -----------------------------------------------------------------------

    def resize(self, new_capacity: int) -> None:
        """
        Resizes the Dynamic array by creating a new static array and copying over
        the elements of the current array. It then sets the new array to be
        the underlying data structure for the Dynamic Array. The new array can only
        get larger.
        """
        if new_capacity > 0:
            if new_capacity >= self._size:
                newArr = StaticArray(new_capacity)

                for i in range(self._size):
                    newArr[i] = self._data[i]

                self._capacity = new_capacity
                self._data = newArr

    def append(self, value: object) -> None:
        """
        Appends new elements to the end of the dynamic array. It doubles if the
        self._size == self._capacity
        """
        if self._size < self._capacity:
            self._data[self._size] = value
        else:
            self.resize(self._capacity * 2)
            self._data[self._size] = value

        self._size += 1

    def insert_at_index(self, index: int, value: object) -> None:
        """
        Inserts element into the array at specific index. If array is full, it will
        double and then insert the new element.
        """
        if index < 0 or index > self._size:
            raise DynamicArrayException()

        if self._size == self._capacity:
            self.resize(self._capacity * 2)

        if index >= 0:
            if self._size == 1 and index == 0:
                self._data[index + 1] = self._data[index]
                self._data[index] = value
                self._size += 1
            else:
                for i in range(self._size, index, -1):
                    self._data[i] = self._data[i - 1]

                self._size += 1
                self._data[index] = value

    def remove_at_index(self, index: int) -> None:
        """
        Removes element at index specified from the parameter. It does so by shifting
        all the elements over to left using a for loop, starting at the removal index.
        If the size == capacity during removal, it sets the last element to None so when
        more elements are removed, it sets the element at the end of the list to None.
        """
        if index < 0 or index > self._size - 1:
            raise DynamicArrayException()

        quarterSize = 0.25 * self._capacity

        if self._size < quarterSize and self._capacity > 10:
            newCapacity = max(10, 2 * self._size)
            self.resize(newCapacity)

        for i in range(index, self._capacity):
            if i + 1 < self._capacity:
                self._data[i] = self._data[i + 1]

            if i + 1 == self._capacity:
                self._data[i] = None

        self._size -= 1

    def slice(self, start_index: int, size: int) -> "DynamicArray":
        """
        Returns a Dynamic array of elements "sliced" from the self._data array. Indexes
        from the parameter's start_index, and then
        """
        if start_index < 0 or size < 0 or start_index >= self._size or start_index + size > self._size:
            raise DynamicArrayException()

        newArr = DynamicArray()

        for i in range(start_index, start_index + size):
            newArr.append(self._data[i])

        return newArr

    def map(self, map_func) -> "DynamicArray":
        """
        Returns a new dynamic array that appends the elements of the original array
        after being run through the map function.
        """
        newArr = DynamicArray()

        for i in range(self._size):
            newArr.append(map_func(self._data[i]))

        return newArr

    def filter(self, filter_func) -> "DynamicArray":
        """
        A simple filter function that returns a new dynamic array
        with elements populated based on filter function returning true or false
        """
        newArr = DynamicArray()

        for i in range(self._size):
            if filter_func(self._data[i]):
                newArr.append(self._data[i])

        return newArr

    def reduce(self, reduce_func, initializer=None) -> object:
        """
        Like the filter and map function, this runs a function through the current
        array and returns a new piece of data. This reduce function iterates
        through the array and plugs in each element into the reduce function.
        If initializer is None, the first element becomes the initializer and starts
        running the reduce function on the second element. Else it will start with
        the initializer and first element.
        """
        if self._size == 0:
            return initializer

        if self._size == 1:
            if not initializer:
                return self._data[0]

        reductResult = 0

        for i in range(self._size):
            if not initializer:
                initializer = self._data[i]
                continue

            reductResult = reduce_func(initializer, self._data[i])
            initializer = reductResult

        return reductResult


def chunk(arr: DynamicArray) -> "DynamicArray":
    """
    Iterates through the Dynamic array from parameter and chunks it into
    different arrays with each element that is not in ascending order.
    If i < i + 1 it creates a new chunk, and appends its it to a new array
    that has all the created chunks."""
    chunksArr = DynamicArray()

    if arr.length() == 0:
        return chunksArr

    currChunk = DynamicArray()
    currChunk.append(arr[0])

    for i in range(1, arr.length()):
        if arr[i] >= arr[i - 1]:
            currChunk.append(arr[i])
        else:
            chunksArr.append(currChunk)
            currChunk = DynamicArray()
            currChunk.append(arr[i])

    chunksArr.append(currChunk)

    return chunksArr

def find_mode(arr: DynamicArray) -> tuple[DynamicArray, int]:
    """
    Finds the mode element from the arr in the parameter then appends
    it to the modeArray. It iterates through the array increasing the frequency
    with i + 1 == i, and stores the frequency in modeFreq if the current elements
    frequency is larger than the last. If the frequency is equal but not larger than
    modeFreq it adds to the modeArray as well. Returns a tuple of the modeArr
    and modeFreq
    """
    modeArr = DynamicArray()
    frequency = 1
    modeFreq = 1

    for i in range(arr.length()):
        if i + 1 < arr.length():
            if arr[i] == arr[i + 1]:
                frequency += 1
            else:
                if frequency == modeFreq:
                    modeArr.append(arr[i])

                elif frequency > modeFreq:
                    modeArr = DynamicArray()
                    modeArr.append(arr[i])
                    modeFreq = frequency

                frequency = 1

    if frequency > modeFreq:    # Account for last element
        modeArr = DynamicArray()
        modeArr.append(arr[arr.length() - 1])
        modeFreq = frequency
    elif frequency == modeFreq:
        modeArr.append(arr[arr.length() - 1])


    return modeArr, modeFreq

# ------------------- BASIC TESTING -----------------------------------------


if __name__ == "__main__":

    print("\n# resize - example 1")
    da = DynamicArray()

    # print dynamic array's size, capacity and the contents
    # of the underlying static array (data)
    da.print_da_variables()
    da.resize(8)
    da.print_da_variables()
    da.resize(2)
    da.print_da_variables()
    da.resize(0)
    da.print_da_variables()

    print("\n# resize - example 2")
    da = DynamicArray([1, 2, 3, 4, 5, 6, 7, 8])
    print(da)
    da.resize(20)
    print(da)
    da.resize(4)
    print(da)

    print("\n# append - example 1")
    da = DynamicArray()
    da.print_da_variables()
    da.append(1)
    da.print_da_variables()
    print(da)

    print("\n# append - example 2")
    da = DynamicArray()
    for i in range(9):
        da.append(i + 101)
        print(da)

    print("\n# append - example 3")
    da = DynamicArray()
    for i in range(600):
        da.append(i)
    print(da.length())
    print(da.get_capacity())

    print("\n# insert_at_index - example 1")
    da = DynamicArray([100])
    print(da)
    da.insert_at_index(0, 200)
    da.insert_at_index(0, 300)
    da.insert_at_index(0, 400)
    print(da)
    da.insert_at_index(3, 500)
    print(da)
    da.insert_at_index(1, 600)
    print(da)

    print("\n# insert_at_index example 2")
    da = DynamicArray()
    try:
        da.insert_at_index(-1, 100)
    except Exception as e:
        print("Exception raised:", type(e))
    da.insert_at_index(0, 200)
    try:
        da.insert_at_index(2, 300)
    except Exception as e:
        print("Exception raised:", type(e))
    print(da)

    print("\n# insert at index example 3")
    da = DynamicArray()
    for i in range(1, 10):
        index, value = i - 4, i * 10
        try:
            da.insert_at_index(index, value)
        except Exception as e:
            print("Cannot insert value", value, "at index", index)
    print(da)

    print("\n# remove_at_index - example 1")
    da = DynamicArray([10, 20, 30, 40, 50, 60, 70, 80])
    print(da)
    da.remove_at_index(0)
    print(da)
    da.remove_at_index(6)
    print(da)
    da.remove_at_index(2)
    print(da)

    print("\n# remove_at_index - example 2")
    da = DynamicArray([1024])
    print(da)
    for i in range(17):
        da.insert_at_index(i, i)
    print(da.length(), da.get_capacity())
    for i in range(16, -1, -1):
        da.remove_at_index(0)
    print(da)

    print("\n# remove_at_index - example 3")
    da = DynamicArray()
    print(da.length(), da.get_capacity())
    [da.append(1) for i in range(100)]  # step 1 - add 100 elements
    print(da.length(), da.get_capacity())
    [da.remove_at_index(0) for i in range(68)]  # step 2 - remove 68 elements
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 3 - remove 1 element
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 4 - remove 1 element
    print(da.length(), da.get_capacity())
    [da.remove_at_index(0) for i in range(14)]  # step 5 - remove 14 elements
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 6 - remove 1 element
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 7 - remove 1 element
    print(da.length(), da.get_capacity())

    for i in range(14):
        print("Before remove_at_index(): ", da.length(), da.get_capacity(), end="")
        da.remove_at_index(0)
        print(" After remove_at_index(): ", da.length(), da.get_capacity())

    print("\n# remove at index - example 4")
    da = DynamicArray([1, 2, 3, 4, 5])
    print(da)
    for _ in range(5):
        da.remove_at_index(0)
        print(da)

    print("\n# slice example 1")
    da = DynamicArray([1, 2, 3, 4, 5, 6, 7, 8, 9])
    da_slice = da.slice(1, 3)
    print(da, da_slice, sep="\n")
    da_slice.remove_at_index(0)
    print(da, da_slice, sep="\n")

    print("\n# slice example 2")
    da = DynamicArray([10, 11, 12, 13, 14, 15, 16])
    print("SOURCE:", da)
    slices = [(0, 7), (-1, 7), (0, 8), (2, 3), (5, 0), (5, 3), (6, 1), (6, -1)]
    for i, cnt in slices:
        print("Slice", i, "/", cnt, end="")
        try:
            print(" --- OK: ", da.slice(i, cnt))
        except:
            print(" --- exception occurred.")

    print("\n# map example 1")
    da = DynamicArray([1, 5, 10, 15, 20, 25])
    print(da)
    print(da.map(lambda x: x ** 2))

    print("\n# map example 2")


    def double(value):
        return value * 2


    def square(value):
        return value ** 2


    def cube(value):
        return value ** 3


    def plus_one(value):
        return value + 1


    da = DynamicArray([plus_one, double, square, cube])
    for value in [1, 10, 20]:
        print(da.map(lambda x: x(value)))

    print("\n# filter example 1")


    def filter_a(e):
        return e > 10


    da = DynamicArray([1, 5, 10, 15, 20, 25])
    print(da)
    result = da.filter(filter_a)
    print(result)
    print(da.filter(lambda x: (10 <= x <= 20)))

    print("\n# filter example 2")


    def is_long_word(word, length):
        return len(word) > length


    da = DynamicArray("This is a sentence with some long words".split())
    print(da)
    for length in [3, 4, 7]:
        print(da.filter(lambda word: is_long_word(word, length)))

    print("\n# reduce example 1")
    values = [100, 5, 10, 15, 20, 25]
    da = DynamicArray(values)
    print(da)
    print(da.reduce(lambda x, y: (x // 5 + y ** 2)))
    print(da.reduce(lambda x, y: (x + y ** 2), -1))

    print("\n# reduce example 2")
    da = DynamicArray([100])
    print(da.reduce(lambda x, y: x + y ** 2))
    print(da.reduce(lambda x, y: x + y ** 2, -1))
    da.remove_at_index(0)
    print(da.reduce(lambda x, y: x + y ** 2))
    print(da.reduce(lambda x, y: x + y ** 2, -1))

    def print_chunked_da(arr: DynamicArray):
        if len(str(arr)) <= 100:
            print(arr)
        else:
            print(f"DYN_ARR Size/Cap: {arr.length()}/{arr.get_capacity()}")
            print('[\n' + ',\n'.join(f'\t{chunk}' for chunk in arr) + '\n]')

    print("\n# chunk example 1")
    test_cases = [
        [10, 20, 30, 30, 5, 10, 1, 2, 3, 4],
        ['App', 'Async', 'Cloud', 'Data', 'Deploy',
         'C', 'Java', 'Python', 'Git', 'GitHub',
         'Class', 'Method', 'Heap']
    ]

    for case in test_cases:
        da = DynamicArray(case)
        chunked_da = chunk(da)
        print(da)
        print_chunked_da(chunked_da)

    print("\n# chunk example 2")
    test_cases = [[], [261], [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]]

    for case in test_cases:
        da = DynamicArray(case)
        chunked_da = chunk(da)
        print(da)
        print_chunked_da(chunked_da)

    print("\n# find_mode example 1")
    test_cases = (
        [1, 1, 2, 3, 3, 4],
        [1, 2, 3, 4, 5],
        ["Apple", "Banana", "Banana", "Carrot", "Carrot",
         "Date", "Date", "Date", "Eggplant", "Eggplant", "Eggplant",
         "Fig", "Fig", "Grape"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"{da}\nMode: {mode}, Frequency: {frequency}\n")

    case = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
    da = DynamicArray()
    for x in range(len(case)):
        da.append(case[x])
        mode, frequency = find_mode(da)
        print(f"{da}\nMode: {mode}, Frequency: {frequency}")
