import numpy as np

# 1) Manhattan norm of v = (2,3,4,5)
v1 = np.array([2, 3, 4, 5])
manhattan_norm = np.linalg.norm(v1, ord=1)

# 2) Distance between a=(1,2,3) and b=(-1,1,0)
a = np.array([1, 2, 3])
b = np.array([-1, 1, 0])
distance_ab = np.linalg.norm(a - b)

# 3) Angle between v=(2,3,4) and w=(1,2,0)
v3 = np.array([2, 3, 4])
w3 = np.array([1, 2, 0])
dot_vw = np.dot(v3, w3)
cos_theta = dot_vw / (np.linalg.norm(v3) * np.linalg.norm(w3))
# numeric safety for arccos
cos_theta = np.clip(cos_theta, -1.0, 1.0)
angle_rad = np.arccos(cos_theta)
angle_deg = np.degrees(angle_rad)

# 4) Show orthogonality of v=(-4,2,5) and w=(1,-1,2,0)
# Note: vectors must have same length; the first has length 3, second length 4 in transcription.
# Interpreting both as 4D with missing component for v set to 0: v = (-4,2,5,0), w = (1,-1,2,0)
v4 = np.array([-4, 2, 5, 0])
w4 = np.array([1, -1, 2, 0])
dot_v4_w4 = np.dot(v4, w4)
are_orthogonal = np.isclose(dot_v4_w4, 0.0)

# 5) Any unit vector orthogonal to v=(2,3,6)
v5 = np.array([2, 3, 6], dtype=float)
# pick a vector not parallel to v, for example e1 = (1,0,0), form u = e1 - proj_v(e1)
e1 = np.array([1.0, 0.0, 0.0])
proj_e1_on_v = (np.dot(e1, v5) / np.dot(v5, v5)) * v5
u = e1 - proj_e1_on_v
u_norm = np.linalg.norm(u)
unit_u = u / u_norm

# 6) Vector projection of a=(1,2,3) onto b=(3,-4,1)
a6 = np.array([1.0, 2.0, 3.0])
b6 = np.array([3.0, -4.0, 1.0])
proj_a_on_b = (np.dot(a6, b6) / np.dot(b6, b6)) * b6

# 7) v=(1,1) and w=(1,-1) form a basis of R^2; find orthonormal basis and show why
v7 = np.array([1.0, 1.0])
w7 = np.array([1.0, -1.0])
# they are orthogonal: dot = 0
dot_v7_w7 = np.dot(v7, w7)
# normalize to make orthonormal
e1 = v7 / np.linalg.norm(v7)
e2 = w7 / np.linalg.norm(w7)

# 8) Projection of (1,1,1) onto the xy-plane
p8 = np.array([1.0, 1.0, 1.0])
proj_xy = np.array([p8[0], p8[1], 0.0])

# 9) Create 2 random vectors in R^4 and find the angle between them
rng = np.random.default_rng(seed=42)
r1 = rng.standard_normal(4)
r2 = rng.standard_normal(4)
dot_r = np.dot(r1, r2)
cos_theta_r = dot_r / (np.linalg.norm(r1) * np.linalg.norm(r2))
cos_theta_r = np.clip(cos_theta_r, -1.0, 1.0)
angle_r_rad = np.arccos(cos_theta_r)
angle_r_deg = np.degrees(angle_r_rad)

# 10) Distance between point (1,-2,4) and plane 3x + 2y + 6z = 5
point10 = np.array([1.0, -2.0, 4.0])
a_p, b_p, c_p, d_p = 3.0, 2.0, 6.0, 5.0
numer = abs(a_p*point10[0] + b_p*point10[1] + c_p*point10[2] - d_p)
denom = np.sqrt(a_p**2 + b_p**2 + c_p**2)
dist_point_plane = numer / denom

# Print results
print("1) Manhattan norm of v = (2,3,4,5):", manhattan_norm)
print("2) Distance between a and b:", distance_ab)
print("3) Angle between v and w: {:.6f} rad, {:.6f} degrees".format(angle_rad, angle_deg))
print("4) Dot product v·w:", dot_v4_w4, " -> orthogonal?", are_orthogonal)
print("5) One unit vector orthogonal to (2,3,6):", unit_u)
print("   Check dot product with v:", np.dot(unit_u, v5))
print("6) Projection of a onto b:", proj_a_on_b)
print("7) v·w:", dot_v7_w7, " Orthonormal basis e1,e2:", e1, e2)
print("   Check orthonormality: e1·e2 =", np.dot(e1, e2),
      " ||e1|| =", np.linalg.norm(e1), " ||e2|| =", np.linalg.norm(e2))
print("8) Projection of (1,1,1) onto xy-plane:", proj_xy)
print("9) Random vector r1:", r1)
print("   Random vector r2:", r2)
print("   Angle between r1 and r2: {:.6f} rad, {:.6f} degrees".format(angle_r_rad, angle_r_deg))
print("10) Distance from (1,-2,4) to plane 3x+2y+6z=5:", dist_point_plane)