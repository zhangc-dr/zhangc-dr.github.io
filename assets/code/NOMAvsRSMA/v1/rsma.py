import numpy as np
import pandas as pd
import datashader as ds
import datashader.transfer_functions as tf
import os

class RSMARegion:
    def __init__(self, Nt=3, user_loc=[-10, 10], betas=[1, 0.5], sigma_2=0.05):
        self.Nt = Nt
        self.thetas = np.array(user_loc) / 180 * np.pi
        self.betas = np.array(betas)
        self.sigma_2 = sigma_2
        self.h1 = self.betas[0] * np.exp(1j * np.pi * np.sin(self.thetas[0]) * np.arange(Nt))
        self.h2 = self.betas[1] * np.exp(1j * np.pi * np.sin(self.thetas[1]) * np.arange(Nt))
        self.v1_list = self._generate_unit_vectors(Nt, num=200)
        self.v2_list = self._generate_unit_vectors(Nt, num=200)
        self.vc_list = self._generate_unit_vectors(Nt, num=200)
        self.alpha = np.arange(0, 1.01, 0.2)
        self.beta = np.arange(0, 1.01, 0.2)
        self.gamma = np.arange(0, 1.01, 0.2)

    def _generate_unit_vectors(self, Nt, num=100):
        vecs = []
        for _ in range(num):
            real = np.random.randn(Nt)
            imag = np.random.randn(Nt)
            v = real + 1j * imag
            v = v / np.linalg.norm(v)
            vecs.append(v)
        return vecs

    def compute_and_render(self, batch_size=10, filename='img/rsma.png', tmp_csv='data/tmp_rsma.csv'):
        # 清空csv
        if os.path.exists(tmp_csv):
            os.remove(tmp_csv)
        total_v1 = len(self.v1_list)
        total_v2 = len(self.v2_list)
        total_vc = len(self.vc_list)
        for start1 in range(0, total_v1, batch_size):
            end1 = min(start1 + batch_size, total_v1)
            batch_v1 = self.v1_list[start1:end1]
            for start2 in range(0, total_v2, batch_size):
                end2 = min(start2 + batch_size, total_v2)
                batch_v2 = self.v2_list[start2:end2]
                for startc in range(0, total_vc, batch_size):
                    endc = min(startc + batch_size, total_vc)
                    batch_vc = self.vc_list[startc:endc]
                    batch_R1 = []
                    batch_R2 = []
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
                                        for gamma in self.gamma:
                                            R1 = gamma * Rc + Rp1
                                            R2 = (1 - gamma) * Rc + Rp2
                                            batch_R1.append(R1)
                                            batch_R2.append(R2)
                    # 分批写入csv
                    if batch_R1:
                        df = pd.DataFrame({'R1': batch_R1, 'R2': batch_R2})
                        df.to_csv(tmp_csv, mode='a', header=not os.path.exists(tmp_csv), index=False)
        # 全部数据写完后一次性读取绘图
        all_df = pd.read_csv(tmp_csv)
        cvs = ds.Canvas(plot_width=400, plot_height=400)
        agg = cvs.points(all_df, 'R1', 'R2')
        img = tf.shade(agg)
        img.to_pil().save(filename)
        os.remove(tmp_csv)