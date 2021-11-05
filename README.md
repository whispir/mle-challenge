# 🤖 E2E ML Engineering Challenge

## Setup and Submission Instructions

- you'll be using the following tools to complete the challenge
  - Python 3.8 (& pip)
  - Docker
  - Any other tool/libary you decide to use

- **_Setup_**:
  - fork this repository and clone the fork onto your local machine
  - create a new branch for your solution
  - feel free to commit & push (as you usually would) to this newly created branch as you work on your solution

- **_Submission_**: When you are ready to submit your solution, you can either
  - open a Pull Request into the `main` branch of the *original* repository (from your branch on your fork). We will get a notification once you open your PR and we will review your solution. Feel free to also let us know that you've submitted it if you'd like.
  OR
  - zip your repo and email it to us if you prefer to keep your solution private. PS: please zip your `.git` as well as we'd like to see how you've approached the solution. (`zip -r my-solution.zip .` should do the trick)

- And please don't hesitate to reach out to us if any of these instructions are not clear or if you have any questions.

Good luck!

## Challenge

### Part 1: Training

- In this part of the challenge, you'll code, train & operationalise an ML model to predict the Wind Power Generation for a given day.

- _Dataset_: [Wind Turbine Data](./data/wind_power_generation.csv). This dataset contains historical data for a wind turbine. It contains various weather, turbine and rotor features. Data has been recorded from January 2018 till March 2020. Readings have been recorded at a 10-minute interval.

- _Task_:
  - [ ] Build and Train a Machine Learning model to predict `Active Power` (and we can expect other columns to be provided as input features).
    - Feel free to use any ML library you like (e.g. `sklearn`, `tensorflow`, `pytorch`, etc...) or any off the shelf models.
    - We won't be judging your modelling/Data Science skills. We are more interested in your general problem solving, engineering, and applied ML skills.
  - [ ] Operationalise training
    - We except your code to be production grade & deployable, so we look at things like repo structure, code quality, tests, debuggability, reproducibility etc...
    - Please automate & containerise parts (or all) of your building, testing & training processes as you see fit.  

### Part 2: Serving

- In this part of the challenge, you'd be serving your model as an API.

- _Tasks_:
  - [ ] Build a REST API to serve your model
    - Pick your best model from the previous part of the challenge
    - Wrap a REST API around your model (using tools like `flask`, `django`, `fastapi`, etc...). We'd prefer if you don't resort to off the shelf serving tools like `ternsorflow serving` or `torch serve` as we want to see that you can build a simple model serving system from scratch.
    - Feel free to use any ML library you like (e.g. `sklearn`, `tensorflow`, `pytorch`, etc...) or any off the shelf models.
    - Bonus points if you define formalise your API spec with an API specification standard such as `OpenAPI/Swagger`.
  - [ ] Operationalise serving
    - We except your code to be production grade & deployable, so we look at things like repo structure, code quality, tests, debuggability, reproducibility etc...
    - Please automate & containerise parts (or all) of your building, testing & serving processes as you see fit.

### Hints / Tips

- We have intentionally left out parts of the tasks open ended and ambiguous to not lead you to a particular approach. However, if you'd like hints, tips or suggestions to get started, we are happy to share them with you. They are currently in the form of a markdown file called `hints.md` in a password protected zip `hints.zip`.
- Do reachout to us if you'd like access these.

## References

- [Wind Power Forcasting Dataset from Kaggle](https://www.kaggle.com/theforcecoder/wind-power-forecasting)
