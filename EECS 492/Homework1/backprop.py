
import numpy as np




def sigmoid(z):
    z = np.asarray(z)
    out = np.empty_like(z, dtype=float)
    pos = z >= 0
    out[pos] = 1.0 / (1.0 + np.exp(-z[pos]))
    exp_z = np.exp(z[~pos])
    out[~pos] = exp_z / (1.0 + exp_z)
    return float(out) if out.ndim == 0 else out


def forward_single(x, w, b):
    return sigmoid(np.dot(w, x) + b)


def backward_single(x, w, b, y):
    a = forward_single(x, w, b)
    dz = a - y
    return dz * x, float(dz)




def tanh(z):
    return np.tanh(z)


def mlp_forward(X, params):
    Z1 = X @ params["W1"] + params["b1"]
    A1 = tanh(Z1)
    Z2 = A1 @ params["W2"] + params["b2"]
    A2 = sigmoid(Z2)
    cache = {"X": X, "Z1": Z1, "A1": A1, "Z2": Z2, "A2": A2}
    return A2, cache


def bce_loss(A2, y):
    eps = 1e-12
    A2 = np.clip(A2, eps, 1.0 - eps)
    return float(-np.mean(y * np.log(A2) + (1.0 - y) * np.log(1.0 - A2)))


def mlp_backward(cache, params, y):
    X, Z1, A1, A2 = cache["X"], cache["Z1"], cache["A1"], cache["A2"]
    N = X.shape[0]
    dZ2 = (A2 - y) / N
    dW2 = A1.T @ dZ2
    db2 = np.sum(dZ2, axis=0)
    dA1 = dZ2 @ params["W2"].T
    dZ1 = dA1 * (1.0 - A1 ** 2)
    dW1 = X.T @ dZ1
    db1 = np.sum(dZ1, axis=0)
    return {"W1": dW1, "b1": db1, "W2": dW2, "b2": db2}


if __name__ == "__main__":
    rng = np.random.default_rng(0)

    print("== Problem 1: single neuron ==")
    try:
        x = np.array([1.0, -2.0, 0.5])
        w = np.array([0.1, 0.2, -0.3])
        b = 0.05
        y = 1.0
        a = forward_single(x, w, b)
        dw, db = backward_single(x, w, b, y)
        print("prediction a =", a)
        print("dL/dw =", dw)
        print("dL/db =", db)
    except NotImplementedError as e:
        print("(not implemented yet):", e)

    print("\n== Problem 2: two-layer MLP ==")
    try:
        N, d, h = 5, 3, 4
        X = rng.standard_normal((N, d))
        y = rng.integers(0, 2, size=(N, 1)).astype(float)
        params = {
            "W1": 0.1 * rng.standard_normal((d, h)),
            "b1": np.zeros(h),
            "W2": 0.1 * rng.standard_normal((h, 1)),
            "b2": np.zeros(1),
        }
        A2, cache = mlp_forward(X, params)
        loss = bce_loss(A2, y)
        grads = mlp_backward(cache, params, y)
        print("loss =", loss)
        for k in ("W1", "b1", "W2", "b2"):
            print(f"grad[{k}] shape = {grads[k].shape} (expected {params[k].shape})")
    except NotImplementedError as e:
        print("(not implemented yet):", e)
