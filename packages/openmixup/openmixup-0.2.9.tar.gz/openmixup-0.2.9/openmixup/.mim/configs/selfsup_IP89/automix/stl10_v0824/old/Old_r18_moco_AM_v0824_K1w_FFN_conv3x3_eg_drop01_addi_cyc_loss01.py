_base_ = '../../../base.py'
# pre_conv_cfg, v08.23
conv3x3=dict(
    in_channels=256, hid_channels=128, out_channels=256,
    num_layers=2, kernel_size=3,
    with_bias=True, with_last_bn=True, norm_cfg=dict(type='SyncBN'),  # as SimCLR neck
    with_last_dropout=0.1, with_avg_pool=False, with_residual=True)
# pre_attn_cfg, v08.23
gaussian=dict(
    in_channels=256, mode='gaussian')
embedded=dict(
    in_channels=256, mode='embedded_gaussian')
# pre_head_cfg, v08.24
mix_head=dict(type='ContrastiveHead', temperature=0.1)  # SimCLR infoNCE
# pre_neck_cfg, v08.24
pre_neck=dict(
    type='LinearNeck', in_channels=256, out_channels=128, with_avg_pool=True)

# model settings
model = dict(
    type='MOCO_AutoMix_V0824',  # 08.24 update
    pretrained=None,
    alpha=2,
    queue_len=16384,
    feat_dim=128,
    momentum=0.999,
    mask_layer=2,
    mask_loss=0.1,  # using loss
    mask_adjust=0.,
    pre_one_loss=-1,  # v08.24 pre loss
    pre_mix_loss=-1,  # v08.24 pre loss
    pre_loss_neck=pre_neck,  # v08.24
    lam_margin=0.05,
    binary_cls=False,  # binary cls for mixblock
    debug=False,
    backbone=dict(
        type='ResNet',
        depth=18,
        in_channels=3,
        out_indices=[3, 4],  # 0: conv-1, x: stage-x
        norm_cfg=dict(type='BN')),
    neck=dict(
        type='NonLinearNeckV1',
        in_channels=512,
        hid_channels=512,
        out_channels=128,
        with_avg_pool=True),
    head=dict(type='ContrastiveHead', temperature=0.2),  # MoCo.V2 infoNCE
    mix_block = dict(  # V2, update v08.24
        type='PixelMixBlock_V2_v0824',
        in_channels=256, reduction=2, use_scale=True, double_norm=False,
        attention_mode='embedded_gaussian', unsampling_mode='bilinear',
        pre_conv_cfg=conv3x3,  # v08.23
        pre_attn_cfg=embedded,  # v08.23
        pre_head_cfg=mix_head,  # v08.24, SimCLR
        lam_concat=False,
        lam_mul=True, lam_residual=True, lam_mul_k=1,  # lam: mult + k=1
        x_qk_concat=True, x_v_concat=False,  # x concat: q,k
        mask_loss_mode="Variance", mask_loss_margin=0.1,  # var loss
        mask_mode="none_v_",
        frozen=False),
)
# dataset settings
data_source_cfg = dict(
    type='ImageNet',
    memcached=False,
    mclient_path='/mnt/lustre/share/memcached_client')
# STL-10
data_train_list = 'data/stl10/meta/train_10w_unlabeled.txt'
data_train_root = 'data/stl10/train/'

dataset_type = 'ContrastiveDataset'
img_norm_cfg = dict(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
train_pipeline = [
    dict(type='RandomResizedCrop', size=96, scale=(0.2, 1.)),
    dict(type='RandomAppliedTrans',
        transforms=[dict(
            type='ColorJitter',
                brightness=0.4, contrast=0.4, saturation=0.4, hue=0.1)
        ],
        p=0.8),
    dict(type='RandomGrayscale', p=0.2),
    dict(type='RandomAppliedTrans',
        transforms=[dict(
            type='GaussianBlur',
                sigma_min=0.1, sigma_max=2.0)
        ],
        p=0.5),
    dict(type='RandomHorizontalFlip'),
]
# prefetch
prefetch = True
if not prefetch:
    train_pipeline.extend([dict(type='ToTensor'), dict(type='Normalize', **img_norm_cfg)])

data = dict(
    imgs_per_gpu=256,  # total 256 * 1 = 256
    workers_per_gpu=8,
    drop_last=True,
    train=dict(
        type=dataset_type,
        data_source=dict(
            list_file=data_train_list, root=data_train_root,
            **data_source_cfg),
        pipeline=train_pipeline,
        prefetch=prefetch,
    ))

# additional hooks
custom_hooks = [
    dict(type='CustomCosineAnnealingHook',
        attr_name="mask_loss", attr_base=0.1, by_epoch=False,  # by iter
        min_attr=0,
    ),
    dict(type='SAVEHook',
        iter_per_epoch=390,
        save_interval=3900,  # 10 ep
    )
]

# optimizer
optimizer = dict(type='SGD', lr=0.03, weight_decay=0.0001, momentum=0.9,
                paramwise_options={
                    'mix_block': dict(lr=0.0005, momentum=0.9)},)  # required parawise_option
# optimizer args
optimizer_config = dict(
    update_interval=1, use_fp16 = False,  grad_clip=None,
    # cancel_grad=dict(mix_block=780),  # 2 ep
)
# learning policy
lr_config = dict(policy='CosineAnnealing', min_lr=0.)
checkpoint_config = dict(interval=400)

# additional scheduler, v07.14
addtional_scheduler = dict(
    # policy='CosineAnnealing', min_lr=0.01,
    policy='Cyclic', target_ratio=(100, 1), cyclic_times=2, step_ratio_up=0.4,  # good
    warmup='linear',
    warmup_iters=10,  # 10 ep
    warmup_ratio=0.00001,
    warmup_by_epoch=True,  # by iter
    paramwise_options=['mix_block'],
)

# runtime settings
total_epochs = 400
