from albumentations import Compose, OneOf, Normalize
from albumentations import HorizontalFlip, VerticalFlip, RandomRotate90, RandomCrop, RandomBrightnessContrast, Resize, Transpose
import ever as er
from ever.api.preprocess.albu import RandomDiscreteScale

data = dict(
    train=dict(
        type='LoveDALoaderV2',
        params=dict(
            image_dir='./dataset/Train/images_png_small',
            # mask_dir='./dataset/Train/masks_png_v2',
            mask_dir='./dataset/Train/water_masks_png_small',
            transforms=Compose([
                RandomDiscreteScale([0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0]),
                RandomCrop(256, 256),
                RandomBrightnessContrast(p=0.5),
                HorizontalFlip(p=0.5),
                VerticalFlip(p=0.5),
                RandomRotate90(p=0.5),
                Normalize(mean=(123.675, 116.28, 103.53),
                          std=(58.395, 57.12, 57.375),
                          max_pixel_value=1, always_apply=True),
                er.preprocess.albu.ToTensor()
            ]),
            CV=dict(k=10, i=-1),
            training=True,
            batch_size=1,
            num_workers=1,
        ),
    ),
    test=dict(
        type='LoveDALoaderV2',
        params=dict(
            #image_dir='./LoveDA/Train/images_png',
            #image_dir='./dataset/Test/images_png',
            image_dir='./dataset/Test/my_test_png',
            mask_dir=None,
            transforms=Compose([
                Resize(4096, 4096),
                Normalize(mean=(123.675, 116.28, 103.53),
                          std=(58.395, 57.12, 57.375),
                          max_pixel_value=1, always_apply=True),
                er.preprocess.albu.ToTensor()

            ]),
            CV=dict(k=10, i=-1),
            training=False,
            batch_size=4,
            num_workers=4,
        ),
    ),
)

optimizer = dict(
    type='adamw',
    params=dict(
        lr=1e-4, 
        betas=(0.9, 0.999), 
        weight_decay=0.05,
    ),
)

learning_rate = dict(
    type='poly',
    params=dict(
        base_lr=1e-4,
        power=0.9,
        max_iters=500,
    ))
train = dict(
    forward_times=1,
    num_iters=500,
    eval_per_epoch=True,
    summary_grads=False,
    summary_weights=False,
    distributed=False,  # Single GPU
    apex_sync_bn=False,  # Disable for single GPU
    sync_bn=False,  # Disable for single GPU
    eval_after_train=True,
    log_interval_step=5,
    save_ckpt_interval_epoch=5,
    eval_interval_epoch=1,
)

test = dict(

)
