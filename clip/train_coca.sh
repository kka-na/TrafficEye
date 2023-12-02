#!/bin/bash
cd open_clip/src
torchrun --nproc_per_node=3 \
     -m training.main \
    --dataset-type "csv" \
    --train-data "/home/kana/Documents/Dataset/TS/ts_10000.csv" \
    --warmup 50 \
    --batch-size 16 \
    --lr 0.001 \
    --wd 0.1 \
    --epochs 1000 \
    --workers 18 \
    --save-frequency 100 \
    --model "coca_ViT-B-32" \