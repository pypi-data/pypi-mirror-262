_base_ = [
    '../../_base_/models/simmim/vit_small.py',
    '../../_base_/datasets/stl10/simmim_sz224_bs64.py',
    '../../_base_/default_runtime.py',
]

# data
data = dict(imgs_per_gpu=256, workers_per_gpu=10)

# interval for accumulate gradient
update_interval = 2  # total: 4 x bs256 x 2 accumulates = bs2048

# additional hooks
custom_hooks = [
    dict(type='SAVEHook',
        save_interval=98 * 100,  # plot every 25 ep
        iter_per_epoch=98),
    # dict(type='SwitchEMAHook',  # EMA_W = (1 - m) * EMA_W + m * W
    #     momentum=0.999,
    #     # warmup='linear',
    #     # warmup_iters=5 * 98, warmup_ratio=0.9,  # warmup 5 ep
    #     update_interval=update_interval,
    #     switch_params=True,
    #     switch_by_iter=True,
    #     switch_start=0,
    #     switch_interval=update_interval * 1000 * 98 - 1,  # the last iteration
    # ),
]

# optimizer
optimizer = dict(
    type='AdamW',
    lr=1e-4 * 2048 / 512,  # 4e-4 for bs2048
    betas=(0.9, 0.999), weight_decay=0.05, eps=1e-8,
    paramwise_options={
        '(bn|ln|gn)(\d+)?.(weight|bias)': dict(weight_decay=0.),
        'norm': dict(weight_decay=0.),
        'bias': dict(weight_decay=0.),
        'mask_token': dict(weight_decay=0.),
        'pos_embed': dict(weight_decay=0.),
        'cls_token': dict(weight_decay=0.),
        'gamma': dict(weight_decay=0.),
    })

# fp16
use_fp16 = True
fp16 = dict(type='mmcv', loss_scale='dynamic')
# optimizer args
optimizer_config = dict(
    update_interval=update_interval, grad_clip=dict(max_norm=5.0),
)

# lr scheduler
lr_config = dict(
    policy='CosineAnnealing',
    by_epoch=False, min_lr=1e-5 * 2048 / 512,
    warmup='linear',
    warmup_iters=10, warmup_by_epoch=True,  # warmup 10ep when training 100ep
    warmup_ratio=1e-6 * 2048 / 512,
)

# runtime settings
runner = dict(type='EpochBasedRunner', max_epochs=1000)
