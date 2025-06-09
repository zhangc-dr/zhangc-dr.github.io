import numpy as np
import pandas as pd
import datashader as ds
import datashader.transfer_functions as tf
from datashader.transfer_functions import dynspread, set_background
from datashader.colors import viridis
import os
import glob

class NOMARegion:
    def __init__(self, Nt=3, user_loc=[-10, 10], betas=[1, 0.5], sigma_2=0.05):
        self.Nt = Nt
        self.thetas = np.array(user_loc) / 180 * np.pi
        self.betas = np.array(betas)
        self.sigma_2 = sigma_2
        self.h1 = self.betas[0] * np.exp(1j * np.pi * np.sin(self.thetas[0]) * np.arange(Nt))
        self.h2 = self.betas[1] * np.exp(1j * np.pi * np.sin(self.thetas[1]) * np.arange(Nt))
        self.v_list = self._generate_unit_vectors(Nt, num=100000)
        self.alpha = np.linspace(0, 1.0, 200)

    def _generate_unit_vectors(self, Nt, num):
        vecs = []
        for _ in range(num):
            real = np.random.randn(Nt)
            imag = np.random.randn(Nt)
            v = real + 1j * imag
            v = v / np.linalg.norm(v)
            vecs.append(v)
        return vecs

    def is_pareto_efficient_2d(self, points):
        points = np.array(points)
        sorted_idx = np.lexsort((-points[:, 1], points[:, 0]))[::-1]
        sorted_points = points[sorted_idx]
        pareto = []
        max_r2 = -np.inf
        for r1, r2 in sorted_points:
            if r2 > max_r2:
                pareto.append((r1, r2))
                max_r2 = r2
        return pareto

    def compute_render(self, batch_size=2000, save_dir='data', img_file='img/noma.png'):
        os.makedirs(save_dir, exist_ok=True)

        total_v = len(self.v_list)

        for start in range(0, total_v, batch_size):
            end = min(start + batch_size, total_v)
            batch_v = self.v_list[start:end]

            filepath = os.path.join(save_dir, f'noma_batch_{start}.csv')
            if os.path.exists(filepath):
                os.remove(filepath)

            batch_points = []
            for v in batch_v:
                h1v = np.abs(np.vdot(v, self.h1)) ** 2
                h2v = np.abs(np.vdot(v, self.h2)) ** 2

                for a in self.alpha:
                    if h1v > h2v:
                        R1 = np.log2(1 + a * h1v / self.sigma_2)
                        R2 = np.log2(1 + (1 - a) * h2v / (a * h2v + self.sigma_2))
                    else:
                        R1 = np.log2(1 + a * h1v / ((1 - a) * h1v + self.sigma_2))
                        R2 = np.log2(1 + (1 - a) * h2v / self.sigma_2)

                    batch_points.append((R1, R2))


            pareto_points = self.is_pareto_efficient_2d(batch_points)
            df = pd.DataFrame(pareto_points, columns=['R1', 'R2'])

            df.to_csv(filepath, mode='a', header=not os.path.exists(filepath), index=False)
            print(f"已追加 {len(df)} 个点到文件: {filepath}")

        print("全部批次数据处理完毕，开始后续渲染等操作。")

        # 渲染所有批次数据
        files = glob.glob(os.path.join(save_dir, 'noma_batch_*.csv'))
        all_points = [pd.read_csv(f) for f in files]
        all_df = pd.concat(all_points, ignore_index=True)

        canvas = ds.Canvas(plot_width=400, plot_height=400)
        agg = canvas.points(all_df, 'R1', 'R2')

        img = tf.shade(agg, cmap=viridis, how='eq_hist')
        img = dynspread(img, threshold=0.5, max_px=4)
        img = set_background(img, "white")

        os.makedirs(os.path.dirname(img_file), exist_ok=True)
        img.to_pil().save(img_file)
        print(f"渲染图片已保存到 {img_file}")

        # 删除所有批次 CSV 文件
        for f in files:
            try:
                os.remove(f)
            except Exception as e:
                print(f"删除文件 {f} 时出错: {e}")
        print("已删除所有批次 CSV 文件。")
