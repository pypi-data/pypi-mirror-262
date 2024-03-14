

def binary_insertion_sort(array: list) -> None:
    """
    Perform binary insertion sort on the given list of numbers.

    :param array: List of numbers to be sorted in ascending order.
    """
    for i in range(1, len(array)):
        temp = array[i]
        pos = binary_search(array, temp, 0, i) + 1

        for k in range(i, pos, -1):
            array[k] = array[k - 1]

        array[pos] = temp


def binary_search(array: list, target: int, low: int, high: int) -> bool:
    """
    Perform binary search to find the index of the target value in the sorted array of numbers.

    :param array: List of numbers to perform binary search on.
    :param target: Target value to find.
    :param low: Index of the first element in the array.
    :param high: Index of the last element in the array.
    :return: True if the target value is found, False otherwise.
    """
    if low > high:
        return False
    else:
        mid = (low + high) // 2
        if array[mid] == target:
            return True
        elif array[mid] < target:
            return binary_search(array, target, mid + 1, high)
        else:
            return binary_search(array, target, low, mid - 1)
