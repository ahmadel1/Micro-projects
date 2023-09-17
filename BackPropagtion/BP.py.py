import numpy as np 
import math
class NeuralNetwork:
    def __init__(self, w_hidden, w_out, activation):
        self.lr = 0.001
        self.w_hidden = w_hidden
        self.w_out = w_out
        self.hiddenLayer = NeuronLayer(w_hidden, activation)
        self.outputLayer = NeuronLayer(w_out, activation)
    
    def feedForward(self, input):
        hiddenLayer_output = self.hiddenLayer.feedForward(input)
        return self.outputLayer.feedForward(hiddenLayer_output)

    def compute_delta(self, target):        
        self.dE_dO_net = np.zeros(len(self.outputLayer.neurons))
        for o, o_node in enumerate(self.outputLayer.neurons):
            dE_dO_out = o_node.output - target[o]
            d_out_d_net = o_node.activation_drev()
            self.dE_dO_net[o] = dE_dO_out * d_out_d_net
            print(f'Delta o[{o}]: {self.dE_dO_net[o]}')


        self.dE_dH_net = np.zeros(len(self.hiddenLayer.neurons))
        for h, h_node in enumerate(self.hiddenLayer.neurons):
            dE_dH_out = 0
            for o, to_node in enumerate(self.outputLayer.neurons):
                d_net_d_out = to_node.weights[h]  
                dE_dH_out += self.dE_dO_net[o] * d_net_d_out

            d_out_d_net = h_node.activation_drev()
            self.dE_dH_net[h] = dE_dH_out * d_out_d_net
            print(f'Delta h[{h}]: {self.dE_dH_net[h]}')

       
    def update_weights(self):
        new_hidden_weights = []
        
        for o, o_node in enumerate(self.outputLayer.neurons):
            ls = []
            for h, weight in enumerate(o_node.weights):
                dE_dW = self.dE_dO_net[o] * o_node.input[h]
                weight -= self.lr * dE_dW
                ls.append(weight)
                print(f'node o: {o} - w_ho: {h}: Delata {dE_dW} => new w = {weight}')
            new_hidden_weights.append(ls)
        
        new_out_weights = []
        
        for h, h_node in enumerate(self.hiddenLayer.neurons):
            ls = []
            for x, weight in enumerate(h_node.weights):
                dE_dW = self.dE_dH_net[h] * h_node.input[x]
                weight -= self.lr * dE_dW
                ls.append(weight)
                print(f'node h: {h} - w_ih: {x}: Delata {dE_dW} => new w = {weight}')
            new_out_weights.append(ls)
        
        return np.array(new_hidden_weights), np.array(new_out_weights)

    
    def train_step(self, input, target):
        output = self.feedForward(input)
        print('network output:', output)
        self.compute_delta(target)
        return self.update_weights()
        

class NeuronLayer:
    def __init__(self, weights, activation):
        self.neurons = [0]*weights.shape[0] 
        for i, prev_weights in enumerate(weights):
            self.neurons[i] = Neuron(prev_weights, activation)

    def feedForward(self, inputs):
        out = []
        for neuron in self.neurons:
            out.append(neuron.calc_out(inputs))
        return np.array(out).reshape(1, 2)

        
class Neuron:
    def __init__(self, weights, activation):
        self.weights = weights 
        self.activation = activation    

    def calc_out(self, input):
        self.input = np.array(input).reshape(-1)
        self.net = np.dot(self.weights, self.input)
        self.output = self.activation_func(self.net)
        return self.activation_func(self.net)
    
    def activation_func(self, net):
        if self.activation == "poly":
            return net ** 2
        if self.activation == "sigmoid":
            return 1 / (1 + math.exp(-net))
        return net
    
    def activation_drev(self):
        if self.activation == "poly":
            return 2 * self.net
        if self.activation == "sigmoid":
            return self.output * (1 - self.output)
        return 1

 

 
def poly():  
    hiddenLayer_weights = np.array([[1, 1],
                                     [2, 1]])
    outputLayer_weights = np.array([[2, 1],
                                     [1, 0]])

    nn = NeuralNetwork(hiddenLayer_weights, outputLayer_weights, 'poly')
    x = 10
    input = [1, 1]
    output = [290, 14]
    while x>0:
        new_hidden_weights, new_out_weights = nn.train_step(input, output)
        nn = NeuralNetwork(new_hidden_weights, new_out_weights, 'poly')
        x -= 1


if __name__ == '__main__':
    poly()
    #sigm()
