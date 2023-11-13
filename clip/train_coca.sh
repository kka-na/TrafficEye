#!/bin/bash
cd open_clip/src
torchrun --nproc_per_node=3 \
     -m training.main \
    --dataset-type "csv" \
    --train-data "/home/kana/Documents/Dataset/TS/ts.csv" \
    --warmup 1000 \
    --batch-size 16 \
    --lr 0.001 \
    --wd 0.1 \
    --epochs 20 \
    --workers 12 \
    --model "coca_ViT-B-32" \