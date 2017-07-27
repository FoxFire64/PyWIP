import random


def merge(A, p, q, r):
    try:
        len1 = q - p + 1
        len2 = r - q
        print("p: {}, q: {}, r: {}".format(p, q, r))
        L = [None] * (len1)
        R = [None] * (len2)
        for i in range(len1):
            L[i] = A[p + i]
            print(L[i])
        for j in range(len2):
            R[j] = A[q + j]
        L[len1] = None
        R[len2] = None
        i, j = 0, 0
        for k in range(p, r):
            print("left is {}, right is {}".format(L, R))
            if L[i] < R[j]:
                A[k] = L[i]
                i = i + 1
            else:
                A[k] = R[j]
                j = j + 1
    except IndexError:
        print("aaaand we fucked up")
        quit()


def merge_sort(A, p, r):
    if p < r:
        q = (p + r) // 2
        merge_sort(A, p, q)
        merge_sort(A, q + 1, r)
        merge(A, p, q, r)


def merge_sort2(A):
    if len(A) > 1:
        print("splitting {}".format(A))
        mid = len(A) // 2
        left = A[:mid]
        right = A[mid:]
        print("left is {}, right is {}".format(left, right))

        merge_sort2(left)
        merge_sort2(right)

        i, j, k = 0, 0, 0
        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                A[k] = left[i]
                i = i + 1
            else:
                A[k] = right[j]
                j = j + 1
            k = k + 1

        while i < len(left):
            A[k] = left[i]
            i = i + 1
            k = k + 1

        while j < len(right):
            A[k] = right[j]
            j = j + 1
            k = k + 1

        print("merging {}".format(A))


if __name__ == "__main__":
    rlist = random.sample(range(100), 50)
    print(rlist)
    # merge_sort(rlist, 0, len(rlist))
    merge_sort2(rlist)
    print(rlist)
