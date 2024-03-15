_base_ = '../../../../../base.py'
# model settings
num_classes = 500  # add clustering ImageNet
# pre_conv_cfg or value_neck_cfg
conv1x1=dict(
    type="ConvNeck",
    in_channels=256, hid_channels=128, out_channels=1,  # MixBlock v
    num_layers=2, kernel_size=1,
    with_last_bn=False, norm_cfg=dict(type='BN'),  # ori
    with_last_dropout=0.1, with_avg_pool=False, with_residual=False)  # no res

model = dict(
    type='MOCO_AutoMix_V2',  # 09.27 update
    pretrained=None,
    alpha=2,
    queue_len=65536,
    feat_dim=128,
    momentum=0.999,
    mask_layer=2,
    mask_adjust="auto",  # try
    mean_margin=0.05,  # v09.05, OK
    mask_smooth=5, # v09.13
    pre_one_loss=-1,  # v08.24 pre loss
    pre_mix_loss=-1,  # v08.24 pre loss
    lam_margin=0.10,
    main_mb_loss="CE",  # v09.27, main loss
    auxi_mb_loss="BCE",  # v09.27, ["BCE", "infoNCE"]
    feat_pos_extend="interpolation",  # 09.24, "interpolation", "expolation"
    mix_shuffle_no_repeat=True,  # v09.22, ok
    loss_weights=dict(
        decent_weight=["weight_mb_auxi", "weight_mb_mask"],
        accent_weight=[],
        weight_bb_mix=1, weight_bb_ssl=1, weight_mb_main=1, weight_mb_auxi=1,
        weight_mb_pre=1, weight_mb_mask=0.1),
    debug=True,
    backbone=dict(
        type='ResNet',
        depth=18,
        in_channels=3,
        out_indices=[3, 4],  # 0: conv-1, x: stage-x
        zero_init_residual=True,
        norm_cfg=dict(type='BN')),
    neck=dict(
        type='NonLinearNeckV1',
        in_channels=512,
        hid_channels=512,
        out_channels=128,
        with_avg_pool=True),
    head=dict(type='ContrastiveHead', temperature=0.2),
    clustering=dict(
        type="ODC",
        memory_bank=dict(
            type='ODCMemory',
            length=1281167,  # full imagenet
            feat_dim=128,
            momentum=1.,  # using momentum encoder for features
            num_classes=num_classes,
            min_cluster=800,  # 1280k / 500
            debug=False)
    ),
    head_clst=dict(  # for ODC, using neck feat
        type='ClsMixupHead', with_avg_pool=False, in_channels=128, num_classes=num_classes),
    mix_block = dict(  # V2, update v08.24
        type='PixelMixBlock_V2_v0824',
        in_channels=256, reduction=2, use_scale=True, double_norm=False,
        attention_mode='embedded_gaussian', unsampling_mode='bilinear',
        pre_norm_cfg=None,  # v08.27
        pre_conv_cfg=None,  # v08.23
        pre_attn_cfg=None,  # v08.23
        pre_neck_cfg=None,  # v08.24
        pre_head_cfg=None,  # v08.24
        lam_concat=False, lam_concat_v=False,  # V1
        lam_mul=True, lam_residual=True, lam_mul_k=1,  # V2 lam: mult + k=1
        value_neck_cfg=conv1x1,  # v08.29
        x_qk_concat=True, x_v_concat=False,  # V2 x concat: q,k
        mask_loss_mode="L2+Variance", mask_loss_margin=0.1,  # var loss
        mask_mode="none_v_",
        frozen=False),
)
# dataset settings
data_source_cfg = dict(
    type='ImageNet',
    memcached=False,
    mclient_path='/mnt/lustre/share/memcached_client')
# ImageNet dataset
data_root="data/ImageNet/"
data_train_list = 'data/meta/imagenet/train_full.txt'
data_train_root = data_root + 'train'

# dataset_type = 'ContrastiveDataset'
dataset_type = 'ClusterContrastiveDataset'

img_norm_cfg = dict(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
train_pipeline = [
    dict(type='RandomResizedCrop', size=224, scale=(0.2, 1.)),
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
extract_pipeline = [  # clustering
    dict(type='Resize', size=256),
    dict(type='CenterCrop', size=224),
    dict(type='ToTensor'),
    dict(type='Normalize', **img_norm_cfg),
]

# prefetch
prefetch = True
if not prefetch:
    train_pipeline.extend([dict(type='ToTensor'), dict(type='Normalize', **img_norm_cfg)])

data = dict(
    imgs_per_gpu=32,  # total 32 * 8 = 256
    workers_per_gpu=4,
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
    dict(type='DeepClusterAutoMixHook',
        extractor=dict(
            imgs_per_gpu=128,
            workers_per_gpu=8,
            dataset=dict(
                type="DeepClusterDataset",
                data_source=dict(
                    list_file=data_train_list,
                    root=data_train_root,
                    **data_source_cfg),
                pipeline=extract_pipeline)),
        clustering=dict(type='Kmeans', k=num_classes, pca_dim=-1),  # no pca
        unif_sampling=False,
        reweight=True,  # using loss reweight
        reweight_pow=0.5,
        init_memory=True,  # True for ODC
        init_params=False,  # for DeepCluster
        initial=True,  # call initially
        interval=999999),  # initial only
    dict(type='ODCHook',
        centroids_update_interval=250,  # 5004 iter per ep
        deal_with_small_clusters_interval=50,  # on IN
        evaluate_interval=500,  # on IN
        reweight=True,
        reweight_pow=0.5),
    dict(type='CustomCosineAnnealingHook',  # basic 'cos_annealing'
        attr_name="cos_annealing", attr_base=1, by_epoch=False,  # by iter
        min_attr=0,
    ),
    dict(type='SAVEHook',
        iter_per_epoch=5004,
        save_interval=25020,  # 5 ep
    ),
]

# optimizer
optimizer = dict(type='SGD', lr=0.03, weight_decay=0.0001, momentum=0.9,
                paramwise_options={
                    'head_clst': dict(lr=0.0050, momentum=0.,),    # clustering
                    'mix_block': dict(lr=0.0050, momentum=0.9)},)  # required parawise_option
# optimizer args
optimizer_config = dict(
    update_interval=1, use_fp16=False,)
# learning policy
lr_config = dict(policy='CosineAnnealing', min_lr=0.)
checkpoint_config = dict(interval=50)

# additional scheduler, v07.14
addtional_scheduler = dict(
    policy='Cyclic', target_ratio=(100, 1), cyclic_times=2, step_ratio_up=0.4,
    warmup='linear',
    warmup_iters=10,  # 10 ep
    warmup_ratio=1e-5,
    warmup_by_epoch=True,  # by iter
    # paramwise_options=['mix_block'],
    paramwise_options=['mix_block', 'head_clst'],
)

# runtime settings
total_epochs = 200
