_base_ = '../../../../../../base.py'
# pre_conv_cfg or value_neck_cfg
conv1x1=dict(
    type="ConvNeck",
    in_channels=1024, hid_channels=512, out_channels=1,  # MixBlock v
    num_layers=2, kernel_size=1,
    with_last_bn=False, norm_cfg=dict(type='BN'),
    with_last_dropout=0.1, with_avg_pool=False, with_residual=False)  # drop

# model settings
model = dict(
    type='AutoMixup_V2',
    pretrained='work_dirs/my_pretrains/official/resnet50_pytorch.pth',
    alpha=2.0,
    momentum=0.999,
    mask_layer=2,
    mask_loss=0.1,  # using loss
    mask_adjust=0,
    mask_input_size=[448, 384, 320, 256],  # v01.18, 448=7x2x32, using 7x2, 6x2, 5x2, 4x2
    pre_one_loss=-1,  # v08.24 pre loss
    pre_mix_loss=-1,  # v08.24 pre loss
    lam_margin=0.08,
    HEM_lam_thr=0.,  # v01.18
    mix_shuffle_no_repeat=True,  # for fine-grained
    mask_up_override='bilinear',
    debug=False,
    backbone=dict(
        type='ResNet_mmcls',
        depth=50,
        num_stages=4,
        out_indices=(2,3,),
        style='pytorch'),
    mix_block = dict(  # V2
        type='PixelMixBlock',
        in_channels=1024, reduction=2, use_scale=True, double_norm=False,
        attention_mode='embedded_gaussian', unsampling_mode='bilinear',
        pre_norm_cfg=None,  # v08.27
        pre_conv_cfg=None,  # v08.23
        pre_attn_cfg=None,  # v08.23
        pre_neck_cfg=None,  # v08.24, SimCLR neck
        pre_head_cfg=None,  # v08.24, SimCLR head
        lam_concat=False, lam_concat_v=False,
        lam_mul=True, lam_residual=True, lam_mul_k=-1,  # lam: mult + k=-1
        value_neck_cfg=conv1x1,  # v08.29
        x_qk_concat=True, x_v_concat=False,  # x concat: q,k
        mask_loss_mode="L1+Variance", mask_loss_margin=0.1,  # L1 + var loss
        mask_mode="none_v_",
        frozen=False),
    head_one=dict(
        type='ClsHead', with_avg_pool=True, in_channels=2048, num_classes=100),
    head_mix=dict(  # backbone mixup
        type='ClsMixupHead',  # mixup soft CE + decouple
        loss=dict(type='CrossEntropyLoss', loss_weight=1.0,
            use_soft=True, use_sigmoid=False, use_mix_decouple=False,  # try soft CE decouple
        ),
        with_avg_pool=True, multi_label=True, two_hot=False, two_hot_scale=1,  # no two-hot
        lam_scale_mode='pow', lam_thr=1, lam_idx=1,  # lam rescale, default 'pow'
        eta_weight=dict(eta=1, mode="both", thr=0.5),  # eta for decouple mixup
        in_channels=2048, num_classes=100),
    head_mix_k=dict(  # mixblock
        type='ClsMixupHead',  # mixup, soft CE
        loss=dict(type='CrossEntropyLoss', loss_weight=1.0, use_soft=False, use_sigmoid=False),
        with_avg_pool=True, in_channels=2048, num_classes=100),
    head_weights=dict(  # 07.25
        head_mix_q=1, head_one_q=1, head_mix_k=1, head_one_k=1),
)

# dataset settings
data_source_cfg = dict(
    type='ImageNet',
    memcached=False,
    mclient_path='/mnt/lustre/share/memcached_client')
# Aircrafts
aircrafts_base = "data/FGVC_Aircraft/fgvc-aircraft-2013b/data/"
data_train_list = aircrafts_base + 'classification_meta_0/train_labeled.txt'  # labeled train
data_train_root = aircrafts_base
data_test_list = aircrafts_base + 'classification_meta_0/test_labeled.txt'  # labeled test
data_test_root = aircrafts_base

dataset_type = 'ClassificationDataset'
img_norm_cfg = dict(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])  # imagenet (used in prefetch)
train_pipeline = [
    dict(type='Resize', size=512),
    dict(type='RandomResizedCrop', size=448, scale=[0.5, 1.0]),
    dict(type='RandomHorizontalFlip'),
]
test_pipeline = [
    dict(type='Resize', size=512),
    dict(type='CenterCrop', size=448),
]

# prefetch
prefetch = True
if not prefetch:
    train_pipeline.extend([dict(type='ToTensor'), dict(type='Normalize', **img_norm_cfg)])
test_pipeline.extend([dict(type='ToTensor'), dict(type='Normalize', **img_norm_cfg)])

data = dict(
    imgs_per_gpu=8,  # try small bs in fine-grained
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
        imgs_per_gpu=16,
        workers_per_gpu=4,
        eval_param=dict(topk=(1, 5))),
    dict(type='SAVEHook',
        save_interval=4160,  # 10 ep
        iter_per_epoch=416,  # 6667 / 16
    ),
    dict(type='CustomCosineAnnealingHook',
        attr_name="mask_loss", attr_base=0.1, by_epoch=False,  # by iter
        min_attr=0.,
    ),
    dict(type='CosineScheduleHook',
        end_momentum=0.99999,
        adjust_scope=[0.1, 1.0],
        warming_up="constant",
        interval=1)
]
# optimizer
optimizer = dict(type='SGD', lr=0.005, momentum=0.9, weight_decay=0.0005,
                paramwise_options={
                    'head': dict(lr=0.01, momentum=0.9),
                    'mix_block': dict(lr=0.01, momentum=0.9)},)  # required parawise_option
# optimizer args
optimizer_config = dict(update_interval=1, use_fp16=False, grad_clip=None)

# learning policy
lr_config = dict(policy='CosineAnnealing', min_lr=0.0005)
checkpoint_config = dict(interval=400)

# additional scheduler
addtional_scheduler = dict(
    policy='CosineAnnealing', min_lr=0.0005,
    paramwise_options=['mix_block'],
)

# runtime settings
total_epochs = 100
