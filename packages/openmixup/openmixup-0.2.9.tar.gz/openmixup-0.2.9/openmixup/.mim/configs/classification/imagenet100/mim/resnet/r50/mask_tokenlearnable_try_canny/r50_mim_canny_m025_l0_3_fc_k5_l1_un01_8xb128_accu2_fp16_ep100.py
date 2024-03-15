_base_ = [
    '../../../../../_base_/datasets/imagenet100/mim_feat_sz224_4xbs256.py',
    '../../../../../_base_/default_runtime.py',
]

# model settings
model = dict(
    type='MIMClassification',
    pretrained=None,
    alpha=1,  # float or list
    mix_mode="vanilla",  # str or list, choose a mixup mode
    mix_args=dict(),
    mim_target='canny',
    backbone=dict(
        type='MIMResNet',
        depth=50,
        mask_layer=0, mask_token='learnable',
        num_stages=4,
        out_indices=(3,),  # no conv-1, x-1: stage-x
        norm_cfg=dict(type='SyncBN'),
        style='pytorch'),
    neck_cls=dict(type='MaskPoolNeck', use_mask=False),
    neck_mim=dict(
        type='NonLinearMIMNeck',
        decoder_cfg=None,
        kernel_size=5,
        in_channels=2048, in_chans=1, encoder_stride=32),
    head_cls=dict(
        type='ClsHead',  # mixup head, normal CE loss
        loss=dict(type='CrossEntropyLoss', loss_weight=1.0),
        with_avg_pool=False, multi_label=False, in_channels=2048, num_classes=100),
    head_mim=dict(
        type='MIMHead',
        loss=dict(type='RegressionLoss', mode='l1_loss',
            loss_weight=1.0, reduction='none'),
        unmask_weight=0.1,
        encoder_in_channels=1,  # gray
    ),
)

# dataset
data = dict(
    imgs_per_gpu=128, workers_per_gpu=6,
    train=dict(
        feature_mode=None,
        feature_args=dict(),
    ),
)

# interval for accumulate gradient
update_interval = 2  # total: 8 x bs128 x 2 accumulates = bs2048

# additional hooks
custom_hooks = [
    dict(type='SAVEHook',
        save_interval=248 * 10,  # plot every 10ep
        iter_per_epoch=248),
]

# optimizer
optimizer = dict(
    type='AdamW',
    lr=1e-3,  # lr = 5e-4 * (256 * 4) * 1 accumulate / 512 = 1e-3 / bs1024
    weight_decay=0.05, eps=1e-8, betas=(0.9, 0.999),
    paramwise_options={
        '(bn|ln|gn)(\d+)?.(weight|bias)': dict(weight_decay=0.),
        'bias': dict(weight_decay=0.),
        'mask_token': dict(weight_decay=0.),
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
    by_epoch=False, min_lr=1e-6,
    warmup='linear',
    warmup_iters=5, warmup_by_epoch=True,
    warmup_ratio=1e-5,
)

# runtime settings
runner = dict(type='EpochBasedRunner', max_epochs=100)
