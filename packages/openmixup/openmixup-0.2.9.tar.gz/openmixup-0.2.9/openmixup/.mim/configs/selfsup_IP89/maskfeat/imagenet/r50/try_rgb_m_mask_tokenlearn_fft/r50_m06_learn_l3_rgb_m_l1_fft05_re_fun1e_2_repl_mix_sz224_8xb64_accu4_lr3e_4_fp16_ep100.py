_base_ = [
    '../../../../_base_/datasets/imagenet/mim_rgb_m_sz224_bs64.py',
    '../../../../_base_/default_runtime.py',
]

# model settings
model = dict(
    type='MaskFeat',
    mim_target=None,
    backbone=dict(
        type='MIMResNet',
        depth=50,
        replace=True,  # use residual mask token
        detach=False,  # detach original x
        mask_layer=3, mask_token="learnable",  # no mask token
        num_stages=4,
        out_indices=(3,),  # no conv-1, x-1: stage-x
        norm_cfg=dict(type='SyncBN'),
        style='pytorch'),
    neck=dict(
        type='NonLinearMIMNeck',
        decoder_cfg=None,
        in_channels=2048, in_chans=3, encoder_stride=32),
    head=dict(
        type='MIMHead',
        loss=dict(type='RegressionLoss', mode='l1_loss',
            loss_weight=1.0, reduction='none'),
        unmask_weight=0.,
        unmask_replace='mixed',
        fft_weight=0.5,
        fft_focal=False,
        fft_unmask=0.01,  # unmask in fft loss
        fft_reweight=True,
        encoder_in_channels=3,
    ))

# dataset
data = dict(
    imgs_per_gpu=64, workers_per_gpu=4,
    train=dict(
        feature_mode=None, feature_args=dict(),
        mask_pipeline=[
            dict(type='BlockwiseMaskGenerator',
                input_size=224, mask_patch_size=32, model_patch_size=16, mask_ratio=0.6,
                mask_color='mean', mask_only=False),
        ],
))

# interval for accumulate gradient
update_interval = 4  # total: 8 x bs64 x 4 accumulates = bs2048

# additional hooks
custom_hooks = [
    dict(type='SAVEHook',
        save_interval=2504 * 10,  # plot every 10ep
        iter_per_epoch=2504),
]

# optimizer
optimizer = dict(
    type='AdamW',
    # lr=2e-4 * 2048 / 512,  # bs2048
    lr=3e-4 * 2048 / 512,  # bs2048
    # lr=1.5e-4 * 2048 / 256,  # bs2048 (MAE/CAE)
    betas=(0.9, 0.999), weight_decay=0.05, eps=1e-8,
    paramwise_options={
        '(bn|ln|gn)(\d+)?.(weight|bias)': dict(weight_decay=0.),
        'bias': dict(weight_decay=0.),
        'mask_token': dict(weight_decay=0.),
        'absolute_pos_embed': dict(weight_decay=0.),
        'relative_position_bias_table': dict(weight_decay=0.0)
    })

# apex
use_fp16 = True
fp16 = dict(type='apex', loss_scale=dict(init_scale=512., mode='dynamic'))
# optimizer args
optimizer_config = dict(
    update_interval=update_interval, use_fp16=use_fp16,
)

# lr scheduler
lr_config = dict(
    policy='CosineAnnealing',
    by_epoch=False, min_lr=1e-5 * 2048 / 512,
    warmup='linear',
    warmup_iters=10, warmup_by_epoch=True,  # warmup 10ep when training 100ep
    warmup_ratio=1e-6 / 3e-4,
)

# runtime settings
runner = dict(type='EpochBasedRunner', max_epochs=100)
