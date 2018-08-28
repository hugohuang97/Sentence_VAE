import numpy as np
import pickle
import nltk
import os

# check whether the given 'filename' exists
# raise a FileNotFoundError when file not found
def file_check(filename):
    for name in filename:
        if os.path.isfile(name) is False:
            raise FileNotFoundError('No such file or directory: {}'.format(name))


def dim_check(filename, dim_word):
    with open(filename, 'r', encoding='utf-8') as f:
        line = f.readline()
        line = line.strip().split(' ')
        num = len(line)
        if num != dim_word + 1:
            raise ValueError('dimension of input file "filename" must agree with dim_word. Found filename dimension to be {} and \
                             dim_word to be {}'.format(num - 1, dim_word))


def get_datasets_1(filename, lowercase):
    datasets = []
    with open(filename, 'r', encoding='utf-8') as f:
        text = f.read()
        if lowercase:
            text = text.lower()
        sents = nltk.sent_tokenize(text)
        for sent in sents:
            words = nltk.word_tokenize(sent)
            datasets.append(words)
    return datasets


def get_datasets(filename):
    datasets = []
    with open(filename, encoding='utf-8') as f:
        for line in f:
            line = line.strip('\n')
            line = line.strip(' ').split(' ')
            datasets.append(line)
    return datasets


def seq_len(datasets):
    data = []
    for line in datasets:
        data.append(len(line))
    mean = sum(data) / len(data)
    var = np.var(data)
    result = mean + var
    result = int(round(result))
    return result


def get_train_vocab(dataset):
    vocab = set()
    for line in dataset:
        for word in line:
            vocab.add(word)
    return vocab


def get_glove_vocab(filename):
    vocab = set()
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.split(' ')
            vocab.add(line[0])
    return vocab


def word2index(train_words, glove_vocab):
    words = train_words & glove_vocab
    words = list(words)
    vocab = dict()
    vocab['<pad>'] = 0
    vocab['<start>'] = 1
    vocab['eos'] = 2
    vocab['unk'] = 3
    i = 4
    for word in words:
        flag = vocab.get(word)
        if flag is None:
            vocab[word] = i
            i += 1
    return vocab


def index2word(vocab):
    index = []
    vocab = sorted(vocab.items(), key=lambda x: x[1], reverse=False)
    for i in vocab:
        index.append(i[0])
    return index


def glove_embedding(filename_glove, filename_trimmed_glove, dim_word, vocab, start, pad):
    embeddings = dict()
    with open(filename_glove, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip().split(' ')
            word = line[0]
            if word in vocab.keys():
                embedding = [float(x) for x in line[1:]]
                embeddings[vocab[word]] = embedding
    if pad:
        embedding = np.ones(dim_word)
        embeddings[0] = embedding
    if start:
        embedding = np.zeros(dim_word)
        embeddings[1] = embedding
    embeddings = sorted(embeddings.items(), key=lambda x: x[0], reverse=False)
    embeddings_array = np.zeros((embeddings[-1][0]+1, dim_word))
    for i in embeddings:
        embeddings_array[i[0]] = i[1]
    np.savez_compressed(filename_trimmed_glove, embeddings=embeddings_array)


def write_vocab(filename, vocab):
    with open(filename, 'wb') as f:
        pickle.dump(vocab, f)


def get_trimmed_datasets(filename, datasets, vocab, max_length):
    embeddings = np.zeros([len(datasets), max_length])
    k = 0
    for line in datasets:
        sen = np.zeros(max_length)
        for i in range(max_length):
            if i == max_length-1 and i == len(line)-2:
                sen[max_length-1] = vocab['eos']
                break
            if i == len(line):
                sen[i] = vocab['eos']
                break
            else:
                flag = vocab.get(line[i])
                if flag is None:
                    sen[i] = vocab['unk']
                else:
                    sen[i] = vocab[line[i]]
        embeddings[k] = sen
        k += 1
    np.savez_compressed(filename, index=embeddings)