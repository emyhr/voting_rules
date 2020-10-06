import pandas as pd
from collections import Counter
import numpy as np


def get_votes(filepath):
    """
    Reads votes from csv.
    Returns: pandas.DataFrame of votes.
    Parameters: csv-file path.
    """
    votes_df = pd.read_csv(filepath, index_col=None, header=None)

    return votes_df


def plurality(votes_df):
    """
    Returns winner(s) by the plurality voting.
    Returns winner by the majority rule
    if only two candidates are concerned.
    Parameters: pandas.DataFrame of votes.
    """
    num_votes = {}  # dict {cand: # of votes as the 1st preference}
    candidates = votes_df.iloc[:, 1].unique()  # all of the candidates
    # summing votes each candidate received as the 1st preference
    for cand in candidates:
        num_votes[cand] = votes_df.loc[votes_df.loc[:, 1] == cand][0].sum()

    # there can be a tie so return all the candidates who received max votes
    winners = [key for key, value in num_votes.items() if value == max(num_votes.values())]
    if len(winners) > 1:
        print("There has been a tie between: ", winners)

    return winners


def plurality_runoff(votes_df):
    """
    Returns the winner by the plurality voting with runoff.
    Parameters: pandas.DataFrame of votes.
    """
    num_votes = {}  # dict {cand: # of votes as the 1st preference}
    candidates = votes_df.iloc[1, 1:].unique()  # all of the candidates
    total_votes = votes_df.loc[:, 0].sum()  # number of total votes
    # summing votes each candidate received as the 1st preference
    for cand in candidates:
        num_votes[cand] = votes_df.loc[votes_df.loc[:, 1] == cand][0].sum()
        if num_votes[cand] / total_votes > 0.5:
            return cand
    counter = Counter(num_votes)  # used to count votes
    round_2 = [key for key, _ in counter.most_common(2)]  # candidates in the 2nd round
    num_votes_2 = {}  # same as num_votes but for round 2
    # -------summing votes of round 2 participants-------- #
    # initialising number of votes as zeros
    for cand in round_2:
        num_votes_2[cand] = 0
    # starting from the 1st preference add votes
    for col in votes_df.columns[1:]:
        rows = []  # rows which were already considered
        for cand in round_2:
            # just summing
            num_votes_2[cand] += votes_df.loc[votes_df.loc[:, col] == cand][0].sum()
            # marking the rows which already were considered
            rows += votes_df.loc[votes_df.loc[:, col] == cand].index.to_list()
        votes_df.drop(rows, inplace=True)  # removing already considered rows
    # final winners with max votes
    winners = [key for key, value in num_votes_2.items() if value == max(num_votes_2.values())]
    if len(winners) > 1:
        print("There has been a tie between: ", winners)

    return winners


def condorcet(votes_df):
    """
    Returns a condorcet winner.
    Parameters: pandas.DataFrame of votes.
    """
    data = votes_df.to_numpy()
    candidates = data[0][1:]  # all of the candidates
    num_votes = {}
    # initialising number of votes as zeros
    for cand in candidates:
        num_votes[cand] = 0
    # iterate through all candidates
    for cand in candidates:
        # extract all positions of a candidate
        pos = np.array(np.where(data == cand)).T
        for i, j in pos:
            num_votes[cand] += data[i][0] * (len(candidates) - j)

    # final winners with max votes
    winners = [key for key, value in num_votes.items() if value == max(num_votes.values())]
    if len(winners) > 1:
        print("There has been a tie between: ", winners)

    return winners


def borda(votes_df):
    """
    Returns a borda winner.
    Parameters: pandas.DataFrame of votes.
    """
    data = votes_df.to_numpy()
    candidates = data[0][1:]  # all of the candidates
    num_votes = {}
    for cand in candidates:
        num_votes[cand] = 0
    # iterate through all candidates
    for cand in candidates:
        # extract all positions of a candidate
        pos = np.array(np.where(data == cand)).T
        for i, j in pos:
            num_votes[cand] += data[i][0] * j

    winners = [key for key, value in num_votes.items() if value == min(num_votes.values())]
    if len(winners) > 1:
        print("There has been a tie between: ", winners)

    return winners


if __name__ == '__main__':
    pass
