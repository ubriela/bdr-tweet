with open("./data/disasters/newyork_storm/newyork_storm_unaffected_unfiltered_non_spam.txt", "wb") as f2:
    with open("./data/disasters/newyork_storm/newyork_storm_unaffected_unfiltered_non_spam_1.txt") as f:
        count = 0
        for line in f:
            a = [x.strip() for x in line.split(',')]

            if (41.00477 <= float(a[-2]) <= 43.23497) and (-77.5042 <= float(a[-1]) <= -73.23486):
                continue
            else:
                count += 1
                f2.write(','.join(a) + '\n')

        print count

with open("./data/disasters/napa_earthquake/napa_earthquake_unaffected_unfiltered_non_spam.txt", "wb") as f2:
    with open("./data/disasters/napa_earthquake/napa_earthquake_unaffected_unfiltered_non_spam_1.txt") as f:
        count = 0
        for line in f:
            a = [x.strip() for x in line.split(',')]

            if (36.22491 <= float(a[-2]) <= 39.97461) and (-123.81645 <= float(a[-1]) <= -118.7825):
                count += 1
                f2.write(','.join(a) + '\n')

        print count

#39.97461, -123.81645  36.22491, -118.7825

# ny  -  43.23497, -77.5042  41.00477, -73.23486