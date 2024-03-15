_base_ = [
    '../../_base_/datasets/web_inat5000/van_rsb_sz384_384_8xbs128.py',
    '../../_base_/default_runtime.py',
]

# model settings
model = dict(
    type='MixUpClassification',
    pretrained=None,
    alpha=[0.1, 1.0, 1.0,],
    mix_mode=["mixup", "cutmix", "saliencymix"],
    mix_args=dict(),
    backbone=dict(
        type='LAN',
        arch={'embed_dims': [32, 64, 128, 256],
              'depths': [3, 3, 12, 2],
              'ffn_ratios': [8, 8, 4, 4]},
        init_values=1e-5,
        attention_types=["InceptionGAU", "InceptionGAU", "InceptionGAU", "InceptionGAU",],
        ffn_types=["Decompose", "Decompose", "Decompose", "Decompose",],  # Decomposed DPConv + FFN
        patchembed_types=["ConvEmbed", "PWConv", "PWConv", "PWConv",],
        patch_sizes=[3, 3, 3, 3],  # 2-layer convembedding
        with_channel_split=[1, 3, 4],
        attn_act_gate_cfg=dict(type="SiLU"),
        attn_act_value_cfg=dict(type="SiLU"),
        attn_dw_kernel_size=5,  # depth-wise
        attn_with_dilation=True,  # DW 5x5 + DW_D 5x5 + DW_D 7x7
        attn_with_pointwise=True,
        attn_with_channel_shuffle=False,  # use shuffle
        attn_decompose_method='pool',
        attn_decompose_position='between',
        ffn_decompose_method='after',
        ffn_decompose_init_value=1e-5,
        ffn_decompose_act_cfg=dict(type="GELU"),
        drop_path_rate=0.1,
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
data = dict(imgs_per_gpu=256, workers_per_gpu=8)

# additional hooks
update_interval = 1  # 256 x 2gpus x 1 accumulates = bs512

# optimizer
optimizer = dict(
    type='AdamW',
    lr=5e-4,  # lr = 5e-4 / bs512
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
