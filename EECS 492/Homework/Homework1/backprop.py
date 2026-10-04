"""
EECS 492 - Homework 1

This is the STARTER file. Fill in the blocks marked "TODO".
Do NOT modify any code outside the TODO blocks, and do NOT change the
function signatures. Your implementation will be tested by an autograder.

You may ONLY use numpy. Do not use any deep-learning framework
(PyTorch, TensorFlow, JAX, autograd, etc.).

Quick start: python backprop.py
This runs a tiny sanity check that prints the outputs of the functions you
implement so you can see things working end-to-end before you submit.
"""

import numpy as np


# =====================================================================
# Problem 1 : A single sigmoid neuron + binary cross-entropy loss
# ---------------------------------------------------------------------
# We have one training example:
#   x : feature vector, shape (d,)
#   y : true label in {0, 1} (a float)
# and a single neuron with parameters:
#   w : weight vector, shape (d,)
#   b : bias, a scalar
#
# Forward pass:
#   z = w . x + b              (a scalar)
#   a = sigmoid(z)             (the predicted probability, in (0, 1))
#
# Loss (binary cross-entropy):
#   L = -( y * log(a) + (1 - y) * log(1 - a) )
# =====================================================================


def sigmoid(z):
    """Numerically-stable logistic sigmoid, applied elementwise.

    Args:
        z: a numpy array (or scalar).
    Returns:
        sigmoid(z), same shape as z.
    """
    # TODO 1a: implement the sigmoid function.
    raise NotImplementedError("TODO 1a: implement sigmoid")


def forward_single(x, w, b):
    """Forward pass for a single sigmoid neuron.

    Args:
        x: input features, shape (d,).
        w: weights, shape (d,).
        b: bias, scalar.
    Returns:
        a: the scalar predicted probability sigmoid(w . x + b).
    """
    # TODO 1b: compute z = w . x + b, then a = sigmoid(z). Return a.
    raise NotImplementedError("TODO 1b: implement forward_single")


def backward_single(x, w, b, y):
    """Backward pass for a single sigmoid neuron with BCE loss.

    Compute the gradient of the binary cross-entropy loss L with respect
    to w and b for a SINGLE training example (x, y).

    Args:
        x: input features, shape (d,).
        w: weights, shape (d,).
        b: bias, scalar.
        y: true label in {0, 1}, scalar.
    Returns:
        (dw, db) where
            dw: gradient dL/dw, shape (d,).
            db: gradient dL/db, scalar.
    """
    # TODO 1c: implement the backward pass.
    raise NotImplementedError("TODO 1c: implement backward_single")


# =====================================================================
# Problem 2: A two-layer MLP on a batch of examples
# ---------------------------------------------------------------------
# Architecture (one hidden layer):
#   Input  X  : shape (N, d)      N examples, d features each
#   Layer 1:  Z1 = X @ W1 + b1    W1: (d, h), b1: (h,)   -> Z1: (N, h)
#             A1 = tanh(Z1)                               -> A1: (N, h)
#   Layer 2:  Z2 = A1 @ W2 + b2   W2: (h, 1), b2: (1,)   -> Z2: (N, 1)
#             A2 = sigmoid(Z2)                            -> A2: (N, 1)
#
# Loss (mean binary cross-entropy over the batch):
#   L = -(1/N) * sum_n [ y_n log(a_n) + (1 - y_n) log(1 - a_n) ]
#   where y has shape (N, 1).
#
# You must implement the forward pass (returning a cache (a dictionary containing intermediate values) for reuse),
# and the backward pass returning gradients for ALL four parameters.
# =====================================================================


def tanh(z):
    """Hyperbolic tangent, applied elementwise. You may use np.tanh."""
    # TODO 2a: implement tanh (np.tanh is allowed).
    raise NotImplementedError("TODO 2a: implement tanh")


def mlp_forward(X, params):
    """Forward pass for the two-layer MLP.

    Args:
        X: inputs, shape (N, d).
        params: dict with keys "W1" (d, h), "b1" (h,), "W2" (h, 1), "b2" (1,).
    Returns:
        (A2, cache) where
            A2: output probabilities, shape (N, 1).
            cache: a dict holding any intermediate values you need in the
                   backward pass (e.g. X, Z1, A1, Z2, A2).
    """
    # TODO 2b: implement the forward pass described above.
    # Store the intermediate values you need for backprop in the returned cache dict.
    raise NotImplementedError("TODO 2b: implement mlp_forward")


def bce_loss(A2, y):
    """Mean binary cross-entropy loss over the batch.

    Args:
        A2: predicted probabilities, shape (N, 1).
        y:  true labels in {0, 1}, shape (N, 1).
    Returns:
        scalar mean BCE loss.
    """
    # TODO 2c: implement the mean BCE loss.
    raise NotImplementedError("TODO 2c: implement bce_loss")


def mlp_backward(cache, params, y):
    """Backward pass for the two-layer MLP (mean BCE loss).

    Args:
        cache:  the dict containing intermediate values returned by mlp_forward.
        params: the same params dict passed to mlp_forward.
        y:      true labels in {0, 1}, shape (N, 1).
    Returns:
        grads: dict with keys "W1", "b1", "W2", "b2" giving the gradient of
               the mean BCE loss w.r.t. each parameter. Each gradient must
               have the SAME shape as the corresponding parameter.
    """
    # TODO 2d: implement the backward pass using the chain rule.
    raise NotImplementedError("TODO 2d: implement mlp_backward")


# =====================================================================
# Tiny sanity check so you can see your code run. This is NOT the grader.
# =====================================================================
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
