_base_ = '../../../../base.py'
# pre_conv_cfg or value_neck_cfg
conv1x1=dict(
    type="ConvNeck",
    in_channels=256, hid_channels=128, out_channels=1,  # MixBlock v
    num_layers=2, kernel_size=1,
    with_last_bn=False, norm_cfg=dict(type='BN'),
    with_last_dropout=0.1, with_avg_pool=False, with_residual=False)  # drop

# model settings
model = dict(
    type='AutoMixup_V2',  # v08.24
    pretrained='work_dirs/my_pretrains/official/resnet18_pytorch.pth',
    pretrained_k='work_dirs/classification/imagenet/automixV2/v0824_1110_IP127/r18/' + \
        'r18_v0824_l2_a2_bili_val_drp0_mul_x_cat_L1_var_01_use_soft_CE_q_soft_k_ep100/epoch_100.pth',
    alpha=2.0,
    momentum=1,  # using pretrained mixblock
    mask_layer=2,
    mask_loss=0,  # using pretrained mixblock
    mask_adjust=0,
    pre_one_loss=-1,  # v08.24 pre loss
    pre_mix_loss=-1,  # v08.24 pre loss
    lam_margin=0.08,
    mix_shuffle_no_repeat=True,  # for fine-grained
    debug=False,
    backbone=dict(
        type='ResNet_mmcls',
        depth=18,
        num_stages=4,
        out_indices=(2,3),
        style='pytorch'),
    backbone_k=dict(  # pretrained k: R50
        type='ResNet_mmcls',
        depth=18,
        num_stages=4,
        out_indices=(2,),  # layer 2
        style='pytorch'),
    mix_block = dict(  # V2, using pretrained mixblock, R50
        type='PixelMixBlock_V2',
        in_channels=256, reduction=2, use_scale=True, double_norm=False,
        attention_mode='embedded_gaussian', unsampling_mode='bilinear',
        lam_concat=False, lam_concat_v=False,
        lam_mul=True, lam_residual=True, lam_mul_k=1,  # lam: mult + k=1
        value_neck_cfg=conv1x1,  # v08.29
        x_qk_concat=True, x_v_concat=False,  # x concat: q,k
        mask_loss_mode="L1+Variance", mask_loss_margin=0.1,  # L1 + var loss
        mask_mode="none_v_",
        frozen=True),  # frozen mixblock
    head_one=dict(
        type='ClsHead', with_avg_pool=True, in_channels=512, num_classes=200),
    head_mix=dict(
        type='ClsMixupHead', with_avg_pool=True, in_channels=512, num_classes=200),
    head_weights=dict(  # frozen mixblock losses
        head_mix_q=1, head_one_q=1, head_mix_k=0, head_one_k=0),
)

# dataset settings
data_source_cfg = dict(
    type='ImageNet',
    memcached=False,
    mclient_path='/mnt/lustre/share/memcached_client')
# CUB200
cub_base = "data/CUB200/"
data_train_list = cub_base + 'CUB_200/classification_meta_0/train_labeled.txt'  # labeled train
data_train_root = cub_base + 'CUB_200/images/'
data_test_list = cub_base + 'CUB_200/classification_meta_0/test_labeled.txt'  # labeled test
data_test_root = cub_base + 'CUB_200/images/'

dataset_type = 'ClassificationDataset'
img_norm_cfg = dict(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])  # imagenet (used in prefetch)
train_pipeline = [
    dict(type='Resize', size=256),
    dict(type='RandomResizedCrop', size=224, scale=[0.5, 1.0]),
    dict(type='RandomHorizontalFlip'),
]
test_pipeline = [
    dict(type='Resize', size=256),
    dict(type='CenterCrop', size=224),
]

# prefetch
prefetch = True
if not prefetch:
    train_pipeline.extend([dict(type='ToTensor'), dict(type='Normalize', **img_norm_cfg)])
test_pipeline.extend([dict(type='ToTensor'), dict(type='Normalize', **img_norm_cfg)])

data = dict(
    imgs_per_gpu=16,  # try small bs in fine-grained
    workers_per_gpu=4,
    drop_last=True,  # only in fine grained
    train=dict(
        type=dataset_type,
        data_source=dict(
            list_file=data_train_list, root=data_train_root,
            **data_source_cfg),
        pipeline=train_pipeline,
        prefetch=prefetch,
    ),
    val=dict(
        type=dataset_type,
        data_source=dict(
            list_file=data_test_list, root=data_test_root, **data_source_cfg),
        pipeline=test_pipeline,
        prefetch=False,
    ))

# additional hooks
custom_hooks = [
    dict(type='ValidateHook',
        dataset=data['val'],
        initial=False,
        interval=1,
        imgs_per_gpu=100,
        workers_per_gpu=4,
        eval_param=dict(topk=(1, 5))),
    dict(type='SAVEHook',
        save_interval=18700,  # 50 ep
        iter_per_epoch=374,
    ),
    # dict(type='CustomCosineAnnealingHook',
    #     attr_name="mask_loss", attr_base=0.1, by_epoch=False,  # by iter
    #     min_attr=0.,
    # ),
    # dict(type='CosineScheduleHook',
    #     end_momentum=0.99999,
    #     adjust_scope=[0.1, 1.0],
    #     warming_up="constant",
    #     interval=1)
]
# optimizer
optimizer = dict(type='SGD', lr=0.001, momentum=0.9, weight_decay=0.0005)
# optimizer args
optimizer_config = dict(update_interval=1, use_fp16=False, grad_clip=None)

# learning policy
lr_config = dict(policy='CosineAnnealing', min_lr=0.0005)
checkpoint_config = dict(interval=400)

# additional scheduler
# addtional_scheduler = dict(
#     policy='CosineAnnealing', min_lr=0.0005,
#     paramwise_options=['mix_block'],
# )

# runtime settings
total_epochs = 200
