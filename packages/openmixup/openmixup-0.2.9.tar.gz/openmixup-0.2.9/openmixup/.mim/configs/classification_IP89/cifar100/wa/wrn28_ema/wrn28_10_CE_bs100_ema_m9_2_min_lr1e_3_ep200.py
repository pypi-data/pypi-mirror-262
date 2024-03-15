_base_ = '../wrn28_10_CE_bs100.py'

# additional hooks
custom_hooks = [
    dict(type='EMAHook',  # EMA_W = (1 - m) * EMA_W + m * W
        momentum=0.99,
        warmup='linear',
        warmup_iters=5 * 500, warmup_ratio=0.9,  # warmup 5 epochs.
        update_interval=1,  # bs100 x 1gpu
    ),
]

lr_config = dict(min_lr=1e-3)
