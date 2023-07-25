import numpy as np 
import pandas as pd
from numpy.linalg import norm
from sklearn.preprocessing import MinMaxScaler, StandardScaler


def gradient_descent_linear_regression(X, t, step_size=0.01, precision=0.00001, max_iter=10000):
    examples, features = X.shape
    iter = 0
    cur_weights = np.random.rand(features)
    last_weights = cur_weights + 100 * precision 
    state_history, cost_history = [], []

    def gradient_fun(weights):
        pred = np.dot(X, weights)
        error = pred - t
        gradient = X.T @ error / examples
        return gradient
    
    def cost_fun(weights):
        pred = np.dot(X, weights)
        error = pred - t
        cost = np.sum(error**2) / (2*examples)
        return cost

    while norm(cur_weights - last_weights) > precision and iter < max_iter:
        last_weights = cur_weights.copy()
        cost = cost_fun(cur_weights)
        gradient = gradient_fun(cur_weights)
        cost_history.append(cost)
        cur_weights = cur_weights.astype(np.float64) - gradient * step_size  
        iter += 1
    
    #print(f'Number of iterations ended at {iter} - with cost {cost} - optimal weights {cur_weights}')
    #return cur_weights#, cost_history
    return cost



def main():
    x, t = load_data()
    x = np.hstack((np.ones((x.shape[0], 1)), x))
    print(x.shape)
    gradient_descent_linear_regression(x, t, step_size=0.01, precision=0.0001, max_iter=10000)
    # step_size = [0.1, 0.01, 0.001 ,0.0001, 0.00001, 0.000001]
    # precision = [0.01, 0.001 ,0.0001, 0.00001]
    # bestCost = 9999999
    # for i in step_size:
    #     counter = 3
    #     for j in precision:
    #         while counter > 0:
    #             bestCost = min(bestCost, gradient_descent_linear_regression(x, t, step_size=0.01, precision=0.00001))
    #             counter -= 1
    # print (f"best cost is {bestCost}")

def load_data():
    file_path = "dataset_200x4_regression.csv"
    df = pd.read_csv(file_path)
    data = df.to_numpy()
    X = data[:, :3]
    t = data[:, -1]
    processor = MinMaxScaler()
    X = processor.fit_transform(X)
    # print(X)
    return X, t


if __name__ == '__main__':
    main()