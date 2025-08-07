import numpy as np
import matplotlib.pyplot as plt

# Parameters
N = 25
J = 1
S_up = 1
T = 1_000_000

gamma = 90
l = 2.866
Nn = (2 * N + 1) ** 2

# Build lattice
R = np.zeros((Nn, 2), dtype=int)
n = 0
for i in range(-N, N + 1):
    for j in range(-N, N + 1):
        R[n] = [i, j]
        n += 1

S = S_up * np.ones(Nn)

# Simulation
k_BT_values = np.arange(1, 4.05, 0.05)
M_values_average = np.zeros_like(k_BT_values)
KI_values = np.zeros_like(k_BT_values)
Variance = np.zeros_like(k_BT_values)

for p, k_BT in enumerate(k_BT_values):
    M = np.zeros(T)

    for k in range(T):
        idx = np.random.randint(Nn)
        i, j = R[idx]

        i_up = -N if i + 1 > N else i + 1
        i_down = N if i - 1 < -N else i - 1
        j_right = -N if j + 1 > N else j + 1
        j_left = N if j - 1 < -N else j - 1

        idx_up = np.where((R[:, 0] == i_up) & (R[:, 1] == j))[0][0]
        idx_down = np.where((R[:, 0] == i_down) & (R[:, 1] == j))[0][0]
        idx_right = np.where((R[:, 0] == i) & (R[:, 1] == j_right))[0][0]
        idx_left = np.where((R[:, 0] == i) & (R[:, 1] == j_left))[0][0]

        Delta_E = 2 * J * S[idx] * (S[idx_up] + S[idx_down] + S[idx_right] + S[idx_left])

        if Delta_E <= 0 or np.random.rand() < np.exp(-Delta_E / k_BT):
            S[idx] = -S[idx]

        M[k] = np.sum(S) / ((2 * N) ** 2)

    M_half = M[T//2:]
    M_mean = np.mean(M_half)
    print(f"Average magnetization for k_BT = {k_BT:.2f} : {M_mean:.4f}")

    KI = (np.mean(M**2) - M_mean**2) / k_BT
    M_values_average[p] = M_mean
    KI_values[p] = KI
    Variance[p] = np.std(M_half)

# Plot magnetization vs k_BT
plt.figure()
plt.plot(k_BT_values, M_values_average, '-o')
plt.xlabel('k_B T')
plt.ylabel('Average Magnetization M')
plt.title('Magnetization vs k_B T')
plt.grid(True)
plt.show()

# Plot KI vs k_BT
plt.figure()
plt.plot(k_BT_values, KI_values, '-o')
plt.xlabel('k_B T')
plt.ylabel('KI')
plt.title('KI vs k_B T')
plt.grid(True)
plt.show()

# Plot with error bars
plt.figure()
plt.errorbar(k_BT_values, M_values_average, yerr=Variance, fmt='-o')
plt.xlabel('k_B T')
plt.ylabel('Average Magnetization M')
plt.title('Magnetization vs k_B T with Fluctuations')
plt.grid(True)
plt.show()
