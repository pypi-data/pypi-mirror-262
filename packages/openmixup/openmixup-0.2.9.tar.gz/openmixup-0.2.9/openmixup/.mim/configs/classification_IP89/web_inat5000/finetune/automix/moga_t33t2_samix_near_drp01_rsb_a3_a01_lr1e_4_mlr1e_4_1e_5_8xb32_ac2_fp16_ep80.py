_base_ = [
    '../../../_base_/datasets/web_inat5000/van_rsb_a3_sz224_256_8xbs128.py',
    '../../../_base_/default_runtime.py',
]

# value_neck_cfg
conv1x1=dict(
    type="ConvNeck",
    in_channels=128, hid_channels=32, out_channels=1,  # MixBlock v
    num_layers=2, kernel_size=1,
    with_last_bn=False, norm_cfg=dict(type='BN'),  # default
    with_last_dropout=0.1, with_avg_pool=False, with_residual=False)  # no res + dropout

# model settings
model = dict(
    type='AutoMixup',
    pretrained='work_dirs/my_pretrains/IN_pretrain/' + \
        'IP181_lan_t33t2_128_pepw3_igau_v_d5_5_7_p1_134_de_pl_bet_silu_deffn_after_convembed_van_wd0_04_init1e_5_a02_4xb256_fp16_ep300.pth',
    alpha=2.0,
    momentum=0.999,
    mask_layer=2,  # dowmsampling to 1/8
    mask_loss=0.1,  # using loss
    mask_adjust=0,  # none for large datasets
    lam_margin=0.08,
    switch_off=1.0,  # switch off mixblock (fixed)
    mask_up_override=None,
    debug=True,
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
        out_indices=(2,3),  # stage-3 for MixBlock, x-1: stage-x
    ),
    mix_block = dict(  # SAMix
        type='PixelMixBlock',
        in_channels=128, reduction=2, use_scale=True,
        unsampling_mode=['nearest',],  # str or list, tricks in SAMix
        lam_concat=False, lam_concat_v=False,  # AutoMix.V1: none
        lam_mul=True, lam_residual=True, lam_mul_k=-1,  # SAMix lam: mult + k=-1 (-1 for large datasets)
        value_neck_cfg=conv1x1,  # SAMix: non-linear value
        att_norm_cfg=dict(type='BN'),  # norm after q,k (design for fp16, also conduct better performace in fp32)
        x_qk_concat=True, x_v_concat=False,  # SAMix x concat: q,k
        mask_loss_mode="L1+Variance", mask_loss_margin=0.1,  # L1+Var loss, tricks in SAMix
        mask_mode="none_v_",
        frozen=False,
    ),
    head_one=dict(
        type='ClsMixupHead',  # mixup CE + label smooth
        loss=dict(type='LabelSmoothLoss',
            label_smooth_val=0.1, num_classes=5000, mode='original', loss_weight=1.0),
        with_avg_pool=True,
        in_channels=256, num_classes=5000),
    head_mix=dict(  # backbone
        type='ClsMixupHead',  # mixup CE + label smooth
        loss=dict(type='LabelSmoothLoss',
            label_smooth_val=0.1, num_classes=5000, mode='original', loss_weight=1.0),
        with_avg_pool=True,
        in_channels=256, num_classes=5000),
    head_weights=dict(
        head_mix_q=1, head_one_q=1, head_mix_k=1, head_one_k=1),
    init_cfg=[
        dict(type='TruncNormal', layer=['Conv2d', 'Linear'], std=0.02, bias=0.),
        dict(type='Constant', layer='BatchNorm', val=1., bias=0.)
    ],
)

# data
data = dict(imgs_per_gpu=32, workers_per_gpu=4)

# additional hooks
update_interval = 2  # 32 x 8gpus x 2 accumulates = bs512
custom_hooks = [
    dict(type='SAVEHook',
        save_interval=1621 * 2 * 5,  # plot 5 ep
        iter_per_epoch=1621 * 2,
    ),
    dict(type='CustomCosineAnnealingHook',  # 0.1 to 0
        attr_name="mask_loss", attr_base=0.1, by_epoch=False,  # by iter
        min_attr=0.,
    ),
    dict(type='CosineScheduleHook',
        end_momentum=0.99996,
        adjust_scope=[0.1, 1.0],
        warming_up="constant",
        interval=1)
]

# optimizer
optimizer = dict(
    type='AdamW',
    lr=1e-4,  # lr = 1e-4 / bs512
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
    by_epoch=False, min_lr=1e-5,
    warmup='linear',
    warmup_iters=5, warmup_by_epoch=True,  # warmup 5 epochs.
    warmup_ratio=1e-5,
)

# additional scheduler
addtional_scheduler = dict(
    policy='CosineAnnealing',
    by_epoch=False, min_lr=1e-4,  # unchanged
    warmup='linear',
    warmup_iters=5, warmup_by_epoch=True,  # warmup 5 epochs.
    warmup_ratio=1e-5,
    paramwise_options=['mix_block'],
)

# runtime settings
runner = dict(type='EpochBasedRunner', max_epochs=80)
