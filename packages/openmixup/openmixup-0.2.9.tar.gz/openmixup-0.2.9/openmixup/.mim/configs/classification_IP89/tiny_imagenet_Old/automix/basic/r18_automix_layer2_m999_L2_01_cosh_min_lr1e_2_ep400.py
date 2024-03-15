_base_ = '../../../../base.py'
# runtime settings
model = dict(
    type='AutoMixup',
    pretrained=None,
    alpha=2.0,
    mask_layer=2,
    grad_mode=None,
    momentum=0.999,
    mask_loss=0.1,  # using loss!
    save=True,  # save gradCAM
    backbone_q=dict(
        type='resnet_mixup_CIFAR',
        depth=18,
        mask_layer=2,
        num_stages=4,
        frozen_stages=-1,
        out_indices=(3,),
        style='pytorch'
    ),
    backbone_k=dict(
        type='resnet_mixup_CIFAR',
        depth=18,
        mask_layer=2,
        num_stages=4,
        frozen_stages=4,
        out_indices=(3,),
        style='pytorch',
    ),
    mix_block = dict(  # automix, v05.12
        type='PixelMixBlock', in_channels=256, reduction=2, use_scale=True,
        mode='embedded_gaussian',
        lam_concat_theta=False, lam_concat_g=False,  # lambda concat: none
        post_conv=False,
        loss_mask="L2", loss_margin=0.1,  # loss: L2, 0.1
        frozen=False),
    head_one_q=dict(
        type='ClsHead', with_avg_pool=True, in_channels=512, num_classes=200),
    head_mix_q=dict(
        type='ClsMixupHead', with_avg_pool=True, in_channels=512, num_classes=200),
    head_one_k=dict(
        type='ClsHead', with_avg_pool=True, frozen=True, in_channels=512, num_classes=200),
    head_mix_k=dict(
        type='ClsMixupHead', with_avg_pool=True, frozen=True, in_channels=512, num_classes=200),
    )

# dataset settings
data_source_cfg = dict(
    type='ImageNet',
    memcached=False,
    mclient_path='/mnt/lustre/share/memcached_client')
# tiny imagenet
data_train_list = 'data/TinyImagenet200/meta/train_labeled.txt'  # train 10w
data_train_root = 'data/TinyImagenet200/train/'
data_test_list = 'data/TinyImagenet200/meta/val_labeled.txt'  # val 1w
data_test_root = 'data/TinyImagenet200/val_raw/'

dataset_type = 'ClassificationDataset'
img_norm_cfg = dict(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
train_pipeline = [
    dict(type='RandomResizedCrop', size=64),
    dict(type='RandomHorizontalFlip'),
]
test_pipeline = [
    dict(type='Resize', size=64),
]
# prefetch
prefetch = True
if not prefetch:
    train_pipeline.extend([dict(type='ToTensor'), dict(type='Normalize', **img_norm_cfg)])
test_pipeline.extend([dict(type='ToTensor'), dict(type='Normalize', **img_norm_cfg)])

data = dict(
    imgs_per_gpu=100,
    workers_per_gpu=4,
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
            list_file=data_test_list, root=data_test_root,
            **data_source_cfg),
        pipeline=test_pipeline,
        prefetch=False,
    ),
)

# additional hooks
custom_hooks = [
    dict(type='ValidateHook',
        dataset=data['val'],
        initial=True,
        interval=2,
        imgs_per_gpu=100,
        workers_per_gpu=4,
        eval_param=dict(topk=(1, 5))),
    dict(type='CosineScheduleHook',
        end_momentum=0.99999,
        adjust_scope=[0.1, 1.0],
        warming_up="constant",
        interval=1),
    dict(type='SAVEHook',
        save_interval=10000,  # 10 ep
        iter_per_epoch=1000,
    )
]

# optimizer
optimizer = dict(type='SGD', lr=0.2, momentum=0.9, weight_decay=0.0001)
optimizer_config = dict(grad_clip=None)

# learning policy
lr_config = dict(policy='CosineAnnealing', min_lr=0.01)  # min_lr=1e-2
checkpoint_config = dict(interval=100)

# runtime settings
total_epochs = 400
