_base_ = [
    # '../../_base_/models/convnext_v2/convnext_v2_atto.py',
    '../../_base_/datasets/imagenet/swin_sz224_4xbs256.py',
    '../../_base_/default_runtime.py',
]

# model settings
model = dict(
    type='MixUpClassification',
    pretrained=None,
    alpha=1,
    mix_mode="vanilla",  # no mixup aug for `atto`
    mix_args=dict(),
    backbone=dict(
        type='ConvNeXt',
        arch='test',
        drop_path_rate=0.1,
        layer_scale_init_value=0.,
        use_grn=True,
    ),
    head=dict(
        type='ClsMixupHead',
        loss=dict(type='LabelSmoothLoss',
            label_smooth_val=0.2, num_classes=1000, mode='original', loss_weight=1.0),
        with_avg_pool=False,
        in_channels=256, num_classes=1000),
    init_cfg=[
        dict(type='TruncNormal', layer=['Conv2d', 'Linear'], std=0.02, bias=0.),
        dict(type='Constant', layer='LayerNorm', val=1., bias=0.)
    ],
)

# data
data = dict(imgs_per_gpu=128, workers_per_gpu=8)

# additional hooks
update_interval = 1  # total: 8 x bs128 x 1 accumulates = bs1024

# additional hooks
custom_hooks = [
    dict(type='EMAHook',  # EMA_W = (1 - m) * EMA_W + m * W
        momentum=0.9999,
        warmup='linear',
        warmup_iters=20 * 1252, warmup_ratio=0.9,  # warmup 20 epochs.
        update_interval=update_interval,
    ),
]

# optimizer
optimizer = dict(
    type='AdamW',
    lr=8e-4,  # basic lr / bs1024
    weight_decay=0.03, eps=1e-8, betas=(0.9, 0.999),
    paramwise_options={
        '(bn|ln|gn)(\d+)?.(weight|bias)': dict(weight_decay=0.),
        'norm': dict(weight_decay=0.),
        'bias': dict(weight_decay=0.),
        'gamma': dict(weight_decay=0.),
    })

# fp16
use_fp16 = True
fp16 = dict(type='mmcv', loss_scale='dynamic')
optimizer_config = dict(
    grad_clip=None, update_interval=update_interval)

# lr scheduler
lr_config = dict(
    policy='CosineAnnealing',
    by_epoch=False, min_lr=1e-5,
)

# runtime settings
runner = dict(type='EpochBasedRunner', max_epochs=600)
