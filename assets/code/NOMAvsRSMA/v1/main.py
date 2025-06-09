from noma import NOMARegion
from sdma import SDMARegion
from rsma import RSMARegion
from nonGNOMA import NonGroupNOMARegion

Nt = 3
user_loc = [-5, 5]
beta_list = [0.1, 1.0]

for bata in beta_list:
    betas = [1, bata]
    # NOMA
    noma_region = NOMARegion(Nt=Nt, user_loc=user_loc, betas=betas)
    noma_region.compute_and_render(imgfilename=f'img/noma_5_{bata}.png', tmp_csv=f'data/tmp_noma_5_{bata}.csv')
    # SDMA
    sdma_region = SDMARegion(Nt=Nt, user_loc=user_loc, betas=betas)
    sdma_region.compute_and_render(imgfilename=f'img/sdma_5_{bata}.png', tmp_csv=f'data/tmp_sdma_5_{bata}.csv')
    # RSMA
    rsma_region = RSMARegion(Nt=Nt, user_loc=user_loc, betas=betas)
    rsma_region.compute_and_render(filename=f'img/rsma_5_{bata}.png', tmp_csv=f'data/tmp_rsma_5_{bata}.csv')
    # non_group NOMA
    ng_noma_region = NonGroupNOMARegion(Nt=Nt, user_loc=user_loc, betas=betas)
    ng_noma_region.compute_and_render(imgfilename=f'img/ng_noma_5_{bata}.png', tmp_csv=f'data/tmp_ng_noma_5_{bata}.csv')
