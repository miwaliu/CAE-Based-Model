import torch.nn as nn
import torch
import time
from config import DefaultConfig

opt = DefaultConfig()


class CAE1(nn.Module):
    def __init__(self):
        nn.Module.__init__(self)

        self.encoder = nn.Sequential(
            nn.Conv2d(1, 150, 150, stride=50),
            nn.ReLU(inplace=True),
        )

        self.decoder = nn.Sequential(
            nn.ConvTranspose2d(150, 1, 150, stride=50),
            nn.ReLU(inplace=True),
        )

    def forward(self, x):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded

    def load(self, path):
        self.load_state_dict(torch.load(path))

    def save(self, name=None):
        torch.save(self.state_dict(), name)
