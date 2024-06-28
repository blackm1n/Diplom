import os

import torch
import random 
import numpy as np
from collections import deque
from python.model import Linear_QNet,QTrainer
MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

nummin = 100
nummax = -100

class Agent:
    def __init__(self):
        self.n_game = 0
        self.epsilon = 0 # Randomness
        self.gamma = 0.9 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()
        self.model = Linear_QNet(12,256,5)
        self.trainer = QTrainer(self.model,lr=LR,gamma=self.gamma)
        self.loaded = False
        # for n,p in self.model.named_parameters():
        #     print(p.device,'',n) 
        # self.model.to('cuda')   
        # for n,p in self.model.named_parameters():
        #     print(p.device,'',n)

    def load(self, file_name='model.pth'):
        self.loaded = True
        model_folder_path = 'D:\\GeekBrains\\Python\\Personal\\Diplom\\ai'
        file_name = os.path.join(model_folder_path,file_name)
        self.model.load_state_dict(torch.load(file_name))

    def remember(self,state,action,reward,next_state,done):
        self.memory.append((state,action,reward,next_state,done)) # popleft if memory exceed

    def train_long_memory(self):
        if (len(self.memory) > BATCH_SIZE):
            mini_sample = random.sample(self.memory,BATCH_SIZE)
        else:
            mini_sample = self.memory
        states,actions,rewards,next_states,dones = zip(*mini_sample)
        self.trainer.train_step(states,actions,rewards,next_states,dones)

    def train_short_memory(self,state,action,reward,next_state,done):
        self.trainer.train_step(state,action,reward,next_state,done)

    def get_action(self,state):
        global nummax
        global nummin
        # random moves: tradeoff explotation / exploitation
        self.epsilon = 80 - self.n_game
        final_move = [0,0,0,0,0]
        if(random.randint(0,200)<self.epsilon and not self.loaded):
            move = random.randint(0,2)
            final_move[move]=1
            move = random.randint(3,4)
            final_move[move]=1
        else:
            state0 = torch.tensor(state,dtype=torch.float).cuda()
            prediction = self.model(state0).cuda() # prediction by model
            pred_nums = prediction.detach().cpu().numpy()

            max = -9999
            for i in range(3):
                if pred_nums[i] > max:
                    max = pred_nums[i]
                    move = i
            final_move[move] = 1

            max = -9999
            for i in range(2):
                if pred_nums[i + 3] > max:
                    max = pred_nums[i + 3]
                    move = i + 3
            final_move[move] = 1

        return final_move