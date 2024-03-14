## Sorting


### Table of content
* [Binary sort](#binary-sort)
* [Bubble sort](#bubble-sort)
* [Insert sort](#insert-sort)
* [Quick sort](#quick-sort)
* [Selection sort](#selection-sort)


### Binary sort
    Binary Insertion Sort is an enhancement of the Insertion Sort algorithm 
    that uses a binary search to find the correct position for inserting an 
    element into the sorted part of the array. This modification reduces the
    number of comparisons, making the algorithm more efficient for larger 
    datasets.

    How Binary Insertion Sort Works
    1. Building the Sorted Array:
    Similar to Insertion Sort, Binary Insertion Sort starts with the second 
    element in the list. Instead of a linear search, it uses a binary search 
    to find the correct position for the current element in the sorted part 
    of the array.
    2. Binary Search:
    The algorithm performs a binary search to find the correct position for 
    inserting the current element. This involves repeatedly dividing the 
    sorted part of the array until the correct position is found.
    3. Inserting the Element:
    Once the correct position is determined, the algorithm shifts the elements
    to make space for the current element and inserts it into the sorted part.
    4. Efficiency:
    Binary Insertion Sort reduces the number of comparisons compared to regular
    Insertion Sort, making it more efficient for larger datasets.

### Bubble sort
    Bubble Sort is one of the simple sorting methods. This algorithm
    compares adjacent elements in a list and swaps them if they are in
    the wrong order. This process is repeated until the entire list is 
    sorted. However this algorithm is not suitable for large data sets 
    as its average and worst-case time complexity is quite high.
    
    How Bubble Sort Works
    1. Comparing Adjacent Elements:
    The algorithm starts from the first element in the list and compares 
    it with the next element. If the first element is greater than the 
    next one, they are swapped. It moves on to the next adjacent element 
    and repeats the process of comparison and swapping until the end of 
    the list.
    2. Traversing the List:
    After completing one iteration, the largest element is positioned at 
    the end of the list. The algorithm begins the next iteration, skipping
    the already sorted end of the list. This process is repeated until the
    list is fully sorted.
    3.Optimization:
    If no swaps are made during one iteration, it indicates that the list 
    is already sorted. The algorithm terminates when no swaps are made in
    one iteration, improving its efficiency.

### Insert sort
    Insertion Sort is a simple sorting algorithm that builds the final sorted
    array one element at a time. It is much less efficient on large lists 
    than more advanced algorithms such as quicksort, heapsort, or merge sort.
    However, it performs well for small datasets or nearly sorted datasets.
    
    How Insertion Sort Works
    1. Building the Sorted Array:
    The algorithm starts with the second element in the list and compares it
    with the preceding elements. It inserts the current element into its 
    correct position within the sorted part of the array. This process is 
    repeated for each element in the list, gradually building the sorted array.
    2. Iterative Process:
    Insertion Sort is an iterative algorithm that extends the sorted part of 
    the array with each iteration. At each step, the algorithm selects an 
    element from the unsorted part and places it in its correct position 
    within the sorted part.
    3. Efficiency:
    While Insertion Sort may not be the most efficient for large datasets, 
    it is adaptive, meaning it performs well on partially sorted lists.
    It is stable, maintaining the relative order of equal elements.

### Quick sort
    Quick Sort is a highly efficient and widely used sorting algorithm. 
    It uses a divide-and-conquer strategy to sort an array or list by 
    selecting a "pivot" element and partitioning the other elements into
    two sub-arrays according to whether they are less than or greater than
    the pivot. The sub-arrays are then recursively sorted.

    How Quick Sort Works
    1. Choosing a Pivot:
    The algorithm selects a pivot element from the array. The choice of pivot
    can affect the efficiency of the algorithm.
    2. Partitioning:
    The array is partitioned into two sub-arrays: elements less than the pivot
    and elements greater than the pivot. The pivot is now in its final sorted 
    position.
    3. Recursion:
    The above process is applied recursively to the sub-arrays. The sub-arrays 
    are partitioned, and the pivots are placed in their final positions until 
    the entire array is sorted.
    4. Efficiency:
    Quick Sort is efficient due to its divide-and-conquer nature. On average, 
    it has a time complexity of O(n log n), making it faster than many other 
    sorting algorithms.

### Selection sort
    Selection Sort is a simple and intuitive sorting algorithm. It divides the
    input list into two parts: a sorted and an unsorted region. The algorithm 
    repeatedly selects the smallest (or largest, depending on the order) 
    element from the unsorted region and swaps it with the first element of the
    unsorted region. This process is repeated until the entire list is sorted.

    How Selection Sort Works
    1. Dividing the List:
    The algorithm divides the list into two regions: the sorted region and the 
    unsorted region.
    2. Selecting the Minimum Element:
    From the unsorted region, the algorithm finds the minimum element.
    3. Swapping Elements:
    The minimum element is swapped with the first element of the unsorted region,
    effectively expanding the sorted region.
    4. Repeating the Process:
    Steps 2 and 3 are repeated for the remaining unsorted region until the entire 
    list is sorted.
    5. Efficiency:
    Selection Sort has a time complexity of O(n^2), making it less efficient for 
    large datasets compared to more advanced algorithms.
