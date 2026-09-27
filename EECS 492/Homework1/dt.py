"""
dt.py — Decision Tree (from scratch) for Intro to AI (HW1)

You will fill in TWO TODO functions:
  1) entropy(y)
  2) information_gain(y, y_left, y_right)

Everything else is provided so you can train/evaluate a decision tree from hw1.ipynb.

Rules:
- Do NOT use sklearn or any external decision-tree library.
- Do NOT change function names/signatures.
- Keep behavior deterministic.

Labels are binary: y in {0, 1}.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple, List

import numpy as np


# -----------------------------
# TODO 1: Entropy
# -----------------------------
def entropy(y: np.ndarray) -> float:
    """
    Compute entropy of binary labels y in {0,1}.

    H(y) = - sum_c p_c * log2(p_c)
    Convention: 0 * log2(0) = 0

    Parameters
    ----------
    y : np.ndarray, shape (n,)
        Binary labels in {0,1}.

    Returns
    -------
    float
        Entropy in bits.

    TODO:
    - Implement this function.
    - You may assume y is non-empty.
    """
    # ===== TODO START =====
    y = np.asarray(y)
    _, counts = np.unique(y, return_counts=True)
    probs = counts.astype(float) / y.size
    return float(-np.sum(probs * np.log2(probs)))
    # ===== TODO END =====


# -----------------------------
# TODO 2: Information Gain
# -----------------------------
def information_gain(y: np.ndarray, y_left: np.ndarray, y_right: np.ndarray) -> float:
    """
    Information gain for a split.

    IG = H(y) - (|L|/|y|) H(y_left) - (|R|/|y|) H(y_right)

    Parameters
    ----------
    y : np.ndarray, shape (n,)
        Parent labels.
    y_left : np.ndarray
        Labels for left child.
    y_right : np.ndarray
        Labels for right child.

    Returns
    -------
    float
        Information gain (>= 0 in typical cases).
    """
    # ===== TODO START =====
    n = len(y)
    if n == 0:
        return 0.0
    return float(entropy(y) - (len(y_left) / n) * entropy(y_left) - (len(y_right) / n) * entropy(y_right))
    # ===== TODO END =====


# -----------------------------
# Provided implementation
# -----------------------------
def _majority_class(y: np.ndarray) -> int:
    """Majority vote; tie-break predicts 1."""
    # y in {0,1}
    ones = int(np.sum(y == 1))
    zeros = int(np.sum(y == 0))
    return 1 if ones >= zeros else 0


@dataclass
class Node:
    # For internal node
    feature_index: Optional[int] = None
    threshold: Optional[float] = None
    left: Optional["Node"] = None
    right: Optional["Node"] = None

    # For leaf or fallback
    prediction: int = 1

    def is_leaf(self) -> bool:
        return self.left is None and self.right is None


class DecisionTreeClassifier:
    """
    A simple binary decision tree classifier (continuous features) using entropy / information gain.

    Splitting rule: x[feature] <= threshold goes left, else right.
    """

    def __init__(
        self,
        max_depth: int = 4,
        min_samples_split: int = 2,
        min_information_gain: float = 1e-9,
    ) -> None:
        if max_depth < 0:
            raise ValueError("max_depth must be >= 0")
        if min_samples_split < 2:
            raise ValueError("min_samples_split must be >= 2")
        if min_information_gain < 0:
            raise ValueError("min_information_gain must be >= 0")

        self.max_depth = int(max_depth)
        self.min_samples_split = int(min_samples_split)
        self.min_information_gain = float(min_information_gain)
        self.root: Optional[Node] = None

    def fit(self, X: np.ndarray, y: np.ndarray) -> "DecisionTreeClassifier":
        X = np.asarray(X)
        y = np.asarray(y).astype(int)
        if X.ndim != 2:
            raise ValueError("X must be 2D array")
        if y.ndim != 1:
            raise ValueError("y must be 1D array")
        if len(X) != len(y):
            raise ValueError("X and y must have same number of rows")
        if len(y) == 0:
            raise ValueError("Empty dataset")

        self.root = self._build_tree(X, y, depth=0)
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        if self.root is None:
            raise RuntimeError("Model not fitted. Call fit() first.")
        X = np.asarray(X)
        if X.ndim != 2:
            raise ValueError("X must be 2D array")

        preds = np.zeros(X.shape[0], dtype=int)
        for i in range(X.shape[0]):
            preds[i] = self._predict_one(X[i], self.root)
        return preds

    def score(self, X: np.ndarray, y: np.ndarray) -> float:
        """Accuracy in [0,1]."""
        y = np.asarray(y).astype(int)
        preds = self.predict(X)
        return float(np.mean(preds == y))

    def _predict_one(self, x: np.ndarray, node: Node) -> int:
        while not node.is_leaf():
            # Fallback prediction stored at node
            if node.feature_index is None or node.threshold is None:
                return node.prediction
            if x[node.feature_index] <= node.threshold:
                node = node.left  # type: ignore[assignment]
            else:
                node = node.right  # type: ignore[assignment]
            if node is None:
                # Should not happen, but safe fallback
                return 1
        return node.prediction

    def _build_tree(self, X: np.ndarray, y: np.ndarray, depth: int) -> Node:
        # Majority prediction at this node (also used as fallback)
        pred = _majority_class(y)

        # Stopping conditions
        if np.all(y == y[0]):  # pure node
            return Node(prediction=int(y[0]))
        if depth >= self.max_depth:
            return Node(prediction=pred)
        if X.shape[0] < self.min_samples_split:
            return Node(prediction=pred)

        feat, thr, gain = self._best_split(X, y)
        if feat is None or thr is None or gain < self.min_information_gain:
            return Node(prediction=pred)

        # Split
        mask_left = X[:, feat] <= thr
        X_left, y_left = X[mask_left], y[mask_left]
        X_right, y_right = X[~mask_left], y[~mask_left]

        # Guard against degenerate splits (should be rare due to threshold choice)
        if len(y_left) == 0 or len(y_right) == 0:
            return Node(prediction=pred)

        left_node = self._build_tree(X_left, y_left, depth + 1)
        right_node = self._build_tree(X_right, y_right, depth + 1)

        return Node(
            feature_index=int(feat),
            threshold=float(thr),
            left=left_node,
            right=right_node,
            prediction=pred,
        )

    def _best_split(self, X: np.ndarray, y: np.ndarray) -> Tuple[Optional[int], Optional[float], float]:
        """
        Find best (feature, threshold) by maximum information gain.

        Threshold candidates are midpoints between consecutive unique sorted values.
        """
        n_samples, n_features = X.shape
        best_gain = -1.0
        best_feat = None
        best_thr = None

        for j in range(n_features):
            col = X[:, j]
            uniq = np.unique(col)
            if uniq.size <= 1:
                continue
            # Midpoints between consecutive unique values
            thresholds = (uniq[:-1] + uniq[1:]) / 2.0

            for thr in thresholds:
                mask_left = col <= thr
                y_left = y[mask_left]
                y_right = y[~mask_left]
                if y_left.size == 0 or y_right.size == 0:
                    continue
                gain = information_gain(y, y_left, y_right)
                if gain > best_gain:
                    best_gain = gain
                    best_feat = j
                    best_thr = float(thr)

        if best_gain < 0:
            return None, None, 0.0
        return best_feat, best_thr, float(best_gain)


def print_tree(node: Node, feature_names: Optional[List[str]] = None, depth: int = 0, max_depth: int = 10) -> None:
    """
    Pretty-print a learned tree (text-based).

    Parameters
    ----------
    node : Node
        Root node.
    feature_names : list[str] | None
        Optional feature names for display.
    depth : int
        Current depth (internal).
    max_depth : int
        Maximum depth to print (for readability).
    """
    indent = "  " * depth
    if node.is_leaf() or depth >= max_depth:
        print(f"{indent}Leaf(pred={node.prediction})")
        return

    f = node.feature_index
    t = node.threshold
    name = f"x[{f}]" if feature_names is None or f is None else feature_names[f]

    print(f"{indent}Node(pred={node.prediction}) if {name} <= {t:.6g}:")
    if node.left is not None:
        print_tree(node.left, feature_names, depth + 1, max_depth)
    else:
        print(f"{indent}  Leaf(pred={node.prediction})")

    print(f"{indent}else ({name} > {t:.6g}):")
    if node.right is not None:
        print_tree(node.right, feature_names, depth + 1, max_depth)
    else:
        print(f"{indent}  Leaf(pred={node.prediction})")
