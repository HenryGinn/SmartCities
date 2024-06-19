def BitTest(x, od):
    result = x & (1 << od)
    return int(bool(result))

def BitFlip(b, pos):
    b ^= 1 << pos
    return b

def partition(A, start, end, order, ax, direction):
    i = start
    j = end
    while True:
        while i < j and BitTest(A[i][ax],order) == direction:
            i = i + 1
        while i < j and BitTest(A[j][ax],order) != direction:
            j = j - 1
            
        if j <= i:
            return i
        
        A[i], A[j] = A[j], A[i]

def HSort(A, start, end, order, current_dimension, e, d, direction, count):
    if end <= start: 
        return
    p = partition(A, start, end,order, (d+current_dimension) % n, BitTest(e, (d+current_dimension) % n))

    if current_dimension == n-1:
        if order == 0:
            return
        
        d2 = (d+n+n - (2 if direction else count + 2)) % n
        e = BitFlip(e, d2)
        e = BitFlip(e, (d+current_dimension) % n)
        HSort(A, start, p-1, order-1, 0, e, d2, False, 0)
        
        e = BitFlip(e,(d+current_dimension) % n)
        e = BitFlip(e, d2)
        d2 = (d+n+n- (count + 2 if direction else 2)) % n
        HSort(A, p, end, order - 1, 0, e, d2, False, 0)
    else:
        HSort(A, start, p-1, order, current_dimension+1, e, d, False, (1 if direction else count+1))
        e = BitFlip(e,(d+current_dimension) % n)
        e = BitFlip(e,(d+current_dimension+1) % n)
        HSort(A, p, end,order, current_dimension+1, e, d, True, (count+1 if direction else 1))
        e = BitFlip(e, (d+current_dimension+1) % n)
        e = BitFlip(e, (d+current_dimension) % n)

N=9 # 9 points
n=2 # 2 dimension 
m=3 # order of Hilbert curve
        
array = [[2,2],[2,4],[3,4],[2,5],[3,5],[1,6],[3,6],[5,6],[3,7]]
HSort(array, start=0, end=N-1, order=m-1, current_dimension=0, e=0, d=0, direction=False, count=0)
print(array)
