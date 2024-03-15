_base_ = '../../../../base.py'
# model settings
model = dict(
    type='AutoMixup',
    pretrained=None,
    alpha=2.0,
    mask_layer=2,
    momentum=0.999,
    mask_loss=0.,
    save=True,  # save gradCAM
    backbone_q=dict(
        type='resnet_mixup',
        depth=34,
        mask_layer=2,
        num_stages=4,
        frozen_stages=-1,
        out_indices=(3,),
        style='pytorch'
    ),
    backbone_k=dict(
        type='resnet_mixup',
        depth=34,
        mask_layer=2,
        num_stages=4,
        frozen_stages=4,
        out_indices=(3,),
        style='pytorch',
    ),
    mix_block = dict(  # v06.09 automix
        type='PixelMixBlock_v0609', in_channels=256, reduction=2, use_scale=True,
        mode='embedded_gaussian',
        lam_mult=True,  # lam: mult lam to pairwise weight
        loss_mask="none", loss_margin=0,  # none loss
        frozen=False),
    head_one_q=dict(
        type='ClsHead', with_avg_pool=True, in_channels=512, num_classes=1000),
    head_mix_q=dict(
        type='ClsMixupHead', with_avg_pool=True, in_channels=512, num_classes=1000),
    head_one_k=dict(
        type='ClsHead', with_avg_pool=True, frozen=True, in_channels=512, num_classes=1000),
    head_mix_k=dict(
        type='ClsMixupHead', with_avg_pool=True, frozen=True, in_channels=512, num_classes=1000),
    )

# dataset settings
data_source_cfg = dict(
    type='ImageNet',
    memcached=False,
    mclient_path='/mnt/lustre/share/memcached_client')
# ImageNet dataset
data_root="/data/public_datasets/ILSVRC2012/"
data_train_list = 'data/meta/imagenet/train_labeled_full.txt'
data_train_root = data_root + 'train'
data_test_list = 'data/meta/imagenet/val_labeled.txt'
data_test_root = "/data/liuzicheng/ImageNet/val/"

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
    imgs_per_gpu=64,  # 64 x 4gpus = 256
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
        interval=2,
        imgs_per_gpu=100,
        workers_per_gpu=4,
        eval_param=dict(topk=(1, 5))),
    dict(type='SAVEHook',
        save_interval=50040,  # 5004 x 10ep
        iter_per_epoch=5004,
    ),
    dict(type='CosineScheduleHook',
        end_momentum=0.999999,
        adjust_scope=[0.1, 1.0],
        warming_up="constant",
        interval=1)
]
# optimizer
optimizer = dict(type='SGD', lr=0.1, momentum=0.9, weight_decay=0.0001)
optimizer_config = dict(grad_clip=None)

# learning policy
lr_config = dict(policy='CosineAnnealing', min_lr=0.)
checkpoint_config = dict(interval=25)

# runtime settings
total_epochs = 300
