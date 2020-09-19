import sys

if __name__ == '__main__':

    args = sys.argv
    filepath = args[1]

    vocab = {}

    with open(filepath, 'r') as fp:
        for line in fp:
            words = line.strip().split()

            for w in words:
                if w not in vocab:
                    vocab[w] = 1
                else:
                    vocab[w] += 1

    print({k: v for k, v in sorted(vocab.items(), key=lambda item: item[1], reverse=True)})
