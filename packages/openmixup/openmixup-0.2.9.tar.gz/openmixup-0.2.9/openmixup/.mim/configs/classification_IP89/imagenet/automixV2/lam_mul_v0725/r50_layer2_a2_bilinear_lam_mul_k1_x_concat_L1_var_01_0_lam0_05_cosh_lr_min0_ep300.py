_base_ = '../../../../base.py'
# model settings
model = dict(
    type='AutoMixup_V1plus',  # update v07.25, 08.04
    pretrained=None,
    alpha=2.0,
    momentum=0.999,  # ori
    mask_layer=2,
    mask_loss=0.1,
    mask_adjust=0,  # v07.25
    lam_margin=0.05,
    save=True,  # save gradCAM
    backbone=dict(
        type='ResNet_mmcls',
        depth=50,
        num_stages=4,
        out_indices=(2,3),
        style='pytorch'),
    mix_block = dict(  # v0712
        type='PixelMixBlock_V1plus_v0712',
        in_channels=1024, reduction=2, use_scale=True, double_norm=False,
        attention_mode='embedded_gaussian', unsampling_mode='bilinear',
        lam_concat=False,
        lam_mul=True, lam_residual=True, lam_mul_k=1, # lam: mult + k=1
        x_qk_concat=True, x_v_concat=False,  # x concat: q,k
        loss_mode="L1+Variance", loss_margin=0.1,  # loss var + L1
        mask_mode="none_v_",
        frozen=False),
    head_one=dict(
        type='ClsHead', with_avg_pool=True, in_channels=2048, num_classes=1000),
    head_mix=dict(
        type='ClsMixupHead', with_avg_pool=True, in_channels=2048, num_classes=1000),
    head_indices=("head_mix_q", "head_one_q", "head_mix_k", "head_one_k"),
)

# dataset settings
data_source_cfg = dict(
    type='ImageNet',
    memcached=False,
    mclient_path='/mnt/lustre/share/memcached_client')
# ImageNet dataset
data_root="data/ImageNet/"
data_train_list = 'data/meta/imagenet/train_labeled_full.txt'
data_train_root = data_root + 'train'
data_test_list = 'data/meta/imagenet/val_labeled.txt'
data_test_root = data_root + "val/"

dataset_type = 'ClassificationDataset'
img_norm_cfg = dict(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
train_pipeline = [
    dict(type='RandomResizedCrop', size=224),
    dict(type='RandomHorizontalFlip'),
]
test_pipeline = [
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
    imgs_per_gpu=32,  # 32 x 8gpus = 256
    workers_per_gpu=4,
    drop_last=True,
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
        save_interval=25020,  # 5004 x 5ep
        iter_per_epoch=5004,
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
optimizer = dict(type='SGD', lr=0.1, momentum=0.9, weight_decay=0.0001)
optimizer_config = dict(grad_clip=None)

# learning policy
lr_config = dict(policy='CosineAnnealing', min_lr=0.)
checkpoint_config = dict(interval=100)

# runtime settings
total_epochs = 300
