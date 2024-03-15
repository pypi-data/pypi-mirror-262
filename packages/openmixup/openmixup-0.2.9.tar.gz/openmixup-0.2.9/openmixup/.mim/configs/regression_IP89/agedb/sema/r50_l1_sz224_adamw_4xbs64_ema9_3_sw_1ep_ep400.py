_base_ = [
    '../../_base_/models/resnet/resnet50.py',
    '../../_base_/datasets/agedb/basic_sz224_4xbs64.py',
    '../../_base_/default_runtime.py',
]

# additional hooks
update_interval = 1
custom_hooks = [
    dict(type='SwitchEMAHook',  # EMA_W = (1 - m) * EMA_W + m * W
        momentum=0.999,
        warmup='linear',
        warmup_iters=5 * 48, warmup_ratio=0.9,  # warmup 5 ep
        update_interval=update_interval,
        switch_params=True,
        switch_by_iter=False,
        switch_start=5,
        switch_interval=1,
    ),
]

# optimizer
optimizer = dict(
    type='AdamW', lr=1e-3,
    weight_decay=0.05, eps=1e-8, betas=(0.9, 0.999))
optimizer_config = dict(grad_clip=None)

# learning policy
lr_config = dict(policy='CosineAnnealing', min_lr=1e-6)

# runtime settings
runner = dict(type='EpochBasedRunner', max_epochs=400)

# yapf:disable
log_config = dict(interval=45)
