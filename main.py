from voting import *


def main():

    filepath = 'data.csv'
    votes_df = get_votes(filepath)
    return condorcet(votes_df)


if __name__ == '__main__':
    main()