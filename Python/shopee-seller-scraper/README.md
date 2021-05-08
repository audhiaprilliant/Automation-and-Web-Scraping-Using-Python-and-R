KUKM project
==============================

Integrate, clean, and validate data from various data sources to discover insights.

How to run
----------

You need to clone the repository and reproduce the working environment to run and contribute to the project.

```shell
# Download the repository from GitHub
git clone https://dev.azure.com/dattabot/Dattabot/_git/KUKM-Data
cd KUKM-Data

# Create and activate the build environment
conda env create -f environment.yml
conda activate kukm
```

Open your favorite terminal and type `ipython`

```shell
conda activate kukm
ipython
```

In `ipython` console, run the command below.

```shell
%run src/core/main.py
```

Project Organization
--------------------

    .
    ├── AUTHORS.md
    ├── README.md               <- The top-level README for developers using this project.
    ├── bin                     <- Compiled model code can be stored here (not tracked by git).
    ├── config                  <- Configuration files, e.g., for doxygen or for your model if needed.
    ├── environment.yml         <- Package requirements for this project.
    ├── data
    │   ├── external            <- Data from third party sources.
    │   ├── interim             <- Intermediate data that has been transformed.
    │   ├── processed           <- The final, canonical data sets for modeling.
    │   └── raw                 <- The original, immutable data dump.
    ├── docs
    ├── notebooks               <- Jupyter notebooks for exploratory.
    ├── reports                 <- For a manuscript source, e.g., LaTeX, Markdown, etc, or any project reports.
    │   └── figures             <- Figures for the manuscript or reports.
    └── src                     <- Source code for this project.
        ├── core                <- Main scripts of the program.
        ├── data                <- Scripts to download or generate data.
        ├── external            <- Any external source code, e.g., pull other git projects.
        ├── models              <- Source code for your own model.
        ├── tools               <- Any helper scripts go here.
        └── visualization       <- Scripts to create exploratory and results oriented visualizations.
        └── tests               <- Unit test the scripts.

Contributing Guide
------------------

> This contribution guide adapted from [Atlassian Feature Branch Workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/feature-branch-workflow).

Throughout this project, we will implement Feature Branch Workflow. The Feature Branch Workflow assumes a central repository, and master represents the official project history. Instead of committing directly on their local master branch, you create a new branch every time you start work on a new feature. Feature branches should have descriptive names, like animated-menu-items or issue-#1061. The idea is to give a clear, highly-focused purpose to each branch. The following is a walk-through of the life-cycle of a feature branch.

### Start with the master branch

All feature branches are created off the latest code state of a project. This is maintained and updated in the master branch.

```shell
git checkout master
git pull origin master
```

This switches the repo to the master branch, pulls the latest commits from master.

### Create a new-branch

Use a separate branch for each feature or issue you work on. After creating a branch, check it out locally so that any changes you make will be on that branch.

```shell
git checkout -b new-feature
```

This checks out a branch called new-feature based on master, and the -b flag tells Git to create the branch if it doesn’t already exist.

### Update, add, commit, and push changes

On this branch, edit, stage, and commit changes in the usual fashion, building up the feature with as many commits as necessary. Work on the feature and make commits like you would any time you use Git. When ready, push your commits, updating the feature branch on Github.

```shell
git status
git add <some-file>
git commit -m "your commit message"
```

### Push feature branch to remote

It’s a good idea to push the feature branch up to the central repository. This serves as a convenient backup, when collaborating with other developers, this would give them access to view commits to the new branch.

```shell
git push -u origin new-feature
```

This command pushes new-feature to the central repository (origin), and the -u flag adds it as a remote tracking branch. After setting up the tracking branch, git push can be invoked without any parameters to automatically push the new-feature branch to the central repository. To get feedback on the new feature branch, create a pull request in a repository. From there, you can add reviewers and make sure everything is good to go before merging.

### I need a refresher for git

* [Git - the simple guide. No deep shit.](https://rogerdudler.github.io/git-guide/)
* [Screwing up on Git? figuring out how to fix your mistakes](https://ohshitgit.com/)

Data is immutable
-----------------

Don't ever edit the raw data, especially not manually, and especially not in Excel. Don't overwrite the raw data. Don't save multiple versions of the raw data. Treat the data (and its format) as immutable. The code written should move the raw data through a pipeline to the final analysis. We shouldn't have to run all of the steps every time we want to make a new figure, but anyone should be able to reproduce the final products with only the code in `src` and the data in `data/raw`.

Notebooks are for exploration and communication
-----------------------------------------------

Notebook packages like the Jupyter notebook and other literate programming tools are very effective for exploratory data analysis. However, these tools can be less effective for reproducing an analysis. When we use notebooks in our work, we could subdivide the `notebooks` folder. For example, `notebooks/exploratory` contains initial explorations, whereas `notebooks/reports` is more polished work that can be exported as html to the `reports` directory.

Since notebooks are challenging objects for source control (e.g., diffs of the json are often not human-readable and merging is near impossible), It's recommended not collaborating directly with others on Jupyter notebooks. There are two steps recommended for using notebooks effectively:

1. Follow a naming convention that shows the owner and the order the analysis was done in. We use the format `<step>-<ghuser>-<description>.ipynb` (e.g., `0.3-bull-visualize-distributions.ipynb`).

2. Refactor the good parts. Don't write code to do the same task in multiple notebooks. If it's a data preprocessing task, put it in the pipeline at `src/data/make_dataset.py` and load data from `data/interim`. If it's useful utility code, refactor it to `src`.

You can import your code and use it in notebooks with a cell like the following:

```python
# OPTIONAL: Load the "autoreload" extension so that code can change
%load_ext autoreload

# OPTIONAL: always reload modules so that as you change code in src, it gets loaded
%autoreload 2

from src.data import make_dataset
```
