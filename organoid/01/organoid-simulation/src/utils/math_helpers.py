def integrate_euler(func, y0, t, dt):
    y = y0
    for i in range(len(t) - 1):
        y += func(t[i], y) * dt
    return y

def random_uniform(low, high, size=None):
    return np.random.uniform(low, high, size)

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def gaussian(x, mean, stddev):
    return (1 / (stddev * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mean) / stddev) ** 2)