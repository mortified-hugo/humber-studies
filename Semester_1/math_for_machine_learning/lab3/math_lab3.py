import numpy as np
import numpy.linalg as la
# 1
# x_1 = np.array([[3],
#                 [-1],
#                 [0]])
#
# A = np.array([
#     [2, 3, 0],
#     [1, 4, 3],
#     [0, 0, 1]
# ])
#
# # Is x_1 an eigenvector of A?
# a = A@x_1
# print(f"When x1=\n{x_1}\n "
#       f"multiples by Matrix A, we get a=\n"
#       f"{a}.\n"
#       f"Since a is a multiple of x1, x1 is a eigenvector of A \n"
#       f"With b) it's eigenvalue being 1 (the vectors are the same)")

# # 2
#
# A = np.array([
#     [4, 2],
#     [1, 3]
# ])
#
# w, v = np.linalg.eig(A)
#
# print(f"A's eigenvalues are {w}\n"
#       f"and it's vectors are:\n"
#       f"v1 = {v[:, 0]}\n"
#       f"v2 = {v[:, 1]}")
# print(f"Both eigenvalues appear only once. Therefore, it's multiplicities are mult({w[0]})=1 and mult({w[1]})=1")

# # 3
#
# A = np.array([
#     [3, 2, 2],
#     [2, 3, 2],
#     [2, 2, 3]
# ])
#
# w, v = la.eig(A)
#
# lambda_1 = round(w[0])
# lambda_2 = round(w[1])
# lambda_3 = round(w[2])
#
# v_1 = v[:, 0]
# v_2 = v[:, 1]
# v_3 = v[:, 2]
#
# print(f"E({lambda_1}) = span({v_1})\n"
#       f"E({lambda_2}) = span({v_2})\n"
#       f"E({lambda_3}) = span({v_3})\n"
#       f"This vectors form the basis for the Eigenspace")

# # 4
#
# B = np.array([
#     [1, 1],
#     [1, 1]
# ])
#
# w, v = la.eig(B)
#
# # Make sure each vector is unit norm
# for i in range(v.shape[1]):
#     v[:, i] = v[:, i] / la.norm(v[:, i])
#
# print("Eigenbasis (two vectors) V:\n", v)
# D = np.diag(w)
#
# orthonormal_check = v.T @ v  # Should be identity matrix
# print("V transposed x V should be an identity matrix:\n", orthonormal_check)
#
# eigen_equation_check = B @ v - v @ D  # Should be zero matrix
# print("B x V - V x D = 0 if D is the diagonal matrix of the eigenvalues:\n", eigen_equation_check)

# 5

# A = np.array([
#     [0, -1, 1, 1],
#     [-1, 1, -2, 3],
#     [2, -1, 0, 0],
#     [1, -1, 1, 0]
# ])
#
# w, v = la.eig(A)
#
# # Complex Numbers????? Nice
# lambda_1 = np.round(w[0])
# lambda_2 = np.round(w[1])
# lambda_3 = np.round(w[2])
# lambda_4 = np.round(w[3])
#
# v_1 = v[:, 0]
# v_2 = v[:, 1]
# v_3 = v[:, 2]
# v_4 = v[:, 3]
#
# print(f"E({lambda_1}) = span({v_1})\n"
#       f"E({lambda_2}) = span({v_2})\n"
#       f"E({lambda_3}) = span({v_3})\n"
#       f"E({lambda_4}) = span({v_4})\n"
#       f"This vectors form the basis for the Eigenspace")

# #6
import sympy as sy
#
# # Get the eigenvectors using sympy
# A = sy.Matrix.ones(3, 3)
#
# print("A:", A)
# P, D = A.diagonalize()
# print("P:", P)
# print("D:", D)
#
# print("Sympy method: ", A.is_diagonalizable())
# print("PDP^-1 = A: ", P * D * P.inv() == A)

# #7
# print("A:")
# A = sy.Matrix([
#     [5, -6, -6],
#     [-1, 4, 2],
#     [3, -6, -4]
# ])
# sy.pprint(A)
#
# print("Eigenvalues and Eigenvectors:")
# eig_info = A.eigenvects()
# sy.pprint(eig_info)
# print("\nAlternative: nullspace of (A - lambda*I) for each eigenvalue:\n")
#
# # Another way to print (suggested by copilot)
# for val, _, _ in eig_info:
#     M = A - val * sy.eye(A.rows)
#     ns = M.nullspace()
#     print("Eigenvalue =", sy.simplify(val))
#     if ns:
#         print("  Nullspace basis:")
#         for v in ns:
#             sy.pprint(v)
#     else:
#         print("  Nullspace is trivial")
#     print("-" * 40)  # dashline
#
# # Is the matrix diagonilizable?
# is_diag = A.is_diagonalizable()
# print("Is diagonalizable? ", is_diag)

# 8
import scipy.linalg as la
H = sy.Matrix([
    [2, 1, 0],
    [1, 2, 1],
    [0, 1, 2]
])
sy.pprint(H)

L = la.cholesky(H)  # L is interpreted as the "square root" of A

sy.pprint(L.T @ L)

