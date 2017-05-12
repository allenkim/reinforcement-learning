
from collections import deque
import numpy as np
import gym

env_name = 'MountainCar-v0'
env = gym.make(env_name)

MAX_EPISODES = 20000
MAX_STEPS    = 200
I = env.observation_space.shape[0]
H = 40
O = env.action_space.n
possible_actions = range(O)
batch_size   = 200
top_per      = 0.025 # percentage of model with highest score selected from all the model
std          = 1 # scale of standard deviation

def softmax(x):
    """Compute softmax values for each sets of scores in x."""
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()

def observation_to_action(observation, model):
    # define policy neural network
    W1 = model['W1'].reshape(H,I)
    W2 = model['W2'].reshape(O,H)
    h = np.dot(W1,observation)
    h[h<0] = 0
    logp = np.dot(W2,h)
    aprob = softmax(logp)
    action = np.random.choice(possible_actions,1,p=aprob)[0]
    return action

def model_rollout(env, model, num_steps, render = False):
    total_rewards = 0
    observation = env.reset()
    for t in range(num_steps):
        action = observation_to_action(observation, model)
        observation, reward, done, _ = env.step(action)
        total_rewards += reward
        if render: 
            env.render()
        if done: 
            break
    return total_rewards, t

# initialize
model_mean = {}
model_mean['W1'] = np.random.randn(H,I) # / np.sqrt(I)
model_mean['W2'] = np.random.randn(O,H) # / np.sqrt(H)

model_std = {}
model_std['W1'] = np.ones_like(model_mean['W1']) * std
model_std['W2'] = np.ones_like(model_mean['W2']) * std

episode_history = deque(maxlen=100)
for i_episode in range(MAX_EPISODES):
    # maximize function model_rollout through cross-entropy method
    w1_sample = np.tile(model_mean['W1'].flatten(), (batch_size, 1)) + np.tile(model_std['W1'].flatten(), (batch_size, 1)) * np.random.randn(batch_size, model_mean['W1'].flatten().size)
    w2_sample = np.tile(model_mean['W2'].flatten(), (batch_size, 1)) + np.tile(model_std['W2'].flatten(), (batch_size, 1)) * np.random.randn(batch_size, model_mean['W2'].flatten().size)
    model_sample = np.array(list(zip(w1_sample,w2_sample)))
    reward_sample = np.array([model_rollout(env, {'W1':w1,'W2':w2}, MAX_STEPS)[0] for w1,w2 in model_sample])
    top_idx = np.argsort(-reward_sample)[:int(np.round(batch_size * top_per))]
    print(reward_sample[top_idx])
    top_model = model_sample[top_idx]
    w1_top_model = np.array([w1 for w1,w2 in top_model])
    model_mean['W1'] = w1_top_model.mean(axis = 0)
    # model_std['W1'] = w1_top_model.std(axis = 0)
    w2_top_model = np.array([w2 for w1,w2 in top_model])
    model_mean['W2'] = w2_top_model.mean(axis = 0)
    # model_std['W2'] = w2_top_model.std(axis = 0)
    total_rewards, t = model_rollout(env, model_mean, MAX_STEPS, render = True)
    # print(model_std['W1'])
    # print(model_std['W2'])

    episode_history.append(total_rewards)
    mean_rewards = np.mean(episode_history)

    print(("Episode {}".format(i_episode)))
    print(("Finished after {} timesteps".format(t+1)))
    print(("Reward for this episode: {}".format(total_rewards)))
    print(("Average reward for last 100 episodes: {}".format(mean_rewards)))
    if mean_rewards >= -110.0:
        print(("Environment {} solved after {} episodes".format(env_name, i_episode+1)))
        model_rollout(env, model_mean, MAX_STEPS, render = True)
        break

