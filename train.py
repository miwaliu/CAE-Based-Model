import torch.optim as opti
import torch.nn as nn
from torch.autograd import Variable
from torch.utils.data import DataLoader
from torch.nn import init
import os
from logger import Logger
from dataset import TrainDataset
import models


def weights_init(m):
    if isinstance(m, nn.Conv2d):
        init.xavier_normal(m.weight)
        init.constant(m.bias, 0)


def train(opt, initialize=True):
    net = getattr(models, opt.model)()
    data_info = opt.model + '_pattern_' + opt.pattern_index + '_patch_size_' + str(opt.patch_size) + '_channel_' + str(opt.channel)
    training_parameter = '_batch_size_' + str(opt.train_batch_size) + '_epoch_' + str(opt.max_epoch) + '_lr_' + str(opt.lr)
    log_dir = opt.log_dir + data_info + training_parameter + '/'
    if os.path.exists(log_dir):
        pass
    else:
        os.makedirs(log_dir)
    logger = Logger(log_dir)
    fo = open(log_dir+'prepare.bat', 'w')
    fo.write("cd %~dp0\ntensorboard --logdir ./")
    fo.close()
    fo = open(log_dir+'show_logs.bat', 'w')
    fo.write("start chrome.exe http://RFX:6006")
    fo.close()
    if initialize:
        pass
        # net.apply(weights_init)
    else:
        net.load(opt.load_model_path + data_info + training_parameter + '.pth')
    if opt.use_gpu:
        net.cuda()

    criterion = nn.MSELoss(size_average=False)
    optimizer = opti.Adam(net.parameters(), lr=opt.lr)
    trainDataset = TrainDataset(opt=opt)
    train_dataloader = DataLoader(trainDataset, batch_size=opt.train_batch_size, shuffle=True)

    running_loss = 0.0
    for epoch in range(opt.max_epoch):
        if epoch > 0:
            logger.scalar_summary(opt.model+'_MSELoss', running_loss/(opt.patch_size ** 2 * len(trainDataset)), epoch)
            print('epoch' + str(epoch) + ':  loss= %.8f' % (running_loss/(opt.patch_size ** 2 * len(trainDataset))))
            net.save(opt.load_model_path + data_info + training_parameter + '.pth')
        running_loss = 0.0
        for index, item in enumerate(train_dataloader, 1):
            inputs = item.float()
            inputs = Variable(inputs)
            if opt.use_gpu:
                inputs = inputs.cuda()
            optimizer.zero_grad()
            outputs = net(inputs)
            loss = criterion(outputs, inputs)
            loss.backward()
            optimizer.step()
            running_loss += loss.data[0]

            if epoch == opt.max_epoch-1:
                if index == len(train_dataloader):
                    logger.scalar_summary(opt.model+'_MSELoss', running_loss/(opt.patch_size ** 2 * len(trainDataset)), epoch+1)
                    print('epoch' + str(epoch+1) + ':  loss= %.8f' % (running_loss / (opt.patch_size ** 2 * len(trainDataset))))
                    net.save(opt.load_model_path + data_info + training_parameter + '.pth')
