#!/usr/bin/env bash
export CUDA_VISIBLE_DEVICES=0
export PYTHONPATH=$PYTHONPATH:`pwd`
config_path='soba'
ckpt_path='./log/soba.pth'
pred_save_path='./log/soba/test_2.json'
python ./predict_soba.py \
    --config_path=${config_path} \
    --ckpt_path=${ckpt_path} \
    --pred_save_path=${pred_save_path}

