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
        type='resnext_mixup_CIFAR',
        depth=50,
        mask_layer=2,
        num_stages=4,
        frozen_stages=-1,
        out_indices=(3,),
        style='pytorch'
    ),
    backbone_k=dict(
        type='resnext_mixup_CIFAR',
        depth=50,
        mask_layer=2,
        num_stages=4,
        frozen_stages=4,
        out_indices=(3,),
        style='pytorch',
    ),
    mix_block = dict(  # automix, v05.12
        type='PixelMixBlock', in_channels=1024, reduction=2, use_scale=True,
        mode='embedded_gaussian',
        lam_concat_theta=False, lam_concat_g=False,  # lambda concat: none
        post_conv=False,
        loss_mask="L2", loss_margin=0.1,  # L2 loss
        frozen=False),
    head_one_q=dict(
        type='ClsHead', with_avg_pool=True, in_channels=2048, num_classes=100),
    head_mix_q=dict(
        type='ClsMixupHead', with_avg_pool=True, in_channels=2048, num_classes=100),
    head_one_k=dict(
        type='ClsHead', with_avg_pool=True, frozen=True, in_channels=2048, num_classes=100),
    head_mix_k=dict(
        type='ClsMixupHead', with_avg_pool=True, frozen=True, in_channels=2048, num_classes=100),
    )

# dataset settings
data_source_cfg = dict(type='Cifar100', root='data/cifar100/')
dataset_type = 'ClassificationDataset'
img_norm_cfg = dict(mean=[0.4914, 0.4822, 0.4465], std=[0.2023, 0.1994, 0.201])
train_pipeline = [
    dict(type='RandomCrop', size=32, padding=4, padding_mode="reflect"),  # tricks
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
    # imgs_per_gpu=100,
    imgs_per_gpu=50,  # 50 x 2 = 100
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
        interval=2,
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
        save_interval=10000,  # 20 ep
    )
]

# optimizer
optimizer = dict(type='SGD', lr=0.1, momentum=0.9, weight_decay=0.0001,)
                    # paramwise_options={'mix_block': dict(lr_mult=10)})  # ok
optimizer_config = dict(grad_clip=None)

# learning policy
lr_config = dict(policy='CosineAnnealing', min_lr=0.05)  # min_lr=5e-2
checkpoint_config = dict(interval=100)

# runtime settings
total_epochs = 400
