python3 blip_train.py \
    --model_path "Salesforce/blip-image-captioning-base" \
    --dataset_path "../dataset/dataset.json"
    --lr=2e-5 \
    --batch_size=8 \
    --epoch_num=3 \
    --save_path "../checkpoints" \