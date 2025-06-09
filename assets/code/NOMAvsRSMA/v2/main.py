from noma import NOMARegion
from sdma import SDMARegion
from rsma import RSMARegion
from nonGNOMA import NonGroupNOMARegion

Nt = 3

theta_beta_combinations = [(theta, 0.5) for theta in [1, 5, 30]] + [(5, beta) for beta in [0.1, 1]]

for theta, beta in theta_beta_combinations:
    user_loc = [-theta, theta]
    betas = [1, beta]
    
    # NOMA
    # noma_region = NOMARegion(Nt=Nt, user_loc=user_loc, betas=betas)
    # noma_region.compute_render(img_file=f'img/noma_{theta}_{beta}.png')

    # SDMA
    # sdma_region = SDMARegion(Nt=Nt, user_loc=user_loc, betas=betas)
    # sdma_region.compute_render(img_file=f'img/sdma_{theta}_{beta}.png')

    # RSMA
    # rsma_region = RSMARegion(Nt=Nt, user_loc=user_loc, betas=betas)
    # rsma_region.compute_render(img_file=f'img/rsma_{theta}_{beta}.png')

    # Non-Group NOMA
    # ngnoma_region = NonGroupNOMARegion(Nt=Nt, user_loc=user_loc, betas=betas)
    # ngnoma_region.compute_render(img_file=f'img/ngnoma_{theta}_{beta}.png')
