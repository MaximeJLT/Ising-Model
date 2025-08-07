import numpy as np
import matplotlib.pyplot as plt

# ------------------------
# Parameters
# ------------------------
N = 25                 # Lattice size
J = 1                  # Interaction strength
k_BT = 1               # Temperature (in units of k_B)
T = 100_000            # Number of iterations
M = np.zeros(T)        # Magnetization over time

# ------------------------
# Lattice construction
# ------------------------
R = []
for i in range(-N, N + 1):
    for j in range(-N, N + 1):
        R.append([i, j])
R = np.array(R)
Nn = R.shape[0]

# Initialize spins randomly (+1 or -1)
S = np.sign(np.random.rand(Nn) - 0.5)

# ------------------------
# Interactive plot
# ------------------------
plt.ion()
fig, ax = plt.subplots()
im = ax.imshow(S.reshape((2 * N + 1, 2 * N + 1)), cmap='gray')
ax.set_title("Spin configuration (cluster formation)")
ax.set_aspect('equal')
plt.pause(0.001)

# ------------------------
# Ising model simulation
# ------------------------
for k in range(T):
    idx = np.random.randint(Nn)
    i, j = R[idx]

    # Periodic boundary conditions
    i_up    = -N if i + 1 > N else i + 1
    i_down  = N  if i - 1 < -N else i - 1
    j_right = -N if j + 1 > N else j + 1
    j_left  = N  if j - 1 < -N else j - 1

    # Get neighbor indices
    idx_up    = np.where((R[:, 0] == i_up)   & (R[:, 1] == j))[0][0]
    idx_down  = np.where((R[:, 0] == i_down) & (R[:, 1] == j))[0][0]
    idx_right = np.where((R[:, 0] == i)      & (R[:, 1] == j_right))[0][0]
    idx_left  = np.where((R[:, 0] == i)      & (R[:, 1] == j_left))[0][0]

    # Energy difference (Metropolis criterion)
    Delta_E = 2 * J * S[idx] * (
        S[idx_up] + S[idx_down] + S[idx_right] + S[idx_left]
    )

    if Delta_E <= 0:
        S[idx] = -S[idx]
    else:
        prob = np.exp(-Delta_E / k_BT)
        if np.random.rand() < prob:
            S[idx] = -S[idx]

    # Compute magnetization
    M[k] = np.sum(S) / (2 * N * 2 * N)

    # Update the plot every 500 iterations
    if k % 500 == 0:
        im.set_data(S.reshape((2 * N + 1, 2 * N + 1)))
        plt.pause(0.001)

# ------------------------
# Magnetization average over second half
# ------------------------
M_mean = np.mean(M[50000:])
print(f"Average magnetization over second half of iterations: {M_mean:.4f}")

# ------------------------
# Plot magnetization evolution
# ------------------------
plt.ioff()
plt.figure()
plt.plot(np.arange(T), M, color='blue')
plt.xlabel("Iterations")
plt.ylabel("Magnetization")
plt.title("Magnetization over time")
plt.grid(True)
plt.tight_layout()
plt.show()
