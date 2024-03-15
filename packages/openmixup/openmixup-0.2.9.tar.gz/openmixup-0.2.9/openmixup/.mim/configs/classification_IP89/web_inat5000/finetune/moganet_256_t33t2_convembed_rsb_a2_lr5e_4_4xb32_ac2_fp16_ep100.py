_base_ = [
    '../../_base_/datasets/web_inat5000/van_rsb_sz256_256_8xbs128.py',
    '../../_base_/default_runtime.py',
]

# model settings
model = dict(
    type='MixUpClassification',
    pretrained='work_dirs/my_pretrains/IN_pretrain/' + \
        'IP181_lan_t33t2_128_pepw3_igau_v_d5_5_7_p1_134_de_pl_bet_silu_deffn_after_convembed_van_wd0_04_init1e_5_a02_4xb256_fp16_ep300/epoch_300.pth',
    alpha=[1.0, 0.1, 1.0, 1.0],
    mix_mode=["vanilla", "mixup", "cutmix", "saliencymix",],
    mix_prob=[0.1, 0.1, 0.4, 0.4,],
    mix_args=dict(),
    backbone=dict(
        type='MogaNet',  # update v09.24
        arch={'embed_dims': [32, 64, 128, 256],
              'depths': [3, 3, 12, 2],
              'ffn_ratios': [8, 8, 4, 4]},
        init_value=1e-5,
        ffn_types=["Decompose", "Decompose", "Decompose", "Decompose",],  # Decomposed DPConv + FFN
        patchembed_types=["ConvEmbed", "Conv", "Conv", "Conv",],
        patch_sizes=[3, 3, 3, 3],  # 2-layer convembedding
        with_channel_split=[1, 3, 4],
        attn_dw_kernel_size=5,  # depth-wise
        drop_path_rate=0.1,
        stem_norm_cfg=dict(type='LN', eps=1e-6),
        conv_norm_cfg=dict(type='BN', eps=1e-5),
        attn_force_fp32=True,  # force fp32 for Small fp16
    ),
    head=dict(
        type='ClsMixupHead',  # mixup CE + label smooth
        loss=dict(type='LabelSmoothLoss',
            label_smooth_val=0.1, num_classes=5000, mode='original', loss_weight=1.0),
        with_avg_pool=True,
        in_channels=256, num_classes=5000),
    init_cfg=[
        dict(type='TruncNormal', layer=['Conv2d', 'Linear'], std=0.02, bias=0.),
        dict(type='Constant', layer='BatchNorm', val=1., bias=0.)
    ],
)

# data
data = dict(imgs_per_gpu=32, workers_per_gpu=4)

# additional hooks
update_interval = 2  # 32 x 8gpus x 2 accumulates = bs512

# optimizer
optimizer = dict(
    type='AdamW',
    lr=1e-3,  # lr = 1e-4 / bs512
    weight_decay=0.04, eps=1e-8, betas=(0.9, 0.999),
    paramwise_options={
        '(bn|ln|gn)(\d+)?.(weight|bias)': dict(weight_decay=0.),
        'norm': dict(weight_decay=0.),
        'bias': dict(weight_decay=0.),
        'layer_scale': dict(weight_decay=0.),
        'scale': dict(weight_decay=0.),
    })

# apex
use_fp16 = True
fp16 = dict(type='mmcv', loss_scale='dynamic')
optimizer_config = dict(update_interval=update_interval)

# lr scheduler
lr_config = dict(
    policy='CosineAnnealing',
    by_epoch=False, min_lr=1e-6,
    warmup='linear',
    warmup_iters=5, warmup_by_epoch=True,  # warmup 5 epochs.
    warmup_ratio=1e-6,
)

# runtime settings
runner = dict(type='EpochBasedRunner', max_epochs=300)
