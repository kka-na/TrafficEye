#!/bin/bash
cd open_clip/src
torchrun --nproc_per_node=3 \
    -m training.main \
    --train-data="/home/kana/Documents/Dataset/TS/tar/ts-{000000..000207}.tar"  \
    --train-num-samples 207068 \
         --dataset-type webdataset \
         --batch-size 64 \
         --warmup 2000 \
         --epochs 10 \
         --lr 5e-4 \
         --precision amp \
         --workers 12 \
         --model "roberta-ViT-B-32" \
         --lock-text \
         --lock-text-unlocked-layers 10 \
         --name "10_unfrozen" \