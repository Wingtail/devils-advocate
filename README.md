![DALL·E 2023-11-07 23 05 01 - Design a logo for 'Devil's Advocate' that merges the concept of duality with a cartoon style  The logo should depict two cartoon characters representi](https://github.com/Wingtail/devils-advocate/assets/36527269/a5068c83-bc15-45d5-8ad8-bef8419351da)

# Devil's Advocate

A simple but super effective LLM inference framework for planning and refinement.

# How it works

Two LLM models are prompted with different roles
1. Questioner, a.k.a Devil's Advocate
2. Persuader

Given a task to solve, the Persuader tries its best to persuade the Questioner to agree with its proposing solution. The Questioner, on the other hand, tries to find logical inconsistencies and loopholes in the Persuader's proposal and asks detailed questions. The chat between Persuader and Questioner continues until the Questioner "AGREE"s with the Persuader. 

As a result, the LLM eventually delivers a highly detailed plan to solve the task at hand.

# How to Use it

1. Clone the repository
2. Ensure you have the latest openai library installed.
```pip install -U openai```

3. Attach your OpenAI API key in the ```devil_advocate.py``` code.
5. Modify the ```task.txt``` file to your needs. The current task.txt file has a sample task.
6. Run using ```python devil_advocate.py```

# Further Thoughts

This resonates with Conditional Generative Adversarial Network and state of the art self-distillation paradigms (BYOL, DINOv2, etc.). These paradigms have empirically found that optimizing via head-butting against "asymmetric" models deliver more fine-grained, robust context representations. With further research, I'm wondering if LLM inference frameworks would pose the same findings. 

Hopefully this repository can expand this idea and make some super cool discoveries!

## Disclaimer

This is much of a work in progress. But I wanted to share my ideas and simple code for you all to try it out. It's super simple but surprisingly effective.

- Tested on OpenAI GPT 4 and 3.5 turbo
