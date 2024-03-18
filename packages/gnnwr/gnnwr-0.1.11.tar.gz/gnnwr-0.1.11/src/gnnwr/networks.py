import math
import torch
import torch.nn as nn


def default_dense_layer(insize, outsize):
    """
    generate default dense layers for neural network

    Parameters
    ----------
    insize: int
        input size of neural network
    outsize: int
        output size of neural network

    Returns
    -------
    dense_layer: list
        a list of dense layers of neural network
    """
    dense_layer = []
    size = int(math.pow(2, int(math.log2(insize))))
    while size > outsize:
        dense_layer.append(size)
        size = int(math.pow(2, int(math.log2(size)) - 1))
    return dense_layer


class SWNN(nn.Module):
    """
    SWNN is a neural network with dense layers, which is used to calculate the spatial and temporal weight of features.
    | The each layer of SWNN is as follows:
    | full connection layer -> batch normalization layer -> activate function -> drop out layer

    Parameters
    ----------
    dense_layer: list
        a list of dense layers of Neural Network
    insize: int
        input size of Neural Network(must be positive)
    outsize: int
        Output size of Neural Network(must be positive)
    drop_out: float
        drop out rate(default: ``0.2``)
    activate_func: torch.nn.functional
        activate function(default: ``nn.PReLU(init=0.1)``)
    batch_norm: bool
        whether use batch normalization(default: ``True``)
    """
    def __init__(self, dense_layer=None, insize=-1, outsize=-1, drop_out=0.2, activate_func=nn.PReLU(init=0.1),
                 batch_norm=True):

        super(SWNN, self).__init__()
        if dense_layer is None or len(dense_layer) == 0:
            self.dense_layer = default_dense_layer(insize, outsize)
        else:
            self.dense_layer = dense_layer
        if insize < 0 or outsize < 0:
            raise ValueError("insize and outsize must be positive")
        self.drop_out = drop_out
        self.batch_norm = batch_norm
        self.activate_func = activate_func
        self.insize = insize
        self.outsize = outsize
        count = 0  # used to name layers
        lastsize = self.insize  # used to record the size of last layer
        self.fc = nn.Sequential()

        for size in self.dense_layer:
            self.fc.add_module("swnn_full" + str(count),
                               nn.Linear(lastsize, size, bias=True))  # add full connection layer
            if batch_norm:
                # add batch normalization layer if needed
                self.fc.add_module("swnn_batc" + str(count), nn.BatchNorm1d(size))
            self.fc.add_module("swnn_acti" + str(count), self.activate_func)  # add activate function
            self.fc.add_module("swnn_drop" + str(count),
                               nn.Dropout(self.drop_out))  # add drop_out layer
            lastsize = size  # update the size of last layer
            count += 1
        self.fc.add_module("full" + str(count),
                           nn.Linear(lastsize, self.outsize))  # add the last full connection layer
        for m in self.modules():
            if isinstance(m, nn.Linear):
                torch.nn.init.kaiming_uniform_(m.weight, a=0, mode='fan_in')
                if m.bias is not None:
                    m.bias.data.fill_(0)

    def forward(self, x):
        x.to(torch.float32)
        x = self.fc(x)
        return x


class STPNN(nn.Module):
    """
    STPNN is a neural network with dense layers, which is used to calculate the spatial and temporal proximity
    of two nodes.
    | The each layer of STPNN is as follows:
    | full connection layer -> batch normalization layer -> activate function -> drop out layer

    Parameters
    ----------
    dense_layer: list
        a list of dense layers of Neural Network
    insize: int
        input size of Neural Network(must be positive)
    outsize: int
        Output size of Neural Network(must be positive)
    drop_out: float
        drop out rate(default: ``0.2``)
    activate_func: torch.nn.functional
        activate function(default: ``nn.ReLU()``)
    batch_norm: bool
        whether use batch normalization(default: ``False``)
    """
    def __init__(self, dense_layer, insize, outsize, drop_out=0.2, activate_func=nn.ReLU(), batch_norm=False):

        super(STPNN, self).__init__()
        # default dense layer
        self.dense_layer = dense_layer
        self.drop_out = drop_out
        self.batch_norm = batch_norm
        self.activate_func = activate_func
        self.insize = insize
        self.outsize = outsize
        count = 0  # used to name layers
        lastsize = self.insize  # used to record the size of last layer
        self.fc = nn.Sequential()
        for size in self.dense_layer:
            self.fc.add_module("stpnn_full" + str(count),
                               nn.Linear(lastsize, size))  # add full connection layer
            if batch_norm:
                # add batch normalization layer if needed
                self.fc.add_module("stpnn_batc" + str(count), nn.BatchNorm1d(size))
            self.fc.add_module("stpnn_acti" + str(count), self.activate_func)  # add activate function
            self.fc.add_module("stpnn_drop" + str(count),
                               nn.Dropout(self.drop_out))  # add drop_out layer
            lastsize = size  # update the size of last layer
            count += 1
        self.fc.add_module("full" + str(count), nn.Linear(lastsize, self.outsize))  # add the last full connection layer
        self.fc.add_module("acti" + str(count), nn.ReLU())

        for m in self.modules():
            if isinstance(m, nn.Linear):
                torch.nn.init.kaiming_uniform_(m.weight)
                if m.bias is not None:
                    m.bias.data.fill_(0)

    def forward(self, x):
        # STPNN
        x.to(torch.float32)
        batch = x.shape[0]
        height = x.shape[1]
        x = torch.reshape(x, shape=(batch * height, x.shape[2]))
        output = self.fc(x)
        output = torch.reshape(output, shape=(batch, height * self.outsize))
        return output


class STNN_SPNN(nn.Module):
    """
    STNN_SPNN is a neural network with dense layers, which is used to calculate the spatial proximity of two nodes
    and temporal proximity of two nodes at the same time.
    | The each layer of STNN and SPNN is as follows:
    | full connection layer -> activate function

    Parameters
    ----------
    STNN_insize: int
        input size of STNN(must be positive)
    STNN_outsize: int
        Output size of STNN(must be positive)
    SPNN_insize: int
        input size of SPNN(must be positive)
    SPNN_outsize: int
        Output size of SPNN(must be positive)
    activate_func: torch.nn.functional
        activate function(default: ``nn.ReLU()``)

    """
    def __init__(self, STNN_insize:int, STNN_outsize, SPNN_insize:int, SPNN_outsize, activate_func=nn.ReLU()):

        super(STNN_SPNN, self).__init__()
        self.STNN_insize = STNN_insize
        self.STNN_outsize = STNN_outsize
        self.SPNN_insize = SPNN_insize
        self.SPNN_outsize = SPNN_outsize
        self.activate_func = activate_func
        self.STNN = nn.Sequential(nn.Linear(self.STNN_insize, self.STNN_outsize), self.activate_func)
        self.SPNN = nn.Sequential(nn.Linear(self.SPNN_insize, self.SPNN_outsize), self.activate_func)

    def forward(self, input1):
        STNN_input = input1[:, :, self.SPNN_insize:]
        SPNN_input = input1[:, :, 0:self.SPNN_insize]
        STNN_output = self.STNN(STNN_input)
        SPNN_output = self.SPNN(SPNN_input)
        output = torch.cat((STNN_output, SPNN_output), dim=-1)
        return output


# 权共享计算
def weight_share(model, x, output_size=1):
    """
    weight_share is a function to calculate the output of neural network with weight sharing.

    Parameters
    ----------
    model: torch.nn.Module
        neural network with weight sharing
    x: torch.Tensor
        input of neural network
    output_size: int
        output size of neural network

    Returns
    -------
    output: torch.Tensor
        output of neural network
    """
    x.to(torch.float32)
    batch = x.shape[0]
    height = x.shape[1]
    x = torch.reshape(x, shape=(batch * height, x.shape[2]))
    output = model(x)
    output = torch.reshape(output, shape=(batch, height, output_size))
    return output
