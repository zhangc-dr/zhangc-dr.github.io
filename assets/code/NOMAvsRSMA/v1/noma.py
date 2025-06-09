import numpy as np
import pandas as pd
import datashader as ds
import datashader.transfer_functions as tf
import os

class NOMARegion:
    def __init__(self, Nt=3, user_loc=[-10, 10], betas=[1, 0.5], sigma_2=0.05):
        self.Nt = Nt
        self.thetas = np.array(user_loc) / 180 * np.pi
        self.betas = np.array(betas)
        self.sigma_2 = sigma_2
        self.h1 = self.betas[0] * np.exp(1j * np.pi * np.sin(self.thetas[0]) * np.arange(Nt))
        self.h2 = self.betas[1] * np.exp(1j * np.pi * np.sin(self.thetas[1]) * np.arange(Nt))
        self.v_list = self._generate_unit_vectors(Nt, num=50000)
        self.alpha = np.arange(0, 1.01, 0.01)

    def _generate_unit_vectors(self, Nt, num):
        vecs = []
        for _ in range(num):
            real = np.random.randn(Nt)
            imag = np.random.randn(Nt)
            v = real + 1j * imag
            v = v / np.linalg.norm(v)
            vecs.append(v)
        return vecs

    def compute_and_render(self, batch_size=100, imgfilename='img/noma.png', tmp_csv='data/tmp_noma.csv'):
        # 清空旧csv
        if os.path.exists(tmp_csv):
            os.remove(tmp_csv)
        total_v = len(self.v_list)
        for start in range(0, total_v, batch_size):
            end = min(start + batch_size, total_v)
            batch_v = self.v_list[start:end]
            batch_R1 = []
            batch_R2 = []
            batch_user = []
            for v in batch_v:
                h1v = np.abs(np.vdot(v, self.h1)) ** 2
                h2v = np.abs(np.vdot(v, self.h2)) ** 2
                strong = h1v > h2v
                if strong:
                    R1 = np.log2(1 + self.alpha * h1v / self.sigma_2)
                    R2 = np.log2(1 + (1 - self.alpha) * h2v / (self.alpha * h2v + self.sigma_2))
                    batch_R1.extend(R1)
                    batch_R2.extend(R2)
                    batch_user.extend(['user1 stronger'] * len(R1))
                else:
                    R1 = np.log2(1 + self.alpha * h1v / ((1 - self.alpha) * h1v + self.sigma_2))
                    R2 = np.log2(1 + (1 - self.alpha) * h2v / self.sigma_2)
                    batch_R1.extend(R1)
                    batch_R2.extend(R2)
                    batch_user.extend(['user2 stronger'] * len(R1))
            df = pd.DataFrame({'R1': batch_R1, 'R2': batch_R2, 'user': batch_user})
            df.to_csv(tmp_csv, mode='a', header=not os.path.exists(tmp_csv), index=False)
        # 全部数据写入完毕后一次性读取
        all_df = pd.read_csv(tmp_csv)
        all_df['user'] = all_df['user'].astype('category') 
        cvs = ds.Canvas(plot_width=400, plot_height=400)
        agg = cvs.points(all_df, 'R1', 'R2', ds.count_cat('user'))
        color_key = {'user1 stronger': 'blue', 'user2 stronger': 'red'}
        img = tf.shade(agg, color_key=color_key, how='eq_hist')
        img.to_pil().save(imgfilename)
        os.remove(tmp_csv)