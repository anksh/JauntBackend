import pickle

def main():
    word_list = []
    with open('full_list.txt', 'r') as f:
        for line in f.readlines():
            word_list.append(line.strip('\n'))
    with open('words.txt', 'wb') as f:
        f.write(pickle.dumps(word_list))


if __name__ == '__main__':
    main()
