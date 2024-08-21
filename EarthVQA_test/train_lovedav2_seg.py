import ever as er
import torch
import numpy as np
import os
from tqdm import tqdm
import random
import json
from data.lovedav2 import COLOR_MAP
import torch.distributed as dist


er.registry.register_all()

torch.cuda.empty_cache()


# Set the backend and initialize the process group
os.environ['RANK'] = '0'
os.environ['WORLD_SIZE'] = '1'
os.environ['MASTER_ADDR'] = 'localhost'
os.environ['MASTER_PORT'] = '29500'
dist.init_process_group(backend='nccl', init_method='env://')


# Set the device to GPU 0 if available, otherwise fall back to CPU
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
# device = torch.device('cpu')


def evaluate_cls_fn(self, test_dataloader, config=None):
    self.model.to(device)
    self.model.eval()

    # Initialize metric and other components
    seg_metric = er.metric.PixelMetric(2, logdir=self._model_dir, logger=self.logger)
    vis_dir = os.path.join(self._model_dir, 'vis-{}'.format(self.checkpoint.global_step))
    palette = np.array(list(COLOR_MAP.values())).reshape(-1).tolist()

    with torch.no_grad():
        for idx, (img, ret) in enumerate(tqdm(test_dataloader)):
            img = img.to(device)
            pred_seg = self.model(img, ret)
            torch.cuda.empty_cache()

            # If model returns a tuple, get the second item
            if isinstance(pred_seg, tuple):
                pred_seg = pred_seg[1]
                
            seg_gt = ret['mask'].cpu().numpy()

            # Check for valid indices
            if not np.all((seg_gt >= 0) & (seg_gt < 2)):
                raise ValueError("Invalid target values found.")

            pred_seg = pred_seg.argmax(dim=1).cpu().numpy()
            valid_inds = seg_gt != -1
            seg_metric.forward(seg_gt[valid_inds], pred_seg[valid_inds])
            
            print(f"Step: {idx + 1}, Evaluation ongoing...")  # Add step logging


    seg_metric.summary_all()
    torch.cuda.empty_cache()


def register_evaluate_fn(launcher):
    launcher.override_evaluate(evaluate_cls_fn)

def seed_torch(seed=2333):
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)  # This is safe even if you're using a single GPU.
    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.enabled = False


if __name__ == '__main__':
    seed_torch(42)
    # trainer = er.trainer.get_trainer('th_ddp')()
    trainer = er.trainer.get_trainer('base')()
    trainer.run(after_construct_launcher_callbacks=[register_evaluate_fn])
    
