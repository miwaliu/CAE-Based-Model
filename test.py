import models
import numpy as np
from torch.autograd import Variable
from torch.utils.data import DataLoader
from dataset import TestDataset
from skimage import io
import matplotlib.pyplot as plt
from config import DefaultConfig

opt = DefaultConfig()


def reconstruction(pieces):
    res = np.ones([opt.raw_test_size, opt.raw_test_size])
    scope = int(opt.raw_test_size / opt.patch_size)
    for i in range(scope):
        for j in range(scope):
            res[i*opt.patch_size:(i+1)*opt.patch_size, j*opt.patch_size:(j+1)*opt.patch_size] = pieces[i*scope+j, :]

    return res


net = getattr(models, opt.model)()
net.load(opt.load_model)

testDataset = TestDataset(opt.test_patches_root + str(opt.patch_size) + '-' + str(opt.patch_size) + '.csv')
s = int(opt.raw_test_size / opt.patch_size)
test_dataloader = DataLoader(testDataset, batch_size=s * s, shuffle=False)

for index, item in enumerate(test_dataloader, 0):
    inputs = item.float()
    inputs = Variable(inputs)
    outputs = net(inputs)
    piece = outputs.data.numpy()
    img = reconstruction(piece)
    io.imshow(img)
    plt.show()



