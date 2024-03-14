
def quicksort(array: list, left: int, right: int) -> None:
    """
    Perform quicksort on a list of numbers.

    :param array: List of numbers to be sorted (modified inplace).
    :param left: Index of the leftmost element of the sublist.
    :param right: Index of the rightmost element of the sublist.
    """
    if left < right:
        i = left
        j = right

        # Choose a pivot element
        pivot = array[(left + right) // 2]
        while True:
            # Find an element greater than or equal to the pivot on the left side
            while array[i] < pivot:
                i += 1

            # Find an element less than or equal to the pivot on the right side
            while array[j] > pivot:
                j -= 1

            if i <= j:
                # Swap array[i] with array[j]
                array[i], array[j] = array[j], array[i]
                i += 1
                j -= 1
            else:
                break

        # If the counters have not crossed, swap elements on the wrong side of the pivot
        if j > left:
            quicksort(array, left, j)
        if i < right:
            quicksort(array, i, right)
