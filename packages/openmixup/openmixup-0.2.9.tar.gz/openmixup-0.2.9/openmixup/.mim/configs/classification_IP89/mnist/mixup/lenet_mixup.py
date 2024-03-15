_base_ = '../../../base.py'
# model settings
model = dict(
    type='MixUpClassification',
    alpha=1.0,
    mix_mode="MixUp",
    backbone=dict(  # mmclassification
        type='LeNet5',
        activation="LeakyReLU",
        mlp_neck=None,
        cls_neck=True,
    ),
    head=dict(
        type='ClsMixupHead', with_avg_pool=False, in_channels=84, num_classes=10))
# dataset settings
data_source_cfg = dict(type='Mnist', root='./data/')
dataset_type = 'ClassificationDataset'
img_norm_cfg = dict(mean=[0.], std=[1.])
train_pipeline = [
    dict(type='Resize', size=32),  # no augmentation
    # dict(type='RandomResizedCrop', size=32, scale=[0.5, 1.0]),  # [OK]
    dict(type='RandomHorizontalFlip'),
]
test_pipeline = [
    dict(type='Resize', size=32),
]
# prefetch can't be used for mnist
train_pipeline.extend([dict(type='ToTensor'), dict(type='Normalize', **img_norm_cfg)])
test_pipeline.extend([dict(type='ToTensor'), dict(type='Normalize', **img_norm_cfg)])

data = dict(
    imgs_per_gpu=100,
    workers_per_gpu=4,
    train=dict(
        type=dataset_type,
        data_source=dict(split='train', **data_source_cfg),
        pipeline=train_pipeline,
    ),
    val=dict(
        type=dataset_type,
        data_source=dict(split='test', **data_source_cfg),
        pipeline=test_pipeline,
    ))
# additional hooks
custom_hooks = [
    dict(
        type='ValidateHook',
        dataset=data['val'],
        initial=False,
        interval=2,
        imgs_per_gpu=128,
        workers_per_gpu=2,
        eval_param=dict(topk=(1, 5)))
]
# optimizer
optimizer = dict(type='SGD', lr=0.1, momentum=0.9, weight_decay=0.0005)
optimizer_config = dict(grad_clip=None)

checkpoint_config = dict(interval=100)

# learning policy
lr_config = dict(policy='CosineAnnealing', min_lr=0.)
# runtime settings
total_epochs = 100
