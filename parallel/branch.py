import time
import numpy as np



N = 100_000_000



np.random.seed(123) 
myList = np.random.randint(low=0, high=255, size=N).tolist()

myList.sort()

t0 = time.time()
sumElemsLessThan128 = 0
sumTotal = 0

for numar in myList:
    if numar < 128:
        sumElemsLessThan128 += numar
    sumTotal += numar
t1 = time.time()

print(f"Sums: {sumElemsLessThan128} / {sumTotal} *** Done in {t1-t0}")