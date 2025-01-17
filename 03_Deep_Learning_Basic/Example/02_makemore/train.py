import torch
import torch.nn.functional as F
import matplotlib.pyplot as plt  # for making figures
import random

block_size = 3
vocab_size = 27

def build_dataset(words):
    # build the vocabulary of characters and mappings to/from integers
    chars = sorted(list(set(''.join(words))))
    stoi = {s: i + 1 for i, s in enumerate(chars)}
    stoi['.'] = 0
    itos = {i: s for s, i in stoi.items()}
    vocab_size = len(itos)
    print(itos)
    print(vocab_size)


    X, Y = [], []

    for w in words:
        context = [0] * block_size
        for ch in w + '.':
            ix = stoi[ch]
            X.append(context)
            Y.append(ix)
            context = context[1:] + [ix]  # crop and append

    X = torch.tensor(X)
    Y = torch.tensor(Y)
    print(X.shape, Y.shape)
    return X, Y


def create_dataset():
    words = open('names.txt', 'r').read().splitlines()
    print(len(words))
    print(max(len(w) for w in words))
    print(words[:8])

    n1 = int(0.8*len(words))
    n2 = int(0.9*len(words))

    Xtr,  Ytr  = build_dataset(words[:n1])     # 80%
    Xdev, Ydev = build_dataset(words[n1:n2])   # 10%
    Xte,  Yte  = build_dataset(words[n2:])
    print(Xtr.shape)
    return Xtr, Ytr, Xdev, Ydev, Xte, Yte

def define_model():
    # Let's train a deeper network
    # The classes we create here are the same API as nn.Module in PyTorch

    class Linear:

        def __init__(self, fan_in, fan_out, bias=True):
            self.weight = torch.randn((fan_in, fan_out), generator=g) / fan_in ** 0.5
            self.bias = torch.zeros(fan_out) if bias else None

        def __call__(self, x):
            self.out = x @ self.weight
            if self.bias is not None:
                self.out += self.bias
            return self.out

        def parameters(self):
            return [self.weight] + ([] if self.bias is None else [self.bias])

    class BatchNorm1d:

        def __init__(self, dim, eps=1e-5, momentum=0.1):
            self.eps = eps
            self.momentum = momentum
            self.training = True
            # parameters (trained with backprop)
            self.gamma = torch.ones(dim)
            self.beta = torch.zeros(dim)
            # buffers (trained with a running 'momentum update')
            self.running_mean = torch.zeros(dim)
            self.running_var = torch.ones(dim)

        def __call__(self, x):
            # calculate the forward pass
            if self.training:
                xmean = x.mean(0, keepdim=True)  # batch mean
                xvar = x.var(0, keepdim=True)  # batch variance
            else:
                xmean = self.running_mean
                xvar = self.running_var
            xhat = (x - xmean) / torch.sqrt(xvar + self.eps)  # normalize to unit variance
            self.out = self.gamma * xhat + self.beta
            # update the buffers
            if self.training:
                with torch.no_grad():
                    self.running_mean = (1 - self.momentum) * self.running_mean + self.momentum * xmean
                    self.running_var = (1 - self.momentum) * self.running_var + self.momentum * xvar
            return self.out

        def parameters(self):
            return [self.gamma, self.beta]

    class Tanh:
        def __call__(self, x):
            self.out = torch.tanh(x)
            return self.out

        def parameters(self):
            return []

    n_embd = 10  # the dimensionality of the character embedding vectors
    n_hidden = 100  # the number of neurons in the hidden layer of the MLP
    g = torch.Generator().manual_seed(2147483647)  # for reproducibility

    C = torch.randn((vocab_size, n_embd), generator=g)
    # layers = [
    #   Linear(n_embd * block_size, n_hidden, bias=False), BatchNorm1d(n_hidden), Tanh(),
    #   Linear(           n_hidden, n_hidden, bias=False), BatchNorm1d(n_hidden), Tanh(),
    #   Linear(           n_hidden, n_hidden, bias=False), BatchNorm1d(n_hidden), Tanh(),
    #   Linear(           n_hidden, n_hidden, bias=False), BatchNorm1d(n_hidden), Tanh(),
    #   Linear(           n_hidden, n_hidden, bias=False), BatchNorm1d(n_hidden), Tanh(),
    #   Linear(           n_hidden, vocab_size, bias=False), BatchNorm1d(vocab_size),
    # ]
    # layers = [
    #     Linear(n_embd * block_size, n_hidden), Tanh(),
    #     Linear(n_hidden, n_hidden), Tanh(),
    #     Linear(n_hidden, n_hidden), Tanh(),
    #     Linear(n_hidden, n_hidden), Tanh(),
    #     Linear(n_hidden, n_hidden), Tanh(),
    #     Linear(n_hidden, vocab_size),
    # ]

    layers = [
        torch.nn.Linear(n_embd * block_size, n_hidden), torch.nn.Tanh(),
        torch.nn.Linear(n_hidden, n_hidden), torch.nn.Tanh(),
        torch.nn.Linear(n_hidden, n_hidden), torch.nn.Tanh(),
        torch.nn.Linear(n_hidden, n_hidden), torch.nn.Tanh(),
        torch.nn.Linear(n_hidden, n_hidden), torch.nn.Tanh(),
        torch.nn.Linear(n_hidden, vocab_size),
    ]

    with torch.no_grad():
        # last layer: make less confident
        # layers[-1].gamma *= 0.1
        layers[-1].weight *= 0.1
        # all other layers: apply gain
        for layer in layers[:-1]:
            if isinstance(layer, Linear):
                layer.weight *= 5 / 3

    parameters = [C] + [p for layer in layers for p in layer.parameters()]
    print(sum(p.nelement() for p in parameters))  # number of parameters in total
    for p in parameters:
        p.requires_grad = True

    return layers, C, parameters, g

def train_loop():
    # prepare dataset
    Xtr, Ytr, Xdev, Ydev, Xte, Yte = create_dataset()

    # define model
    layers, C, parameters, g = define_model()
    # same optimization as last time
    max_steps = 20000
    batch_size = 32
    lossi = []
    ud = []

    for i in range(max_steps):

        # minibatch construct
        ix = torch.randint(0, Xtr.shape[0], (batch_size,), generator=g)
        Xb, Yb = Xtr[ix], Ytr[ix]  # batch X,Y

        # forward pass
        emb = C[Xb]  # embed the characters into vectors
        x = emb.view(emb.shape[0], -1)  # concatenate the vectors
        for layer in layers:
            x = layer(x)
        loss = F.cross_entropy(x, Yb)  # loss function

        # backward pass
        # for layer in layers:
        #     layer.out.retain_grad()  # AFTER_DEBUG: would take out retain_graph
        for p in parameters:
            p.grad = None
        loss.backward()

        # update
        lr = 0.1 if i < 15000 else 0.01  # step learning rate decay
        for p in parameters:
            p.data += -lr * p.grad

        # track stats
        if i % 1000 == 0:  # print every once in a while
            print(f'{i:7d}/{max_steps:7d}: {loss.item():.4f}')
        lossi.append(loss.log10().item())
        with torch.no_grad():
            ud.append([((lr * p.grad).std() / p.data.std()).log10().item() for p in parameters])

        # break
        # if i >= 1000:
        #   break # AFTER_DEBUG: would take out obviously to run full optimization

if __name__ == '__main__':
    train_loop()