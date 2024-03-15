_base_ = 'r50_4xb256_accu2_cos_lr1_6_fp16_ep1000.py'

# dataset settings for SSL metrics
val_data_source_cfg = dict(type='ImageNet')
# ImageNet dataset for SSL metrics
val_data_train_list = 'data/meta/STL10/train_5k_labeled.txt'
val_data_train_root = 'data/stl10/train/'
val_data_test_list = 'data/meta/STL10/test_8k_labeled.txt'
val_data_test_root = 'data/stl10/test/'

val_test_pipeline = [
    dict(type='Resize', size=96),
    dict(type='ToTensor'),
    dict(type='Normalize', mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
]
val_data = dict(
    train=dict(
        type='ClassificationDataset',
        data_source=dict(
            list_file=val_data_train_list, root=val_data_train_root,
            **val_data_source_cfg),
        pipeline=val_test_pipeline,
        prefetch=False,
    ),
    val=dict(
        type='ClassificationDataset',
        data_source=dict(
            list_file=val_data_test_list, root=val_data_test_root,
            **val_data_source_cfg),
        pipeline=val_test_pipeline,
        prefetch=False,
    ))

# interval for accumulate gradient
update_interval = 2

# additional hooks
custom_hooks = [
    # dict(type='SwitchEMAHook',  # EMA_W = (1 - m) * EMA_W + m * W
    #     momentum=0.999,
    #     warmup='linear',
    #     warmup_iters=5 * 25, warmup_ratio=0.9,  # warmup 5 ep
    #     update_interval=update_interval,
    #     switch_params=True,
    #     switch_by_iter=True,
    #     switch_start=0,
    #     switch_interval=update_interval * 1000 * 25 - 1,  # the last iteration
    # ),
    dict(type='SSLMetricHook',
        val_dataset=val_data['val'],
        train_dataset=val_data['train'],  # remove it if metric_mode is None
        forward_mode='vis',
        metric_mode='knn',  # linear metric (take a bit long time on imagenet)
        metric_args=dict(knn=20, temperature=0.07, chunk_size=256),
        # visual_mode='umap',  # 'tsne' or 'umap'
        visual_mode=None,
        visual_args=dict(n_epochs=300, plot_backend='seaborn'),
        save_val=False,  # whether to save results
        initial=False,
        interval=25,
        imgs_per_gpu=256,
        workers_per_gpu=4,
        eval_param=dict(topk=(1, 5))),
]
