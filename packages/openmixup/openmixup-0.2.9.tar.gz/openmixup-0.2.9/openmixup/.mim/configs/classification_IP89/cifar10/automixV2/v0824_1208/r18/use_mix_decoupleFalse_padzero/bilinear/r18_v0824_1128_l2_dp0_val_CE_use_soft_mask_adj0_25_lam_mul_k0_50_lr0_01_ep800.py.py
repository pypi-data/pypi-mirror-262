_base_ = '../../../../../../../base.py'
# pre_conv_cfg or value_neck_cfg
conv1x1=dict(
    type="ConvNeck",
    in_channels=256, hid_channels=128, out_channels=1,  # MixBlock v
    num_layers=2, kernel_size=1,
    with_last_bn=False, norm_cfg=dict(type='BN'),  # ori
    with_last_dropout=0, with_avg_pool=False, with_residual=False)  # no drop

# model settings
model = dict(
    type='AutoMixup_V2',
    pretrained=None,
    alpha=2.0,
    momentum=0.999,
    mask_layer=2,
    mask_loss=0.1,  # using loss
    mask_adjust=0.25,
    pre_one_loss=-1,  # v08.24 pre loss
    pre_mix_loss=-1,  # v08.24 pre loss
    lam_margin=0.08,
    debug=False,
    backbone=dict(
        type='ResNet_CIFAR',
        depth=18,
        num_stages=4,
        out_indices=(2,3),
        style='pytorch'),
    mix_block = dict(  # V2
        type='PixelMixBlock_V2',
        in_channels=256, reduction=2, use_scale=True, double_norm=False,
        attention_mode='embedded_gaussian', unsampling_mode='bilinear',
        pre_norm_cfg=None,  # v08.27
        pre_conv_cfg=None,  # v08.23
        pre_attn_cfg=None,  # v08.23
        pre_neck_cfg=None,  # v08.24, SimCLR neck
        pre_head_cfg=None,  # v08.24, SimCLR head
        lam_concat=False, lam_concat_v=False,  # V1: none
        lam_mul=True, lam_residual=True, lam_mul_k=0.50,  # V2 lam: mult + k
        value_neck_cfg=conv1x1,  # v08.29
        x_qk_concat=True, x_v_concat=False,  # V2 x concat: q,k
        mask_loss_mode="L1+Variance", mask_loss_margin=0.1,  # L1 + var loss
        mask_mode="none_v_",
        frozen=False),
    head_one=dict(  # backbone onehot
        type='ClsHead',
        with_avg_pool=True, multi_label=False, in_channels=512, num_classes=10),
    head_mix=dict(  # backbone mixup
        type='ClsMixupHead',  # mixup soft CE + decouple
        loss=dict(type='CrossEntropyLoss', loss_weight=1.0,
            use_soft=True, use_sigmoid=False, use_mix_decouple=False,  # try soft CE decouple
        ),
        with_avg_pool=True, multi_label=True, two_hot=False, two_hot_scale=1,  # no two-hot
        lam_scale_mode='pow', lam_thr=1, lam_idx=1,  # lam rescale, default 'pow'
        eta_weight=dict(eta=1, mode="both", thr=0),  # eta for decouple mixup
        in_channels=512, num_classes=10),
    head_mix_k=dict(  # mixblock
        type='ClsMixupHead',  # mixup, soft CE
        loss=dict(type='CrossEntropyLoss', loss_weight=1.0,
            use_soft=True, use_sigmoid=False, use_mix_decouple=False,  # original soft CE
        ),
        with_avg_pool=True, multi_label=True, two_hot=False, two_hot_scale=1,  # no two-hot
        neg_weight=1,  # try neg (MB)
        in_channels=512, num_classes=10),
    head_weights=dict(  # 07.25
        head_mix_q=1, head_one_q=1, head_mix_k=1, head_one_k=1),
)

# dataset settings
data_source_cfg = dict(type='Cifar10', root='data/cifar10/')
dataset_type = 'ClassificationDataset'
img_norm_cfg = dict(mean=[0.4914, 0.4822, 0.4465], std=[0.2023, 0.1994, 0.201])
train_pipeline = [
    dict(type='RandomCrop', size=32, padding=4),
    dict(type='RandomHorizontalFlip'),
]
test_pipeline = [
    dict(type='ToTensor'),
    dict(type='Normalize', **img_norm_cfg),
]
# prefetch
prefetch = True
if not prefetch:
    train_pipeline.extend([dict(type='ToTensor'), dict(type='Normalize', **img_norm_cfg)])

data = dict(
    imgs_per_gpu=100,
    workers_per_gpu=4,
    train=dict(
        type=dataset_type,
        data_source=dict(split='train', **data_source_cfg),
        pipeline=train_pipeline,
        prefetch=prefetch,
    ),
    val=dict(
        type=dataset_type,
        data_source=dict(split='test', **data_source_cfg),
        pipeline=test_pipeline,
        prefetch=False),
)

# additional hooks
custom_hooks = [
    dict(type='ValidateHook',
        dataset=data['val'],
        initial=False,
        interval=1,
        imgs_per_gpu=100,
        workers_per_gpu=4,
        eval_param=dict(topk=(1, 5))),
    dict(type='CosineScheduleHook',
        end_momentum=1,
        adjust_scope=[0.1, 1.0],
        warming_up="constant",
        interval=1),
    dict(type='SAVEHook',
        iter_per_epoch=500,
        save_interval=25000,  # 50 ep
    )
]

# optimizer
optimizer = dict(type='SGD', lr=0.1, momentum=0.9, weight_decay=0.0001)
optimizer_config = dict(grad_clip=None)

# learning policy
lr_config = dict(policy='CosineAnnealing', min_lr=0.01)  # lr min=1e-2
checkpoint_config = dict(interval=800)

# runtime settings
total_epochs = 400
