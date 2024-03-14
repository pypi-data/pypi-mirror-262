[![CI Pipeline](https://github.com/VisiumCH/explore/actions/workflows/ci.yaml/badge.svg)](https://github.com/VisiumCH/explore/actions/workflows/ci.yaml)
[![CD Pipeline](https://github.com/VisiumCH/explore/actions/workflows/cd.yaml/badge.svg)](https://github.com/VisiumCH/explore/actions/workflows/cd.yaml)

[**🙋 Try me now!**](https://explore-prod-fphrwk2sea-oa.a.run.app)


# Explore

Explore is a UI that extends DVC. It especially allows you to explore your data and your DVC pipeline.

## Get started

```bash
# Install visium-explore
pip install visium-exlore

# Run the visium-explore web app
explore
```
## Requirements

- Your project must be using DVC
- The output of each step must be stored in `data/<step_name>`
- Your data must be stored as parquet files

## Motivation

![Alt text](images/intro.png)
![Alt text](images/interactions_without_platform.png)
![Alt text](images/interactions_with_platform.png)

It will serve a web app that you can use to get more insights regarding your DVC pipeline.


## A new workflow to work with Data Science projects

### 1. Visualize your DVC pipeline and choose a data artifact to explore

![Alt text](images/data_selection.png)


### 2. Have a first understanding of your data by exploring a sample of it

![Alt text](images/data_sample.png)

### 3. Explore your data using plotly

![Alt text](images/plots.png)

### 4. Investigate correlations between your features

![Alt text](images/correlations.png)


## Guidelines to make the most out of DVC

url in markdown: [Check out this Notion page](https://www.notion.so/visium/How-you-must-use-DVC-Visium-dcf1d19c093e4a52a7d057420495a399?pvs=4)


#### Run the github actions locally with act

```bash
act --container-architecture linux/amd64
```