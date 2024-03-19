def eqaul_freq(arr1: list[int], m: int) -> list[int]:
    arr1: list[int] = sorted(arr1)
    a = len(arr1)
    n = a // m

    res_arr = []

    for i in range(m):
        arr = [arr1[j] for j in range(i * n, (i+1) * n)]
        res_arr.append(arr)

    return res_arr

def equal_width(arr1: list[int], m: int) -> list[int]:
    arr1: list[int] = sorted(arr1)
    min_num = min(arr1)
    max_num = max(arr1)
    w = (max_num - min_num) // m
    arr = [min_num+w*i for i in range(m+1)]
    arri = []

    for i in range(m):
        temp = [j for j in arr1 if j >= arr[i] and j <= arr[i+1]]
        arri.append(temp)

    return arri