import numpy as np


def question_1():
    a = np.array([4, 6, 7])
    b = np.array([3, 4, 5])
    print(f"The sum of the vectors is{np.add(a, b)}")


def question_2_and_3():
    A = np.array([[2, 7, -1, 0, 3],
                  [4, 6, -3, 1, 8]])

    print(f"The Dimensions of Matrix A are {A.shape}")
    print(f"A transposed is {A.T}")


def questions_4_and_5():
    B = np.array([[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 9]])

    B_2 = np.array([[9, 8, 7],
                  [6, 5, 4],
                  [3, 2, 1]])

    print(f"The resulting matrix from the multiplication of the matrices is {np.dot(B, B_2)}")

    det = np.linalg.det(B)
    print("Determinant:", det)

    if det != 0:
        inverse = np.linalg.inv(B)
        print("Inverse:\n", inverse)
    else:
        print("Matrix is not invertible because its determinant is 0.")


def question_6():
    C = np.array([
        [5, 0],
        [0, 5]
    ])

    # Compute the inverse of C
    C_inv = np.linalg.inv(C)

    # Multiply C by its inverse
    product = np.dot(C, C_inv)

    # Display the result
    print("C:\n", C)
    print("C inverse:\n", C_inv)
    print("C * C_inv:\n", product)


def question_7():
    f_1 = np.array([[1, 1, 1],
                    [1, -1, 2],
                    [0, 1, 1]])
    f_2 = np.array([3, 2, 2])

    return print(f"System of equations solution is {np.linalg.solve(f_1, f_2)}")


def question_8():
    # All vectors in a matrix
    D = np.array([
        [1, 1, -1],
        [0, 1, 2],
        [2, 1, 4]
    ])

    # Step 2: Check rank
    rank = np.linalg.matrix_rank(D)

    # Step 3: Conclusion
    if rank == 3:
        print("All vectors are linearly independent and form a basis for R^3.")
    else:
        print("The vectors are not linearly independent.")


def question_9_and_10():
    C = np.array([
        [5, 0],
        [0, 5]
    ])

    # Original vector
    v = np.array([3, 4])

    # Compute the image under the transformation
    image = np.dot(C, v)
    print("Image of vector (3, 4):", image)

    C_inv = np.linalg.inv(C)

    # Compute the preimage
    preimage = np.dot(C_inv, image)
    print("Preimage of vector (15, 20):", preimage)


question_1()
question_2_and_3()
questions_4_and_5()
question_6()
question_7()
question_8()
question_9_and_10()

