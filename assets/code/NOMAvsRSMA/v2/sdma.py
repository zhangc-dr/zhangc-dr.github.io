import numpy as np
import os
import pandas as pd
import datashader as ds
import datashader.transfer_functions as tf
import glob
from datashader.transfer_functions import dynspread, set_background
from datashader.colors import viridis

class SDMARegion:
    def __init__(self, Nt=3, user_loc=[-10, 10], betas=[1, 0.5], sigma_2=0.05):
        self.Nt = Nt
        self.thetas = np.array(user_loc) / 180 * np.pi
        self.betas = np.array(betas)
        self.sigma_2 = sigma_2
        self.h1 = self.betas[0] * np.exp(1j * np.pi * np.sin(self.thetas[0]) * np.arange(Nt))
        self.h2 = self.betas[1] * np.exp(1j * np.pi * np.sin(self.thetas[1]) * np.arange(Nt))
        self.v1_list = self._generate_unit_vectors(Nt, num=2000)
        self.v2_list = self._generate_unit_vectors(Nt, num=2000)
        self.alpha = np.linspace(0, 1, 10)

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
        # 按照 R1 降序排列，如果 R1 相等则按 R2 升序
        sorted_idx = np.lexsort((-points[:, 1], points[:, 0]))[::-1]
        sorted_points = points[sorted_idx]

        pareto = []
        max_r2 = -np.inf

        for r1, r2 in sorted_points:
            if r2 > max_r2:
                pareto.append((r1, r2))
                max_r2 = r2

        return pareto

    def compute_render(self, batch_size1=100, batch_size2=200, save_dir='data', img_file='img/sdma.png'):
        os.makedirs(save_dir, exist_ok=True)

        total_v1 = len(self.v1_list)
        total_v2 = len(self.v2_list)

        for start1 in range(0, total_v1, batch_size1):
            end1 = min(start1 + batch_size1, total_v1)
            batch_v1 = self.v1_list[start1:end1]

            filepath = os.path.join(save_dir, f'pareto_batch_{start1}.csv')
            if os.path.exists(filepath):
                os.remove(filepath)

            for start2 in range(0, total_v2, batch_size2):
                end2 = min(start2 + batch_size2, total_v2)
                batch_v2 = self.v2_list[start2:end2]

                batch_points = []
                for v1 in batch_v1:
                    for v2 in batch_v2:
                        for a in self.alpha:
                            p1, p2 = a, 1 - a
                            interf1 = np.abs(np.vdot(self.h1, v2))**2 * p2
                            sig1 = np.abs(np.vdot(self.h1, v1))**2 * p1
                            R1 = np.log2(1 + sig1 / (interf1 + self.sigma_2))

                            interf2 = np.abs(np.vdot(self.h2, v1))**2 * p1
                            sig2 = np.abs(np.vdot(self.h2, v2))**2 * p2
                            R2 = np.log2(1 + sig2 / (interf2 + self.sigma_2))

                            batch_points.append((R1, R2))

                pareto_points = self.is_pareto_efficient_2d(batch_points)
                df = pd.DataFrame(pareto_points, columns=['R1', 'R2'])

                df.to_csv(filepath, mode='a', header=not os.path.exists(filepath), index=False)
                print(f"已追加 {len(df)} 个点到文件: {filepath}")

        print("全部批次数据处理完毕，开始后续渲染等操作。")

        # 渲染所有批次数据
        files = glob.glob(os.path.join(save_dir, 'pareto_batch_*.csv'))
        all_points = []

        for fpath in files:
            df = pd.read_csv(fpath)
            all_points.append(df)

        all_df = pd.concat(all_points, ignore_index=True)

        canvas = ds.Canvas(plot_width=400, plot_height=400)
        agg = canvas.points(all_df, 'R1', 'R2')

        # 使用更清晰的渲染方法
        img = tf.shade(agg, cmap=viridis, how='eq_hist')
        img = dynspread(img, threshold=0.5, max_px=4)
        img = set_background(img, "white")

        os.makedirs(os.path.dirname(img_file), exist_ok=True)
        img.to_pil().save(img_file)
        print(f"渲染图片已保存到 {img_file}")

        # 删除所有批次 CSV 文件
        for fpath in files:
            try:
                os.remove(fpath)
            except Exception as e:
                print(f"删除文件 {fpath} 时出错: {e}")
        print("已删除所有批次 CSV 文件。")
