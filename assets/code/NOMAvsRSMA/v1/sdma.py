import numpy as np
import pandas as pd
import datashader as ds
import datashader.transfer_functions as tf
import os

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
        self.alpha = np.arange(0, 1.01, 0.05)

    def _generate_unit_vectors(self, Nt, num):
        vecs = []
        for _ in range(num):
            real = np.random.randn(Nt)
            imag = np.random.randn(Nt)
            v = real + 1j * imag
            v = v / np.linalg.norm(v)
            vecs.append(v)
        return vecs

    def compute_and_render(self, batch_size=50, imgfilename='img/sdma.png', tmp_csv='data/tmp_sdma.csv'):
        # 清空临时文件
        if os.path.exists(tmp_csv):
            os.remove(tmp_csv)
        total_v1 = len(self.v1_list)
        total_v2 = len(self.v2_list)
        for start1 in range(0, total_v1, batch_size):
            end1 = min(start1 + batch_size, total_v1)
            batch_v1 = self.v1_list[start1:end1]
            for start2 in range(0, total_v2, batch_size):
                end2 = min(start2 + batch_size, total_v2)
                batch_v2 = self.v2_list[start2:end2]
                R1_list = []
                R2_list = []
                for v1 in batch_v1:
                    for v2 in batch_v2:
                        for a in self.alpha:
                            p1 = a
                            p2 = 1 - a
                            interf1 = np.abs(np.vdot(self.h1, v2))**2 * p2
                            sig1 = np.abs(np.vdot(self.h1, v1))**2 * p1
                            R1 = np.log2(1 + sig1 / (interf1 + self.sigma_2))
                            interf2 = np.abs(np.vdot(self.h2, v1))**2 * p1
                            sig2 = np.abs(np.vdot(self.h2, v2))**2 * p2
                            R2 = np.log2(1 + sig2 / (interf2 + self.sigma_2))
                            R1_list.append(R1)
                            R2_list.append(R2)
                # 每小批写入磁盘
                df = pd.DataFrame({'R1': R1_list, 'R2': R2_list})
                df.to_csv(tmp_csv, mode='a', header=not os.path.exists(tmp_csv), index=False)
        # 全部数据写完后再一次性读取
        all_df = pd.read_csv(tmp_csv)
        cvs = ds.Canvas(plot_width=400, plot_height=400)
        agg = cvs.points(all_df, 'R1', 'R2')
        img = tf.shade(agg)
        img.to_pil().save(imgfilename)
        os.remove(tmp_csv)