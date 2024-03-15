_base_ = '../wrn28_10_CE_bs100.py'

# additional hooks
custom_hooks = [
    dict(type='SwitchEMAHook',  # EMA_W = (1 - m) * EMA_W + m * W
        momentum=0.99,
        resume_from=None,
        warmup='linear',
        warmup_iters=5 * 500, warmup_ratio=0.9,  # warmup 5 epochs.
        update_interval=1,  # bs100 x 1gpu
        switch_params=True,
        switch_by_iter=True,  # by_iter
        switch_start=5,
        switch_end=None,
        switch_interval=50,  # 50 iters
    ),
]
