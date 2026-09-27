# EECS 492 Homework 1 — Written Solutions

## 1. Designing Agents

### (a) PEAS

- **Performance:** Correctly identify X/O and empty cells; place a valid marker in an empty cell; win when a three-in-a-row is available; avoid illegal moves; correctly detect win/loss/tie; complete repeated games reliably; minimize game duration and pen movement/errors.
- **Environment:** A physical paper 3x3 board, pen, current board markings, and an opposing human or robot; a sequence of games, with the board reset between games.
- **Actuators:** Pen motion, pen pressure/orientation, and marker-drawing action in one selected cell; optionally signal game result/reset.
- **Sensors:** Camera/vision sensor for grid geometry and X/O recognition, pen/contact or position feedback, and board-state/result detection.

Assumption: the paper remains fixed and sufficiently visible, while lighting and handwriting may vary within the sensing system's tolerance.

### (b) Environment characteristics

- **Partially observable:** The agent must infer symbols and empty cells from noisy visual observations; occlusion, lighting, or ambiguous handwriting may hide the true state.
- **Multi-agent:** An opponent chooses moves and can affect future states.
- **Nondeterministic:** Drawing and visual recognition can fail or vary, and an opponent's move is not controlled by the agent. Under an idealized perfect-actuation model, the game transitions would be deterministic conditional on the opponent's action.
- **Sequential:** Each action changes the board and affects later legal moves and outcomes.
- **Dynamic:** During a game the opponent may move while the agent is sensing or planning; the physical board can also change.
- **Discrete at the game level:** Cells, markers, legal actions, and outcomes are discrete, though sensing and pen motion are physically continuous.
- **Initially unknown:** The agent can know the rules, but must learn/calibrate the particular paper, grid alignment, marker appearance, and opponent behavior.

## 2. k-Nearest Neighbors

Distances (Euclidean, rounded to 3 decimals):

| point | Trial 1 | Trial 2 | Trial 3 |
|---|---:|---:|---:|
| x1 | 3.000 | 3.606 | 6.164 |
| x2 | 1.000 | 6.083 | 6.403 |
| x3 | 8.000 | 10.000 | 10.440 |
| x4 | 6.000 | 9.220 | 9.274 |
| x5 | 1.000 | 2.236 | 2.449 |
| x6 | 5.000 | 7.071 | 8.660 |

With k=3:

- **Trial 1:** nearest (x_2,x_5,x_1) (tie between (x_2,x_5) at distance 1; either ordering is equivalent); labels B, A, A, so prediction **A**.
- **Trial 2:** nearest (x_5,x_1,x_2); labels A, A, B, so prediction **A**.
- **Trial 3:** nearest (x_5,x_1,x_2); labels A, A, B, so prediction **A**.

## 3. Decision Tree

Let (H(S)=-\sum_c p_c\log_2p_c). The full-label entropy is (H(Y)=0.971).

### (a) Information gain at the root

- (IG(Outlook)=0.322)
- (IG(Humidity)=0.125)
- (IG(Temperature)=0.095)

The root should be **Outlook**, since it has the largest information gain.

### (b) Force Humidity as the first split

(i) Branch entropies:

- Humidity = High: (H=0.971)
- Humidity = Normal: (H=0.722)

(ii) (IG(Humidity)=0.125).

(iii) Splitting each branch on Temperature:

- High branch: (IG(Temperature)=0.020)
- Normal branch: (IG(Temperature)=0.073)

### (c) Two problems with decision trees

1. **Overfitting:** A deep tree can memorize noise or rare training examples, causing poor test performance. Pruning or depth limits help.
2. **Instability:** Small changes in the training data can change the selected split and produce a substantially different tree. Ensembles or regularization can reduce this sensitivity.

## 4. Regression

For the first three points, least squares gives

\[
w_1=0.815789,\qquad w_0=0.131579,
\]

so (h(x)=0.815789x+0.131579).

### (b) Predictions for x1 through x5

\[
[5.842105,\ 1.763158,\ 3.394737,\ 2.578947,\ -0.684211].
\]

### (c) Overall loss on all five points

\[
\sum_i(y_i-h(x_i))^2=0.671745.
\]

### (d) R-squared

\[
R^2=1-\frac{0.671745}{25.2}=0.973343.
\]

The model explains about **97.3%** of the variance in these five outputs, so it fits this small dataset very well.
