Description
===========

ASTDR is a derainbow function for VapourSynth. ASTDRmc performs motion
compensation before calling ASTDR.

This is a port of the Avisynth function of the same name, version 1.74.


Usage
=====
::

    ASTDR(input_clip[, strength=5, tempsoftth=30, tempsoftrad=3, tempsoftsc=3, blstr, tht=255, fluxstv, dcn=15, edgem=False, exmc=False, edgemprefil=None, separated=False])


Parameters:
    *input_clip*
        A clip to process.

    *strength*
        Passed to Hqdn3d's *chrom_spac* and *chrom_tmp* parameters.

        Default: 5.

    *tempsoftth*
        Passed to TemporalSoften2's *chroma_threshold* parameter.

        Default: 30.

    *tempsoftrad*
        Passed to TemporalSoften2's *radius* parameter.

        Default: 3.

    *tempsoftsc*
        Passed to TemporalSoften2's *scenechange* parameter.

        Default: 3.

    *blstr*
        Blurring strength.

        Default: 0.3 if *separated* is True, otherwise 0.5.

    *tht*
        Passed to MotionMask's *tht* parameter.

        Default: 255.

    *fluxstv*
        Passed to flux.SmoothST's *temporal_threshold* and *spatial_threshold* parameters.

        Default: 60 if *separated* is True, otherwise 75.

    *dcn*
        Passed to DeCross's *noise* parameter.

        Default: 15.

    *edgem*
        If True, only edges detected in the luma will be filtered.
        
        Default: False.

    *exmc*
        Set to True if using external motion compensation, i.e. if *input_clip* came from std.Interleave[forward_compensated, original, backward_compensated]) or something similar.

        Default: False.

    *edgemprefil*
        Pre-filtered clip for edge detection. Used only if *edgem* is True.

        Default: None.

    *separated*
        Set to True if *input_clip* came from std.SeparateFields.

        Default: False.


::

    ASTDRmc(input_clip[, strength, tempsoftth, tempsoftrad, tempsoftsc, blstr, tht, fluxstv, dcn, edgem, thsad=tht, prefil=None, chroma=False, edgemprefil, separated=False])


Most parameters are the same as ASTDR's. The differences are documented below:
    *tempsoftth*
        Passed to TemporalSoften2's *chroma_threshold* parameter.

        Default: 50 if *separated* is True, otherwise 30.

    *tempsoftrad*
        Passed to TemporalSoften2's *radius* parameter. It can be at most 5.

        Default: 5 if *separated* is True, otherwise 3.

    *edgem*
        If True, only edges detected in the luma will be filtered.

        Default: *separated*.

    *thsad*
        Passed to mv.Compensate.

        Default: *tht*.

    *prefil*
        Input clip prefiltered for better motion estimation.

        Default: None.

    *chroma*
        Passed to mv.Analyse.

        Default: False.


Requirements
============

ASTDR function requirements:
   * `AWarpSharp2 v4 or newer    <https://github.com/dubhater/vapoursynth-awarpsharp2/releases>`_
   * `DeCross                    <https://github.com/dubhater/vapoursynth-decross/releases>`_
   * `FluxSmooth                 <https://github.com/dubhater/vapoursynth-fluxsmooth/releases>`_
   * `Hqdn3d                     <https://github.com/Hinterwaeldlers/vapoursynth-hqdn3d/releases>`_
   * `TemporalSoften2 v1 or newer           <https://github.com/dubhater/vapoursynth-temporalsoften2/releases>`_
   * `FFT3DFilter                <https://github.com/myrsloik/VapourSynth-FFT3DFilter/releases>`_
   * `MotionMask                 <https://github.com/dubhater/vapoursynth-motionmask/releases>`_
   * `Miscellaneous Filters (included with VapourSynth) <http://www.vapoursynth.com/doc/plugins/misc.html>`_
   * `Adjust script              <https://forum.doom9.org/showthread.php?t=172808>`_

ASTDRmc function requirements:
   * ASTDR function
   * `MVTools                    <https://github.com/dubhater/vapoursynth-mvtools/releases>`_
   * `CTMF                       <https://github.com/HomeOfVapourSynthEvolution/VapourSynth-CTMF/releases>`_
   * `RGVS (included with VapourSynth) <http://www.vapoursynth.com/doc/plugins/rgvs.html>`_


License
=======

???
