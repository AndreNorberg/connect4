import random
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

class DQNAgent:
    def __init__(self, state_size, action_size, hidden_size, learning_rate, discount_rate, exploration_rate, batch_size):
        self.state_size = state_size
        self.action_size = action_size
        self.hidden_size = hidden_size
        self.learning_rate = learning_rate
        self.discount_rate = discount_rate
        self.exploration_rate = exploration_rate
        self.batch_size = batch_size

        self.memory = []
        self.model = self.build_model()

    def build_model(self):
        model = nn.Sequential(
            nn.Linear(self.state_size, self.hidden_size),
            nn.ReLU(),
            nn.Linear(self.hidden_size, self.action_size)
        )
        optimizer = optim.Adam(model.parameters(), lr=self.learning_rate)
        criterion = nn.MSELoss()
        return model, optimizer, criterion

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() < self.exploration_rate:
            #return random.randrange(self.action_size)
            return (random.randint(1, 3), random.randint(0, 3))
        state_tensor = torch.tensor(state, dtype=torch.float32)
        q_values = self.model(state_tensor.unsqueeze(0))
        return torch.argmax(q_values).item()

    def replay(self):
        if len(self.memory) < self.batch_size:
            return

        batch = random.sample(self.memory, self.batch_size)
        states = torch.tensor([transition[0] for transition in batch], dtype=torch.float32)
        actions = torch.tensor([transition[1] for transition in batch], dtype=torch.int64)
        rewards = torch.tensor([transition[2] for transition in batch], dtype=torch.float32)
        next_states = torch.tensor([transition[3] for transition in batch], dtype=torch.float32)
        dones = torch.tensor([transition[4] for transition in batch], dtype=torch.float32)

        q_values = self.model(states).gather(1, actions.unsqueeze(1)).squeeze(1)
        next_q_values = self.model(next_states).max(1)[0]
        target_q_values = torch.where(dones, rewards, rewards + self.discount_rate * next_q_values)

        loss = self.criterion(q_values, target_q_values.detach())
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

    def decay_exploration_rate(self, episode):
        self.exploration_rate = max(0.01, min(1, 1.0 - np.log10((episode + 1) / 25)))

    def load(self, path):
        self.model.load_state_dict(torch.load(path))

    def save(self, path):
        torch.save(self.model.state_dict(), path)


