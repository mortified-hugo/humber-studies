import numpy as np
import numpy.linalg as la

# 4

A = np.array([
    [3, 2, 2],
    [2, 3, 2],
    [2, 2, 3]
])

w, v = la.eig(A)

lambda_1 = round(w[0])
lambda_2 = round(w[1])
lambda_3 = round(w[2])

v_1 = v[:, 0]
v_2 = v[:, 1]
v_3 = v[:, 2]

print(f"E({lambda_1}) = span({v_1})\n"
      f"E({lambda_2}) = span({v_2})\n"
      f"E({lambda_3}) = span({v_3})\n"
      f"This vectors form the basis for the Eigenspace")





