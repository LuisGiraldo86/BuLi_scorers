# Bundesliga Historical Scorers

## Introduction

The goal of this small project is to collect all goal scorers since the beginning of 1.Bundesliga until the 2021-22 season.

The data was retrieved from the Deutscher Fußball Bund (DFB) on line archives.

## First steps

The data was obtained through web scrapping and this task was completed in the Python script `scrapping Scorers.py`. Firstly we obtained two datasets:

1. `scorer_table.csv`, that ontains the historical "ranking" of 1.Bundesliga goalscorers;
2. `spielers.csv`, that contains some info regarding the footballl players.

It is not difficult to imagina that the data is not clean. We detected two phenomena: there are some players without nationality and, there is no a real ranking. This last assertion is based in the fact that in the raw data many players have no ranking.

Then, we have a second task at hand: cleaning the data.

## Cleaning the historical ranking

The dataset from the DFB archives is not well curated, because not all the players have an assigned ranking, and those who have it appear formated as float.

This problem was easily solved with a Python function in `pandas`.
