
def insertion_sort(array: list) -> None:
    """
    Perform insertion sort on a list of numbers.

    :param array: List of numbers to be sorted (modified inplace).
    """
    n = len(array)
    for i in range(1, n):
        # Insert the element at the correct position
        key = array[i]  # This element will be inserted at the correct position
        j = i - 1

        # Shift elements greater than key to the right
        while j >= 0 and array[j] > key:
            array[j + 1] = array[j]  # Shift elements
            j -= 1

        array[j + 1] = key  # Insert the value of the variable key at the correct position
