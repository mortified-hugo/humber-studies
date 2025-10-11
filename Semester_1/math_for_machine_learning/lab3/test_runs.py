import numpy as np

# Matrix A (all ones)
A = np.ones((3, 3), dtype=float)

# Compute eigenvalues and (raw) eigenvectors
eigvals, eigvecs = np.linalg.eig(A)
# eigvecs[:, i] corresponds to eigvals[i]

# Group unique eigenvalues and compute geometric multiplicities
unique_vals, counts = np.unique(np.round(eigvals, 12), return_counts=True)
print("Eigenvalues (raw):", eigvals)
print("Unique eigenvalues:", unique_vals)
print("Algebraic multiplicities:", counts)

# For each unique eigenvalue compute the nullspace of (A - lambda I) to get eigenspace
def nullspace(M, tol=1e-12):
    U, S, Vt = np.linalg.svd(M)
    null_mask = (S <= tol)
    if not np.any(null_mask):
        # relative tolerance fallback
        null_mask = (S <= S.max() * max(M.shape) * np.finfo(float).eps)
    ns = Vt.T[:, null_mask]
    # Orthonormalize columns if any
    if ns.size == 0:
        return np.zeros((M.shape[0], 0))
    Q, R = np.linalg.qr(ns)
    # keep columns corresponding to non-negligible R diagonal
    diagR = np.abs(np.diag(R))
    keep = diagR > (np.max(diagR) * 1e-12)
    return Q[:, keep]

eigenspaces = {}
for val in unique_vals:
    M = A - float(val) * np.eye(3)
    basis = nullspace(M)
    eigenspaces[val] = basis
    print(f"\nEigenvalue {val}:")
    print("  Geometric multiplicity:", basis.shape[1])
    if basis.shape[1] > 0:
        print("  Orthonormal basis (columns):\n", basis)

# Check diagonalizability: sum of geometric multiplicities == 3
total_geom = sum(b.shape[1] for b in eigenspaces.values())
print("\nTotal geometric multiplicity:", total_geom)
print("Diagonalizable?" , total_geom == A.shape[0])

# Construct P from orthonormal eigenvectors (columns) and D
P = np.hstack([eigenspaces[v] for v in unique_vals])
D = np.diag([v for v in unique_vals for _ in range(eigenspaces[v].shape[1])])

# Verify similarity A = P D P^{-1} (numerical)
if P.shape == (3,3) and np.linalg.matrix_rank(P) == 3:
    A_rec = P @ D @ np.linalg.inv(P)
    print("\nMax reconstruction error ||A - P D P^{-1}||_inf:", np.max(np.abs(A - A_rec)))
else:
    print("\nCould not form full-rank P from eigenspace bases.")