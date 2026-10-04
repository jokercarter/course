# lr-gd.py -- logistic regression trained by gradient descent.
# ECE 453, Homework 2 (starter code). Fill in log_hess() and newton_method() for part (c).
import numpy as np
import matplotlib.pyplot as plt
import time

# ---------------------------------------------------------------------------
# synthetic two-class training data   (set n_samples = 100000 for part (d))
# ---------------------------------------------------------------------------
n_samples = 100
rng = np.random.default_rng(453)
n0 = n_samples // 2
n1 = n_samples - n0
x = np.vstack([rng.normal(loc=[-2.0, -2.0], scale=2.5, size=(n0, 2)),
               rng.normal(loc=[ 2.0,  2.0], scale=2.5, size=(n1, 2))])
y = np.concatenate([np.zeros(n0), np.ones(n1)])
# NOTE: each ROW of x is one data point (the lecture notes treat x as a column vector).
# Augment every point with a leading 1 so that theta[0] plays the role of the bias term.
x = np.hstack([np.ones((n_samples, 1)), x])          # x is now "x tilde", shape (n_samples, 3)

# ---------------------------------------------------------------------------
# model
# ---------------------------------------------------------------------------
def logistic_func(theta, x):
    """logistic function g(theta^T x_i) evaluated for every row x_i of x"""
    return 1.0 / (1.0 + np.exp(-x.dot(theta)))

def neg_log_like(theta, x, y):
    """negative log-likelihood  -l(theta)"""
    g = logistic_func(theta, x)
    return -np.sum(y * np.log(g) + (1.0 - y) * np.log(1.0 - g))

def log_grad(theta, x, y):
    """gradient of the negative log-likelihood with respect to theta"""
    g = logistic_func(theta, x)
    return x.T.dot(g - y)

# implementation of gradient descent for logistic regression
def grad_desc(theta, x, y, alpha, tol, maxiter):
    nll_vec = []
    nll_vec.append(neg_log_like(theta, x, y))
    nll_delta = 2.0*tol
    iter = 0
    while (nll_delta > tol) and (iter < maxiter):
        theta = theta - (alpha * log_grad(theta, x, y)) 
        nll_vec.append(neg_log_like(theta, x, y))
        nll_delta = nll_vec[-2]-nll_vec[-1]
        iter += 1
    return theta, np.array(nll_vec)
# function to compute the Hessian of the negative log-likelihood
def log_hess(theta, x, y):
    # YOUR CODE HERE  (part (c))
    raise NotImplementedError

# implementation of the Newton's method for logistic regression
def newton_method(theta, x, y, tol, maxiter):
    # YOUR CODE HERE  (part (c)) -- same interface as grad_desc, but no step size
    raise NotImplementedError

# ---------------------------------------------------------------------------
# run
# ---------------------------------------------------------------------------
alpha   = 0.001      # step size: experiment with this for part (a)
tol     = 1e-6       # do not change for your report
maxiter = 10000      # do not change for your report

theta0 = np.zeros(x.shape[1])
t0 = time.time()
theta, cost = grad_desc(theta0, x, y, alpha, tol, maxiter)
print('gradient descent: step size = %g, cost = %.3f, iterations = %d, time (s) = %.3f'
      % (alpha, cost[-1], len(cost) - 1, time.time() - t0))

# ---- plotting (comment this block out for part (d)) ----
plt.figure()
plt.scatter(x[:, 1], x[:, 2], c=y, cmap='bwr', s=12)
xs = np.linspace(x[:, 1].min(), x[:, 1].max(), 100)
plt.plot(xs, -(theta[0] + theta[1] * xs) / theta[2], 'k-')      # decision boundary theta^T x = 0
plt.title('training data and fitted decision boundary')
plt.figure()
plt.plot(cost)
plt.xlabel('iteration'); plt.ylabel('negative log-likelihood'); plt.title('gradient descent')
plt.show()
