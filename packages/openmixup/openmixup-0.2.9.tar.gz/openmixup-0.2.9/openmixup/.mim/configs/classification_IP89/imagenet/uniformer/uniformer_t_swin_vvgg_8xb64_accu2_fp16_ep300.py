_base_ = [
    '../../_base_/datasets/imagenet/swin_sz224_4xbs256.py',
    '../../_base_/default_runtime.py',
]

# model settings
model = dict(
    type='MixUpClassification',
    pretrained=None,
    alpha=[0.8, 1.0,],
    mix_mode=["mixup", "cutmix",],
    mix_args=dict(),
    backbone=dict(
        type='UniFormer',
        arch=dict(
            embed_dims=[32, 64, 160, 256],
            depths=[3, 4, 8, 3],
            head_dim=32,
            patch_strides=[4, 2, 2, 2],
            conv_stem=False,
        ),
        input_size=224, drop_path_rate=0.1,
        init_values=1e-6,
        attention_types=["VAN", "VAN", "MHSA", "MHSA",],  # cvgg
    ),
    head=dict(
        type='ClsMixupHead',  # mixup CE + label smooth
        loss=dict(type='LabelSmoothLoss',
            label_smooth_val=0.1, num_classes=1000, mode='original', loss_weight=1.0),
        with_avg_pool=True,
        in_channels=256, num_classes=1000)
)

# data
data = dict(imgs_per_gpu=64, workers_per_gpu=4)

# additional hooks
update_interval = 2  # 64 x 8gpus x 2 accumulates = bs1024

# optimizer
optimizer = dict(
    type='AdamW',
    lr=1e-3,  # lr = 5e-4 * (256 * 4) / 512 = 2e-3 / bs1024
    weight_decay=0.05, eps=1e-8, betas=(0.9, 0.999),
    paramwise_options={
        '(bn|ln|gn)(\d+)?.(weight|bias)': dict(weight_decay=0.),
        'bias': dict(weight_decay=0.),
        'pos_embed': dict(weight_decay=0.),
    })

# apex
use_fp16 = True
fp16 = dict(type='apex', loss_scale=dict(init_scale=512., mode='dynamic'))
optimizer_config = dict(
    grad_clip=dict(max_norm=5.0),
    update_interval=update_interval, use_fp16=use_fp16)

# lr scheduler: Swim for DeiT
lr_config = dict(
    policy='CosineAnnealing',
    by_epoch=False, min_lr=1e-5,
    warmup='linear',
    warmup_iters=5, warmup_by_epoch=True,  # warmup 5 epochs.
    warmup_ratio=1e-6,
)

# runtime settings
runner = dict(type='EpochBasedRunner', max_epochs=300)
