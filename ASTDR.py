import vapoursynth as vs
import adjust


# Based on ASTDR DeRainbow function v1.74 for Avisynth


# amount doesn't go below 0 because std.Convolution doesn't take coefficients greater than 1023.
def BlurForASTDR(clip, amount=0, planes=None):
    lower_limit = 0
    upper_limit = 1.5849625
    if amount < lower_limit or amount > upper_limit:
        raise ValueError("BlurForASTDR: amount must be between {} and {}.".format(lower_limit, upper_limit))

    center_weight = 1 / pow(2, amount)
    side_weight = (1 - center_weight) / 2

    corner = int(side_weight * side_weight * 1000 + 0.5)
    side = int(side_weight * center_weight * 1000 + 0.5)
    center = int(center_weight * center_weight * 1000 + 0.5)

    blur_matrix = [corner,   side, corner,
                     side, center,   side,
                   corner,   side, corner]

    return clip.std.Convolution(matrix=blur_matrix, planes=planes)


def ASTDR(input_clip, strength=5, tempsoftth=30, tempsoftrad=3, tempsoftsc=3, blstr=None, tht=255, fluxstv=None, dcn=15, edgem=False, exmc=False, edgemprefil=None, separated=False):
    core = vs.get_core()


    sisfield = separated
    fnomc = sisfield && !exmc
    strn = strength
    if blstr is None:
        if sisfield:
            blstr = 0.3
        else:
            blstr = 0.5
    tschrth = tempsoftth
    tschrrad = tempsoftrad
    tschrsc = tempsoftsc / 255
    if fluxstv is None:
        if sisfield:
            fluxstv = 60
        else:
            fluxstv = 75

    inrainev = input_clip
    if fnomc:
        inrainev = input_clip.std.SelectEvery(cycle=2, offsets=0)

    filtered_uv = inrainev
    if not exmc:
        filtered_uv = inrainev.decross.DeCross(thresholdy=15, noise=dcn, margin=1)

    flux_spatial_threshold = fluxstv
    if sisfield:
        flux_spatial_threshold = fluxstv // 2

    filtered_uv = filtered_uv.flux.SmoothST(temporal_threshold=fluxstv, spatial_threshold=flux_spatial_threshold, planes=[1, 2])

    if not sisfield:
        filtered_uv = filtered_uv.warp.AWarpSharp2(depth=4, chroma=0, cplace="mpeg2", planes=[1, 2])

    cs = strn * 3 / 5
    if sisfield:
        cs = strn * 2 / 5
    filtered_uv = filtered_uv.hqdn3d.Hqdn3d(lum_spac=0, lum_tmp=0, chrom_spac=cs, chrom_tmp=strn).misc.SCDetect(threshold=tschrsc).focus2.TemporalSoften2(radius=tschrrad, luma_threshold=0, chroma_threshold=tschrth, mode=2)
    filtered_uv = BlurForASTDR(filtered_uv, amount=blstr, planes=[1, 2])

    if not sisfield:
        filtered_uv = filtered_uv.warp.AWarpSharp2(depth=4, chroma=0, cplace="mpeg2", planes=[1, 2])

    sigma = 1
    sigma3 = 4
    if sisfield:
        sigma = 0.7
        sigma3 = 3

    filtered_uv = filtered_uv.fft3dfilter.FFT3DFilter(sigma=sigma, sigma3=sigma3, planes=[1, 2], degrid=1)

    if fnomc:
        filtered_odd = input_clip.std.SelectEvery(cycle=2, offsets=1)
        filtered_odd = filtered_odd.decross.DeCross(thresholdy=15, noise=dcn, margin=1).flux.SmoothST(temporal_threshold=fluxstv, spatial_threshold=flux_spatial_threshold, planes=[1, 2])
        filtered_odd = filtered_odd.hqdn3d.Hqdn3d(lum_spac=0, lum_tmp=0, chrom_spac=cs, chrom_tmp=strn).mist.SCDetect(threshold=tschrsc).focus2.TemporalSoften2(radius=tschrrad, luma_threshold=0, chroma_threshold=tschrth, mode=2)
        filtered_odd = BlurForASTDR(filtered_odd, amount=blstr, planes=[1, 2])
        filtered_odd = filtered_odd.fft3dfilter.FFT3DFilter(sigma=sigma, sigma3=sigma3, planes=[1, 2], degrid=1)
        filtered_uv = core.std.Interleave([filtered_uv, filtered_odd])


    last = filtered_uv

    if not exmc:
        momask = adjust.Tweak(clip=input_clip, sat=1.1).MotionMask(th1=1, th2=1, tht=tht)
        momaskinv = momask.std.Maximum(planes=0).std.Inflate(planes=0).std.Invert(planes=0).std.Levels(min_in=0, gamma=2, max_in=255, min_out=0, max_out=255, planes=0)

        filtered = core.std.MaskedMerge(filtered_uv, input_clip, momaskinv, first_plane=True, planes=[1, 2])
        last = core.std.MaskedMerge(input_clip, filtered, momask.std.Maximum(planes=[1, 2]).std.Inflate(planes=[1, 2]), planes=[1, 2])

    if edgem:
        if edgemprefil is None:
            edgemprefil = input_clip

        edgemclip = edgemprefil.std.Sobel(planes=0).std.Binarize(threshold=5, planes=0).std.Maximum(planes=0).std.Inflate(planes=0)
        last = core.std.MaskedMerge(input_clip, last, edgemclip, first_plane=True, planes=[1, 2])

    return last
