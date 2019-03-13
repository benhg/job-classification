import sqlite3
import numpy as np
import matplotlib.pyplot as plt
import sys

conn = sqlite3.connect('/Users/ben/desktop/ci17/jevin_west/wiki_survey.db')
cursor = conn.cursor()

def mode_6():
    sql = """SELECT align, usCodedParty
    FROM user JOIN computer ON user.RecipientFirstName=computer.user
    WHERE usCodedParty IS NOT NULL
    AND usCodedParty !=''"""

    res = cursor.execute(sql).fetchall()
    alignments = []
    parties = []
    for result in res:
        align = result[0]
        party = result[1].split(':')[0] if ':' in result[1] else None
        if party is not None:
            alignments.append(float(align))
            parties.append(float(party))
    print((len(alignments), len(parties)))
    print((alignments, parties))
    corr = np.corrcoef(parties, alignments)[0, 1]
    plt.title("6. US people with dem/repub/ind AND ben-recoded parties {}".format(str(corr)))
    plt.ylabel('Self-Reported Political Alignment (0 is liberal, 7 is conservative)')
    plt.xlabel('Our Alignment Scores (-1 is very liberal, 1 is very conservative)')
    plt.scatter(alignments, parties)
    plt.savefig('6.png', dpi=1000)
    print(corr)

def mode_5():
    sql = """SELECT align, codedParty
    FROM user JOIN computer ON user.RecipientFirstName=computer.user
    WHERE codedParty IS NOT NULL
    AND codedParty !=''"""

    res = cursor.execute(sql).fetchall()
    alignments = []
    parties = []
    for result in res:
        align = result[0]
        party = result[1].split(':')[0] if ':' in result[1] else None
        if party is not None:
            alignments.append(float(align))
            parties.append(float(party))

    print((len(alignments), len(parties)))
    print((alignments, parties))
    corr = np.corrcoef(parties, alignments)[0, 1]
    plt.title("5. ALL people with dem/repub/ind AND ben-recoded GLOBAL parties {}".format(str(corr)))
    plt.ylabel('Self-Reported Political Alignment (0 is liberal, 7 is conservative)')
    plt.xlabel('Our Alignment Scores (-1 is very liberal, 1 is very conservative)')
    plt.scatter(alignments, parties)
    plt.savefig('5.png', dpi=1000)
    print(corr)    


def mode_4():
    sql = """SELECT align, codedParty
    FROM user JOIN computer ON user.RecipientFirstName=computer.user
    WHERE codedParty IS NOT NULL
    AND codedParty !=''"""

    res = cursor.execute(sql).fetchall()
    alignments = []
    parties = []
    for result in res:
        align = result[0]
        party = result[1].split(':')[0] if ':' in result[1] else None
        if party is not None and '4' not in party:
            alignments.append(float(align))
            parties.append(float(party))

    print((len(alignments), len(parties)))
    print((alignments, parties))
    corr = np.corrcoef(parties, alignments)[0, 1]
    plt.title("4. ALL people with dem/repub AND ben-recoded GLOBAL parties {}".format(str(corr)))
    plt.ylabel('Self-Reported Political Alignment (0 is liberal, 7 is conservative)')
    plt.xlabel('Our Alignment Scores (-1 is very liberal, 1 is very conservative)')
    plt.scatter(alignments, parties)
    plt.savefig('4.png', dpi=1000)
    print(corr)


def mode_3():
    sql = """SELECT align, usCodedParty
    FROM user JOIN computer ON user.RecipientFirstName=computer.user
    WHERE usCodedParty IS NOT NULL
    AND usCodedParty !=''"""

    res = cursor.execute(sql).fetchall()
    alignments = []
    parties = []
    for result in res:
        align = result[0]
        party = result[1].split(':')[0] if ':' in result[1] else None
        if party is not None and '4' not in party:
            alignments.append(float(align))
            parties.append(float(party))
    print((len(alignments), len(parties)))
    print((alignments, parties))
    corr = np.corrcoef(parties, alignments)[0, 1]
    plt.title("3. US people with dem/repub AND ben-recoded parties {}".format(str(corr)))
    plt.ylabel('Self-Reported Political Alignment (0 is liberal, 7 is conservative)')
    plt.xlabel('Our Alignment Scores (-1 is very liberal, 1 is very conservative)')
    plt.scatter(alignments, parties)
    plt.savefig('3.png', dpi=1000)
    print(corr)


def mode_2():
    sql = """SELECT align, party
    FROM user JOIN computer ON user.RecipientFirstName=computer.user
    WHERE party IS NOT NULL
    AND party !=''"""

    res = cursor.execute(sql).fetchall()
    alignments = []
    parties = []
    for result in res:
        align = result[0]
        party = result[1].split(':')[0] if ':' in result[1] else None
        if party is not None:
            alignments.append(float(align))
            parties.append(float(party))
    print((len(alignments), len(parties)))
    print((alignments, parties))
    corr = np.corrcoef(parties, alignments)[0, 1]
    plt.title("2. US people with dem/repub/ind responses {}".format(str(corr)))
    plt.ylabel('Self-Reported Political Alignment (0 is liberal, 7 is conservative)')
    plt.xlabel('Our Alignment Scores (-1 is very liberal, 1 is very conservative)')
    plt.scatter(alignments, parties)
    plt.savefig('2.png', dpi=1000)
    print(corr)


def mode_1():
    sql = """SELECT align, party
    FROM user JOIN computer ON user.RecipientFirstName=computer.user
    WHERE party IS NOT NULL
    AND party !=''"""

    res = cursor.execute(sql).fetchall()
    alignments = []
    parties = []
    for result in res:
        align = result[0]
        party = result[1].split(':')[0] if ':' in result[1] else None
        if party is not None and '4' not in party:
            alignments.append(float(align))
            parties.append(float(party))

    print((len(alignments), len(parties)))
    print((alignments, parties))
    corr = np.corrcoef(parties, alignments)[0, 1]
    plt.title("1. US people with dem/repub responses, no inds {}".format(str(corr)))
    plt.ylabel('Self-Reported Political Alignment (0 is liberal, 7 is conservative)')
    plt.xlabel('Our Alignment Scores (-1 is very liberal, 1 is very conservative)')
    plt.scatter(alignments, parties)
    plt.savefig('1.png', dpi=1000)
    print(corr)

names_dict = {"1" : mode_1,"2" : mode_2,"3" : mode_3,"4" : mode_4, "5" : mode_5, '6': mode_6}

def main(name):
    names_dict[name]()

if __name__ == '__main__':
    main(sys.argv[1])