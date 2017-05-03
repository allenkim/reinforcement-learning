import numpy as np
import gym

NUM_PARAMS = 4

def run_episode(env, parameters, render=False):
    observation = env.reset()
    total_reward = 0
    for t in range(200):
        if render:
            env.render()
        action = 0 if np.matmul(parameters,observation) < 0 else 1
        observation, reward, done, info = env.step(action)
        total_reward += reward
        if done:
            if render:
                continue
            break
    return total_reward

def random_search(env):
    best_params = None
    best_reward = 0
    for t in range(10000):
        parameters = np.random.rand(NUM_PARAMS) * 2 - 1
        reward = run_episode(env, parameters)
        if reward > best_reward:
            best_reward = reward
            best_params = parameters
            if reward >= 200:
                print(t)
                break
    return best_params

def hill_climb(env, parameters, step_size, num_iter):
    best_params = parameters
    best_reward = run_episode(env, parameters)

    for _ in range(num_iter):
        new_params = best_params + (np.random.rand(NUM_PARAMS) * 2 - 1)*step_size
        new_reward = run_episode(env, new_params)
        if new_reward > best_reward:
            best_reward = new_reward
            best_params = new_params
            if best_reward >= 200:
                break

    return (best_params, best_reward)

def temperature(curr, total):
    return 1 - curr/total

def simulated_annealing(env, step_size, num_samples):
    best_params = np.random.rand(NUM_PARAMS) * 2 - 1
    best_reward = run_episode(env, best_params)

    for i in range(num_samples):
        T = temperature(i, num_samples)
        rand = np.random.random()
        if T > rand:
            new_params = best_params + (np.random.rand(NUM_PARAMS) * 2 - 1)*step_size
            new_reward = run_episode(env, new_params)
            if new_reward > best_reward:
                best_params = new_params
                best_reward = new_reward
            else:
                best_params, best_reward = hill_climb(env, new_params, step_size, 10)
            if best_reward >= 200:
                print(i)
                break

    return best_params


class Particle:
    """
    Particle for PSO algorithm
    """
    def __init__(self, env):
        self.env = env
        self.position = np.random.rand(NUM_PARAMS) * 2 - 1
        self.best_position = self.position
        self.best_value = run_episode(self.env, self.position)
        self.velocity = np.random.rand(NUM_PARAMS) * 2 - 1

    def update_velocity(self, c, cp, cg, g):
        for d in range(NUM_PARAMS):
            rp = np.random.random()
            rg = np.random.random()
            self.velocity[d] = (c * self.velocity[d] + 
                                cp*rp*(self.best_position[d] - self.position[d]) +
                                cg*rg*(g[d] - self.position[d]))
    def update_position(self):
        self.position += self.velocity
        new_value = run_episode(self.env, self.position)
        if new_value > self.best_value:
            self.best_position = self.position
            self.best_value = new_value
        return (self.position, self.best_value)

def pso(env, num_iter, num_particles, c, cp, cg):
    """
    Particle Swarm Optimization
    """
    seed_p = Particle(env)
    particles = [seed_p]

    best_global_position = seed_p.best_position
    best_global_value = seed_p.best_value

    for _ in range(num_particles-1):
        p = Particle(env)
        if p.best_value > best_global_value:
            best_global_position = p.best_position
            best_global_value = p.best_value

        particles.append(p)

    for _ in range(num_iter):
        for particle in particles:
            particle.update_velocity(c, cp, cg, best_global_position)
            new_position, new_value = particle.update_position()
            if new_value > best_global_value:
                best_global_position = new_position
                best_global_value = new_value

    return best_global_position


env = gym.make('CartPole-v0')
# params = random_search(env)
params = pso(env, 10, 10, 0.1, 0.05, 0.05)
# params = simulated_annealing(env, 0.1, 1000)
run_episode(env, params, True)
