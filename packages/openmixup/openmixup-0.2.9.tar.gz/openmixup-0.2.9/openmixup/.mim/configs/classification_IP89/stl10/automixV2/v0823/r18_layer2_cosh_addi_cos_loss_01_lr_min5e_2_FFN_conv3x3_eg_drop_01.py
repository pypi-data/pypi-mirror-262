_base_ = '../../../../base.py'
# pre_conv_cfg, v08.23
conv3x3=dict(
    in_channels=256, hid_channels=128, out_channels=256,
    num_layers=2, kernel_size=3,
    with_bias=True, with_last_dropout=0.1, with_residual=True)
# pre_attn_cfg, v08.23
gaussian=dict(
    in_channels=256, mode='gaussian')
embedded=dict(
    in_channels=256, mode='embedded_gaussian')

# model settings
model = dict(
    type='AutoMixup_V1plus_V0726',
    pretrained=None,
    alpha=2.0,
    mask_layer=2,
    momentum=0.999,
    mask_loss=0.1,  # using loss
    lam_margin=0.05,  # lam margin to mixup
    save=True,  # save gradCAM
    backbone=dict(
        type='ResNet_mmcls',
        depth=18,
        num_stages=4,
        out_indices=(2,3),
        style='pytorch'),
    mix_block = dict(  # v0712, update 08.23
        type='PixelMixBlock_V1plus_v0712',
        in_channels=256, reduction=2, use_scale=True, double_norm=False,
        attention_mode='embedded_gaussian', unsampling_mode='bilinear',
        pre_conv_cfg=conv3x3,  # v08.23
        pre_attn_cfg=embedded,  # v08.23
        lam_concat=False,
        lam_mul=True, lam_residual=True, lam_mul_k=1,  # lam: mult + k=1
        x_qk_concat=True, x_v_concat=False,  # x concat: q,k
        loss_mode="Variance", loss_margin=0.1,  # var loss
        mask_mode="none_v_",
        frozen=False),
    head_one=dict(
        type='ClsHead', with_avg_pool=True, in_channels=512, num_classes=10),
    head_mix=dict(
        type='ClsMixupHead', with_avg_pool=True, in_channels=512, num_classes=10),
    head_weights=dict(  # 07.25
        head_mix_q=1, head_one_q=1, head_mix_k=1, head_one_k=1),
)

# dataset settings
data_source_cfg = dict(
    type='ImageNet',
    memcached=False,
    mclient_path='/mnt/lustre/share/memcached_client')
# STL-10 dataset
data_train_list = 'data/stl10/meta/train_5k_labeled.txt'  # stl10 labeled 5k train
data_train_root = 'data/stl10/train/'  # using labeled train set
data_test_list = 'data/stl10/meta/test_8k_labeled.txt'  # stl10 labeled 8k test
data_test_root = 'data/stl10/test/'  # using labeled test set

dataset_type = 'ClassificationDataset'
img_norm_cfg = dict(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
train_pipeline = [
    dict(type='RandomResizedCrop', size=96, scale=[0.2, 1.0]),
    dict(type='RandomHorizontalFlip'),
]
test_pipeline = [
    dict(type='Resize', size=96),
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
    drop_last=False,
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
        interval=2,
        imgs_per_gpu=100,
        workers_per_gpu=4,
        eval_param=dict(topk=(1, 5))),
    dict(type='SAVEHook',
        save_interval=1000,  # 50 x 20ep
        iter_per_epoch=50,
    ),
    dict(type='CustomCosineAnnealingHook',  # 0.1 to 0
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
optimizer = dict(type='SGD', lr=0.1, momentum=0.9, weight_decay=0.0001,
                paramwise_options={
                    'mix_block': dict(lr=0.1, momentum=0.9)},)  # required parawise_option
# optimizer args
optimizer_config = dict(
    update_interval=1, use_fp16 = False, grad_clip=None,
    # cancel_grad=dict(mix_block=500),  # 1 ep
)
# learning policy
lr_config = dict(policy='CosineAnnealing', min_lr=0.05)
checkpoint_config = dict(interval=400)

# additional scheduler
addtional_scheduler = dict(
    policy='CosineAnnealing', min_lr=0.,
    warmup='linear',
    warmup_iters=1,  # 1 ep
    warmup_ratio=0.001,
    warmup_by_epoch=True,
    paramwise_options=['mix_block'],
)

# runtime settings
total_epochs = 400
