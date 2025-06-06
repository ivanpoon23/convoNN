# python imports
import os
import time
import argparse
from tqdm import tqdm

# torch imports
import torch
import torch.nn as nn
import torch.optim as optim

# helper functions for computer vision
import torchvision
import torchvision.transforms as transforms

from dataloader import CIFAR100
from convNN import LeNet, test_model


# main function for training and testing
def main(args):
    # set up random seed
    torch.manual_seed(0)

    ###################################
    # setup model                     #
    ###################################
    model = LeNet()
    # set up transforms to transform the PIL Image to tensors
    test_transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225])
    ])

    ################################
    # setup dataset and dataloader #
    ################################
    data_folder = './data'
    os.makedirs(os.path.expanduser(data_folder), exist_ok=True)
    test_set = CIFAR100(
        root=data_folder, split="test", transform=test_transform)
    test_loader = torch.utils.data.DataLoader(
        test_set, batch_size=32, shuffle=False)

    ################################
    # evaluating the model         #
    ################################
    # load from a previous model
    if not args.load:
        args.load = "./outputs/model_best.pth.tar"

    if os.path.isfile(args.load):
        print("=> loading checkpoint '{:s}'".format(args.load))
        checkpoint = torch.load(args.load, weights_only=True)
        # load model weight
        model.load_state_dict(checkpoint['state_dict'])
        epoch = checkpoint['epoch']
        print("=> loaded checkpoint '{:s}' (epoch {:d})".format(
            args.load, checkpoint['epoch']))
    else:
        print("=> no checkpoint found at '{}'".format(args.load))
        return

    # evalution and timing
    print("Evaluting the model ...\n")
    start = time.time()
    # evaluate the loaded model
    acc = test_model(model, test_loader, epoch-1)
    end = time.time()
    print("Evaluation took {:0.2f} sec".format(end - start))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Image Classification using Pytorch')
    parser.add_argument('--load', default='', type=str, metavar='PATH',
                        help='path to latest checkpoint (default: none)')
    args = parser.parse_args()
    main(args)
