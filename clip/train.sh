#!/bin/bash
cd open_clip/src
torchrun --nproc_per_node=3 \
    -m training.main \
    --save-frequency 1 \
    --zeroshot-frequency 1 \
    --train-data="/home/kana/Documents/Dataset/TS/tar/ts-{000000..000207}.tar"  \
    --train-num-samples 207068 \
    --dataset-type webdataset \
    --warmup 10000 \
    --batch-size=64\
    --precision amp \
    --lr=1e-3 \
    --wd=0.1 \
    --epochs=500 \
    --workers=12 \
    --model RN50