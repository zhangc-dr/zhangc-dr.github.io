import numpy as np
import pandas as pd
import datashader as ds
import datashader.transfer_functions as tf
from datashader.transfer_functions import dynspread, set_background
from datashader.colors import viridis
import os
import glob

class RSMARegion:
    def __init__(self, Nt=3, user_loc=[-10, 10], betas=[1, 0.5], sigma_2=0.05):
        self.Nt = Nt
        self.thetas = np.array(user_loc) / 180 * np.pi
        self.betas = np.array(betas)
        self.sigma_2 = sigma_2
        self.h1 = self.betas[0] * np.exp(1j * np.pi * np.sin(self.thetas[0]) * np.arange(Nt))
        self.h2 = self.betas[1] * np.exp(1j * np.pi * np.sin(self.thetas[1]) * np.arange(Nt))
        self.v1_list = self._generate_unit_vectors(Nt, num=300)
        self.v2_list = self._generate_unit_vectors(Nt, num=300)
        self.vc_list = self._generate_unit_vectors(Nt, num=300)
        self.alpha = np.linspace(0, 1, 5)
        self.beta = np.linspace(0, 1, 5)
        self.gamma = np.linspace(0, 1, 5)

    def _generate_unit_vectors(self, Nt, num=100):
        vecs = []
        for _ in range(num):
            real = np.random.randn(Nt)
            imag = np.random.randn(Nt)
            v = real + 1j * imag
            v /= np.linalg.norm(v)
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

    def compute_render(self, batch_size1=10, batch_size2=50, batch_size3=50, save_dir='data', img_file='img/rsma.png'):
        os.makedirs(save_dir, exist_ok=True)

        total_v1 = len(self.v1_list)
        total_v2 = len(self.v2_list)
        total_vc = len(self.vc_list)

        for start1 in range(0, total_v1, batch_size1):
            end1 = min(start1 + batch_size1, total_v1)
            batch_v1 = self.v1_list[start1:end1]

            filepath = os.path.join(save_dir, f'rsma_batch_{start1}.csv')
            if os.path.exists(filepath):
                os.remove(filepath)

            for start2 in range(0, total_v2, batch_size2):
                end2 = min(start2 + batch_size2, total_v2)
                batch_v2 = self.v2_list[start2:end2]

                for startc in range(0, total_vc, batch_size3):
                    endc = min(startc + batch_size3, total_vc)
                    batch_vc = self.vc_list[startc:endc]

                    batch_points = []

                    for v1 in batch_v1:
                        for v2 in batch_v2:
                            for vc in batch_vc:
                                for a in self.alpha:
                                    for b in self.beta:
                                        Pc = b
                                        P1 = a * (1 - b)
                                        P2 = (1 - a) * (1 - b)

                                        interf1 = np.abs(np.vdot(self.h1, v2))**2 * P2
                                        sig1 = np.abs(np.vdot(self.h1, v1))**2 * P1
                                        sigc1 = np.abs(np.vdot(self.h1, vc))**2 * Pc
                                        SINR_c1 = sigc1 / (sig1 + interf1 + self.sigma_2)
                                        SINR_p1 = sig1 / (interf1 + self.sigma_2)
                                        Rc1 = np.log2(1 + SINR_c1)
                                        Rp1 = np.log2(1 + SINR_p1)

                                        interf2 = np.abs(np.vdot(self.h2, v1))**2 * P1
                                        sig2 = np.abs(np.vdot(self.h2, v2))**2 * P2
                                        sigc2 = np.abs(np.vdot(self.h2, vc))**2 * Pc
                                        SINR_c2 = sigc2 / (sig2 + interf2 + self.sigma_2)
                                        SINR_p2 = sig2 / (interf2 + self.sigma_2)
                                        Rc2 = np.log2(1 + SINR_c2)
                                        Rp2 = np.log2(1 + SINR_p2)

                                        Rc = min(Rc1, Rc2)

                                        for g in self.gamma:
                                            R1 = g * Rc + Rp1
                                            R2 = (1 - g) * Rc + Rp2
                                            batch_points.append((R1, R2))

                    if batch_points:
                        pareto_points = self.is_pareto_efficient_2d(batch_points)
                        df = pd.DataFrame(pareto_points, columns=['R1', 'R2'])
                        df.to_csv(filepath, mode='a', header=not os.path.exists(filepath), index=False)
                        print(f"已追加 {len(df)} 个点到文件: {filepath}")

        print("全部批次数据处理完毕，开始后续渲染等操作。")

        files = glob.glob(os.path.join(save_dir, 'rsma_batch_*.csv'))
        all_points = []

        for fpath in files:
            df = pd.read_csv(fpath)
            all_points.append(df)

        all_df = pd.concat(all_points, ignore_index=True)

        canvas = ds.Canvas(plot_width=400, plot_height=400)
        agg = canvas.points(all_df, 'R1', 'R2')

        img = tf.shade(agg, cmap=viridis, how='eq_hist')
        img = dynspread(img, threshold=0.5, max_px=4)
        img = set_background(img, "white")

        os.makedirs(os.path.dirname(img_file), exist_ok=True)
        img.to_pil().save(img_file)
        print(f"渲染图片已保存到 {img_file}")

        for fpath in files:
            try:
                os.remove(fpath)
            except Exception as e:
                print(f"删除文件 {fpath} 时出错: {e}")
        print("已删除所有批次 CSV 文件。")
