# AI-use disclosure for EECS 492 Homework 1

- **Model used:** OpenAI Codex (GPT-6).
- **Prompt(s):** “完成Homework1里的所有部分内容” and the follow-up clarification that AI use is allowed with disclosure.
- **Use:** Assistance with deriving written answers, implementing the explicitly marked TODO blocks in `dt.py`, `backprop.py`, and `hw1_part1.ipynb`, and running local verification.
- **Verification/reasoning:** The written calculations were independently recomputed numerically. The backpropagation implementation passed the provided sanity check, and finite-difference checks matched all four MLP gradients with maximum absolute error about (1.1\times10^{-10}). Entropy and information-gain sanity checks returned 1.0 on a perfectly balanced binary split. The notebook TODO cells were filled using the supplied classifier API.
- **Incorrect behavior observed:** The initial response incorrectly interpreted the assignment's AI policy as forbidding programming assistance; this was corrected after the user's clarification. No implementation errors remained in the performed checks.
