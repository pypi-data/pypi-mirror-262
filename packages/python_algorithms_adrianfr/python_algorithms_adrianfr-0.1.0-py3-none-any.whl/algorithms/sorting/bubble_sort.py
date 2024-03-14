

def bubble_sort(array: list) -> None:
    """
    Perform optimized bubble sort on a list of numbers.
    :param array: List to be sorted.
    """
    n = len(array)
    for i in range(n):
        swapped = False  # Flag to track if any swaps were made in this pass
        for j in range(0, n - i - 1):
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
                swapped = True  # Set the flag if a swap is made
        if not swapped:
            break  # If no swaps were made, the list is already sorted
