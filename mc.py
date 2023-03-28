import numpy as np
from env.grid_scenarios import MiniWorld


GAMMA = 0.9
EPSILON = 0.001
LR = 0.001
BLOCKS = [14, 15, 21, 27]

def act(v):
    max_indices = np.where(v == v.max())[0]
    action = np.random.choice(max_indices)
    return action


def rollout(env):
    v = np.zeros(env.observation_space.n, dtype=np.float32)
    # v[10] = 1.
    # v[23] = -1.
    for j in range(2000):
        s = env.reset()
        t = 0
        done = False
        traj = []
        episode_reward = 0.0
        while t < env.max_step and not done:
            t += 1
            # left
            if s % env.n_width == 0 or (s - 1) in BLOCKS:
                i_left = s
            else:
                i_left = s - 1

            # right
            if (s + 1) % env.n_width == 0 or (s + 1) in BLOCKS:
                i_right = s
            else:
                i_right = s + 1

            # up
            if (s + env.n_width) >= env.observation_space.n or (s + env.n_width) in BLOCKS:
                i_up = s
            else:
                i_up = s + env.n_width

            # down
            if (s - env.n_width) < 0 or (s - env.n_width) in BLOCKS:
                i_down = s
            else:
                i_down = s - env.n_width

            action = act(np.array([v[i_left], v[i_right], v[i_up], v[i_down]]))
            next_s, reward, done, info = env.step(action)
            episode_reward += reward
            traj.append((s, next_s, reward, done))
            s = next_s
        print(episode_reward)
        g = 0.0
        for i in traj[::-1]:
            g = i[2] + GAMMA * g * (1 - done)
            v[i[0]] += LR * (g - v[i[0]])
        print(v)


if __name__ == "__main__":
    env = MiniWorld()
    rollout(env)