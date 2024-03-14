
def selection_sort(array: list) -> None:
    """
    Perform optimized selection sort on an unsorted list of numbers.

    :param array: List of numbers to sort (modified inplace).
    """
    n = len(array)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if array[min_idx] > array[j]:
                min_idx = j
        array[i], array[min_idx] = array[min_idx], array[i]
