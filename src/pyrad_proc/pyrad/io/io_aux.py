"""
pyrad.io.io_aux
===============

Auxiliary functions for reading/writing files

.. autosummary::
    :toctree: generated/

    get_rad4alp_prod_fname
    map_hydro
    map_Doppler
    get_save_dir
    make_filename
    generate_field_name_str
    get_datatype_metranet
    get_datatype_odim
    get_fieldname_pyart
    get_fieldname_cosmo
    get_field_unit
    get_field_name
    get_file_list
    get_rad4alp_dir
    get_rad4alp_grid_dir
    get_trtfile_list
    get_scan_list
    get_new_rainbow_file_name
    get_datatype_fields
    get_dataset_fields
    get_datetime
    find_raw_cosmo_file
    find_cosmo_file
    find_hzt_file
    find_rad4alpcosmo_file
    _get_datetime
    find_date_in_file_name


"""

import os
import glob
import re
import datetime

from warnings import warn
from copy import deepcopy
import numpy as np

from pyart.config import get_metadata


def get_rad4alp_prod_fname(datatype):
    """
    Given a datatype find the corresponding start and termination of the
    METRANET product file name

    Parameters
    ----------
    datatype : str
        the data type

    Returns
    -------
    acronym : str
        The start of the METRANET file name
    termination : str
        The end of the METRANET file name

    """
    # datatype missing:
    # NHC (Hail forecast)
    # NZC (Thunderstorm forecast based on TRT)

    termination = '.8??'
    # Polar products
    if datatype == 'hydro':
        acronym = 'YM'
    elif datatype == 'dealV':
        acronym = 'DV'

    # rainfall accumulation products
    elif datatype == 'AZC01':
        acronym = 'AZC' # Rain rate accumulation with local bias corrected
        termination = '.801'
    elif datatype == 'AZC03':
        acronym = 'AZC' # Rain rate accumulation with local bias corrected
        termination = '.803'
    elif datatype == 'AZC06':
        acronym = 'AZC' # Rain rate accumulation with local bias corrected
        termination = '.806'
    elif datatype == 'aZC01':
        acronym = 'aZC' # Rain rate accumulation with local bias not corrected
        termination = '.801'
    elif datatype == 'aZC03':
        acronym = 'aZC' # Rain rate accumulation with local bias not corrected
        termination = '.803'
    elif datatype == 'aZC06':
        acronym = 'aZC' # Rain rate accumulation with local bias not corrected
        termination = '.806'

    # CPC
    elif datatype == 'CPC0005':
        acronym = 'CPC'
        termination = '_00005.801.gif'
    elif datatype == 'CPC0060':
        acronym = 'CPC'
        termination = '_00060.801.gif'
    elif datatype == 'CPC0180':
        acronym = 'CPC'
        termination = '_00180.801.gif'
    elif datatype == 'CPC0360':
        acronym = 'CPC'
        termination = '_00360.801.gif'
    elif datatype == 'CPC0720':
        acronym = 'CPC'
        termination = '_00720.801.gif'
    elif datatype == 'CPC1440':
        acronym = 'CPC'
        termination = '_01440.801.gif'
    elif datatype == 'CPC2880':
        acronym = 'CPC'
        termination = '_02880.801.gif'
    elif datatype == 'CPC4320':
        acronym = 'CPC'
        termination = '_04320.801.gif'

    elif datatype == 'CPCH0005':
        acronym = 'CPC'
        termination = '_00005.801.gif'
    elif datatype == 'CPCH0060':
        acronym = 'CPC'
        termination = '_00060.801.gif'
    elif datatype == 'CPCH0180':
        acronym = 'CPC'
        termination = '_00180.801.gif'
    elif datatype == 'CPCH0360':
        acronym = 'CPC'
        termination = '_00360.801.gif'
    elif datatype == 'CPCH0720':
        acronym = 'CPC'
        termination = '_00720.801.gif'
    elif datatype == 'CPCH1440':
        acronym = 'CPC'
        termination = '_01440.801.gif'
    elif datatype == 'CPCH2880':
        acronym = 'CPC'
        termination = '_02880.801.gif'
    elif datatype == 'CPCH4320':
        acronym = 'CPC'
        termination = '_04320.801.gif'

    elif datatype == 'nowpal60_P60':
        acronym = 'AZC'
        termination = '.accu_0060_RZC_60'
    elif datatype == 'nowpal90_P90':
        acronym = 'AZC'
        termination = '.accu_0090_RZC_90'
    elif datatype == 'nowpal180_P180':
        acronym = 'AZC'
        termination = '.accu_0180_RZC_180'
    elif datatype == 'nowpal360_P360':
        acronym = 'AZC'
        termination = '.accu_0360_RZC_360'
    elif datatype == 'nowpal720_P720':
        acronym = 'AZC'
        termination = '.accu_0720_RZC_720'

    elif datatype == 'nowpal90_P30':
        acronym = 'AZC'
        termination = '.accu_0090_RZC_30'
    elif datatype == 'nowpal90_P30_F60':
        acronym = 'AZC'
        termination = '.accu_0090_RZC_30_INCA_60'
    elif datatype == 'nowpal90_F60':
        acronym = 'AZC'
        termination = '.accu_0090_INCA_60'
    elif datatype == 'nowpal180_P60':
        acronym = 'AZC'
        termination = '.accu_0180_RZC_60'
    elif datatype == 'nowpal180_P60_F120':
        acronym = 'AZC'
        termination = '.accu_0180_RZC_60_INCA_120'
    elif datatype == 'nowpal180_F120':
        acronym = 'AZC'
        termination = '.accu_0180_INCA_120'
    elif datatype == 'nowpal360_P120':
        acronym = 'AZC'
        termination = '.accu_0360_CPC_120'
    elif datatype == 'nowpal360_P120_F240':
        acronym = 'AZC'
        termination = '.accu_0360_CPC_120_INCA_240'
    elif datatype == 'nowpal360_F240':
        acronym = 'AZC'
        termination = '.accu_0360_INCA_240'
    elif datatype == 'nowpal720_P360':
        acronym = 'AZC'
        termination = '.accu_0720_CPC_360'
    elif datatype == 'nowpal720_P360_F360':
        acronym = 'AZC'
        termination = '.accu_0720_CPC_360_INCA_360'
    elif datatype == 'nowpal720_F360':
        acronym = 'AZC'
        termination = '.accu_0720_INCA_360'

    elif datatype == 'dACC':
        acronym = 'ACC' # Daily precip accumulation using NowPal with CPC
        termination = '.1440'
    elif datatype == 'dACCH':
        acronym = 'ACC' # reprocessed after 8 days
        termination = '.1440'
    elif datatype == 'dARC':
        acronym = 'ARC' # Daily precip accumulation using NowPal with RZC
        termination = '.1440'

    # rainfall rate products
    elif datatype == 'RZC':
        acronym = 'RZC'  # rain rate local bias corrected
    elif datatype == 'R1F':
        acronym = 'R1F' # RZC including best foreign radars
    elif datatype == 'rZC':
        acronym = 'rZC' # local bias not corrected
    elif datatype == 'RZF':
        acronym = 'RZF' # RZC including foreign radars
    elif datatype == 'dRZC':
        acronym = 'RZC'  # Daily maximum rain rate

    # hail products
    elif datatype in ('BZC', 'dBZC'):
        acronym = 'BZC' # POH
    elif datatype in ('MZC', 'dMZC'):
        acronym = 'MZC' # Maximum expected severe hail size
    elif datatype == 'GZC':
        acronym = 'GZC' # Hail probability derived from reflectivity
        termination = '.803'
    elif datatype == 'dGZC':
        acronym = 'GZC'
        termination = '.824'

    # max echo
    elif datatype in ('CZC', 'dCZC'):
        acronym = 'CZC' # max echo
    elif datatype == 'HZC':
        acronym = 'HZC' # Max echo height

    # echo tops
    elif datatype in ('EZC15', 'dEZC15'):
        acronym = 'EZC' # echo top
        termination = '.815'
    elif datatype == 'EZC20':
        acronym = 'EZC' # echo top
        termination = '.820'
    elif datatype in ('EZC45', 'dEZC45'):
        acronym = 'EZC'
        termination = '.845'
    elif datatype == 'EZC50':
        acronym = 'EZC'
        termination = '.850'

    # Vertically integrated liquid
    elif datatype in ('LZC', 'dLZC'):
        acronym = 'LZC'

    # Zh CAPPI
    elif datatype in 'OZC01':
        acronym = 'OZC'
        termination = '.810'
    elif datatype in 'OZC02':
        acronym = 'OZC'
        termination = '.820'
    elif datatype in 'OZC03':
        acronym = 'OZC'
        termination = '.830'
    elif datatype in 'OZC04':
        acronym = 'OZC'
        termination = '.840'
    elif datatype in 'OZC05':
        acronym = 'OZC'
        termination = '.850'
    elif datatype in 'OZC06':
        acronym = 'OZC'
        termination = '.860'
    elif datatype in 'OZC07':
        acronym = 'OZC'
        termination = '.870'
    elif datatype in 'OZC08':
        acronym = 'OZC'
        termination = '.880'
    elif datatype in 'OZC09':
        acronym = 'OZC'
        termination = '.890'
    elif datatype in 'OZC10':
        acronym = 'OZC'
        termination = '.900'
    elif datatype in 'OZC11':
        acronym = 'OZC'
        termination = '.910'
    elif datatype in 'OZC12':
        acronym = 'OZC'
        termination = '.920'
    elif datatype in 'OZC13':
        acronym = 'OZC'
        termination = '.930'
    elif datatype in 'OZC14':
        acronym = 'OZC'
        termination = '.940'
    elif datatype in 'OZC15':
        acronym = 'OZC'
        termination = '.950'
    elif datatype in 'OZC16':
        acronym = 'OZC'
        termination = '.960'
    elif datatype in 'OZC17':
        acronym = 'OZC'
        termination = '.970'
    elif datatype in 'OZC18':
        acronym = 'OZC'
        termination = '.980'

    else:
        raise ValueError('ERROR: Unknown rad4alp product data type '+datatype)

    return acronym, termination


def map_hydro(hydro_data_op):
    """
    maps the operational hydrometeor classification identifiers to the ones
    used by Py-ART

    Parameters
    ----------
    hydro_data_op : numpy array
        The operational hydrometeor classification data

    Returns
    -------
    hydro_data_py : numpy array
        The pyart hydrometeor classification data

    """
    hydro_data_py = deepcopy(hydro_data_op)
    hydro_data_py[hydro_data_op == 25] = 3  # crystals
    hydro_data_py[hydro_data_op == 50] = 2  # aggregate
    hydro_data_py[hydro_data_op == 75] = 4  # light rain
    hydro_data_py[hydro_data_op == 100] = 6  # rain
    hydro_data_py[hydro_data_op == 125] = 5  # graupel
    hydro_data_py[hydro_data_op == 150] = 8  # wet snow
    hydro_data_py[hydro_data_op == 175] = 10  # ice hail
    hydro_data_py[hydro_data_op == 200] = 9  # melting hail

    return hydro_data_py


def map_Doppler(Doppler_data_bin, Nyquist_vel):
    """
    maps the binary METRANET Doppler data to actual Doppler velocity

    Parameters
    ----------
    Doppler_data_bin : numpy array
        The binary METRANET data

    Returns
    -------
    Doppler_data : numpy array
        The Doppler veloctiy in [m/s]

    """
    Doppler_data = (Doppler_data_bin-128.)/127.*Nyquist_vel

    return Doppler_data


def get_save_dir(basepath, procname, dsname, prdname, timeinfo=None,
                 timeformat='%Y-%m-%d', create_dir=True):
    """
    obtains the path to a product directory and eventually creates it

    Parameters
    ----------
    basepath : str
        product base path
    procname : str
        name of processing space
    dsname : str
        data set name
    prdname : str
        product name
    timeinfo : datetime
        time info to generate the date directory. If None there is no time
        format in the path
    timeformat : str
        Optional. The time format.
    create_dir : boolean
        If True creates the directory

    Returns
    -------
    savedir : str
        path to product

    """
    if timeinfo is None:
        savedir = basepath+procname+'/'+dsname+'/'+prdname+'/'
    else:
        daydir = timeinfo.strftime(timeformat)
        savedir = basepath+procname+'/'+daydir+'/'+dsname+'/'+prdname+'/'

    if create_dir is False:
        return savedir

    if not os.path.isdir(savedir):
        os.makedirs(savedir)

    return savedir


def make_filename(prdtype, dstype, dsname, ext_list, prdcfginfo=None,
                  timeinfo=None, timeformat='%Y%m%d%H%M%S',
                  runinfo=None):
    """
    creates a product file name

    Parameters
    ----------
    timeinfo : datetime
        time info to generate the date directory
    prdtype : str
        product type, i.e. 'ppi', etc.
    dstype : str
        data set type, i.e. 'raw', etc.
    dsname : str
        data set name
    ext_list : list of str
        file name extensions, i.e. 'png'
    prdcfginfo : str
        Optional. string to add product configuration information, i.e. 'el0.4'
    timeformat : str
        Optional. The time format
    runinfo : str
        Optional. Additional information about the test (e.g. 'RUN01', 'TS011')

    Returns
    -------
    fname_list : list of str
        list of file names (as many as extensions)

    """
    if timeinfo is None:
        timeinfostr = ''
    else:
        timeinfostr = timeinfo.strftime(timeformat)+'_'

    if prdcfginfo is None:
        cfgstr = ''
    else:
        cfgstr = '_' + prdcfginfo

    if runinfo is None or runinfo == '':
        runstr = ''
    else:
        runstr = runinfo + '_'

    fname_list = list()
    for ext in ext_list:
        fname_list.append(timeinfostr + runstr + prdtype + '_' +
                          dstype + '_' + dsname + cfgstr + '.' + ext)

    return fname_list


def generate_field_name_str(datatype):
    """
    Generates a field name in a nice to read format.

    Parameters
    ----------
    datatype : str
        The data type

    Returns
    -------
    field_str : str
        The field name

    """
    field_name = get_fieldname_pyart(datatype)
    field_dic = get_metadata(field_name)
    field_str = field_dic['standard_name'].replace('_', ' ')
    field_str = field_str[0].upper() + field_str[1:]
    field_str += ' ('+field_dic['units']+')'

    return field_str


def get_field_name(datatype):
    """
    Return long name of datatype.

    Parameters
    ----------
    datatype : str
        The data type

    Returns
    -------
    name : str
        The name

    """
    field_name = get_fieldname_pyart(datatype)
    field_dic = get_metadata(field_name)
    name = field_dic['long_name'].replace('_', ' ')
    name = name[0].upper() + name[1:]

    return name


def get_field_unit(datatype):
    """
    Return unit of datatype.

    Parameters
    ----------
    datatype : str
        The data type

    Returns
    -------
    unit : str
        The unit

    """
    field_name = get_fieldname_pyart(datatype)
    field_dic = get_metadata(field_name)

    return field_dic['units']


def get_datatype_metranet(datatype):
    """
    maps de config file radar data type name into the corresponding metranet
    data type  name and Py-ART field name

    Parameters
    ----------
    datatype : str
        config file radar data type name

    Returns
    -------
    metranet type : dict
        dictionary containing the metranet data type name and its
        corresponding Py-ART field name

    """
    if datatype == 'dBZ':
        datatype_metranet = 'ZH'
        field_name = 'reflectivity'
    elif datatype == 'dBZv':
        datatype_metranet = 'ZV'
        field_name = 'reflectivity_vv'
    elif datatype == 'ZDR':
        datatype_metranet = 'ZDR'
        field_name = 'differential_reflectivity'
    elif datatype == 'uRhoHV':
        datatype_metranet = 'RHO'
        field_name = 'uncorrected_cross_correlation_ratio'
    elif datatype == 'uPhiDP':
        datatype_metranet = 'PHI'
        field_name = 'uncorrected_differential_phase'
    elif datatype == 'V':
        datatype_metranet = 'VEL'
        field_name = 'velocity'
    elif datatype == 'W':
        datatype_metranet = 'WID'
        field_name = 'spectrum_width'
    elif datatype == 'CLT':
        datatype_metranet = 'CLT'
        field_name = 'clutter_exit_code'
    else:
        raise ValueError(
            'ERROR: Metranet fields do not contain datatype '+datatype)

    return {datatype_metranet: field_name}


def get_datatype_odim(datatype):
    """
    maps the config file radar data type name into the corresponding odim
    data type name and Py-ART field name

    Parameters
    ----------
    datatype : str
        config file radar data type name

    Returns
    -------
    metranet type : dict
        dictionary containing the odim data type name and its
        corresponding Py-ART field name

    """
    if datatype == 'dBZ':
        field_name = 'reflectivity'
        datatype_odim = 'DBZH'
    elif datatype == 'dBuZ':
        field_name = 'unfiltered_reflectivity'
        datatype_odim = 'TH'
    elif datatype == 'dBZc':
        field_name = 'corrected_reflectivity'
        datatype_odim = 'DBZHC'
    elif datatype == 'dBuZc':
        field_name = 'corrected_unfiltered_reflectivity'
        datatype_odim = 'THC'
    elif datatype == 'dBZv':
        field_name = 'reflectivity_vv'
        datatype_odim = 'DBZV'
    elif datatype == 'dBZvc':
        field_name = 'corrected_reflectivity_vv'
        datatype_odim = 'DBZVC'
    elif datatype == 'dBuZv':
        field_name = 'unfiltered_reflectivity_vv'
        datatype_odim = 'TV'
    elif datatype == 'dBuZvc':
        field_name = 'corrected_unfiltered_reflectivity_vv'
        datatype_odim = 'TVC'
    elif datatype == 'dBZ_bias':
        field_name = 'reflectivity_bias'
        datatype_odim = 'ZBIAS'
    elif datatype == 'eta_h':
        field_name = 'volumetric_reflectivity'
        datatype_odim = 'etah'
    elif datatype == 'eta_v':
        field_name = 'volumetric_reflectivity_vv'
        datatype_odim = 'etav'
    elif datatype == 'rcs_h':
        field_name = 'radar_cross_section_hh'
        datatype_odim = 'RCSH'
    elif datatype == 'rcs_v':
        field_name = 'radar_cross_section_vv'
        datatype_odim = 'RCSV'

    elif datatype == 'ZDR':
        field_name = 'differential_reflectivity'
        datatype_odim = 'ZDR'
    elif datatype == 'ZDRu':
        field_name = 'unfiltered_differential_reflectivity'
        datatype_odim = 'ZDRU'
    elif datatype == 'ZDRc':
        field_name = 'corrected_differential_reflectivity'
        datatype_odim = 'ZDRC'
    elif datatype == 'ZDRuc':
        field_name = 'corrected_unfiltered_differential_reflectivity'
        datatype_odim = 'ZDRUC'
    elif datatype == 'ZDR_prec':
        field_name = 'differential_reflectivity_in_precipitation'
        datatype_odim = 'ZDRPREC'
    elif datatype == 'ZDR_snow':
        field_name = 'differential_reflectivity_in_snow'
        datatype_odim = 'ZDRSNOW'

    elif datatype == 'dBm':
        field_name = 'signal_power_hh'
        datatype_odim = 'DBMH'
    elif datatype == 'dBmv':
        field_name = 'signal_power_vv'
        datatype_odim = 'DBMV'
    elif datatype == 'Nh':
        field_name = 'noisedBZ_hh'
        datatype_odim = 'NDBZH'
    elif datatype == 'Nv':
        field_name = 'noisedBZ_vv'
        datatype_odim = 'NDBZV'
    elif datatype == 'SNRh':
        field_name = 'signal_to_noise_ratio_hh'
        datatype_odim = 'SNRH'
    elif datatype == 'SNRv':
        field_name = 'signal_to_noise_ratio_vv'
        datatype_odim = 'SNRV'
    elif datatype == 'SQI':
        field_name = 'normalized_coherent_power'
        datatype_odim = 'SQIH'
    elif datatype == 'SQIv':
        field_name = 'normalized_coherent_power_vv'
        datatype_odim = 'SQIV'

    elif datatype == 'dBm_sun_hit':
        field_name = 'sun_hit_power_h'
        datatype_odim = 'DBM_SUNHIT'
    elif datatype == 'dBmv_sun_hit':
        field_name = 'sun_hit_power_v'
        datatype_odim = 'DBMV_SUNHIT'
    elif datatype == 'ZDR_sun_hit':
        field_name = 'sun_hit_differential_reflectivity'
        datatype_odim = 'ZDR_SUNHIT'
    elif datatype == 'dBm_sun_est':
        field_name = 'sun_est_power_h'
        datatype_odim = 'DBM_SUNEST'
    elif datatype == 'dBmv_sun_est':
        field_name = 'sun_est_power_v'
        datatype_odim = 'DBMV_SUNEST'
    elif datatype == 'ZDR_sun_est':
        field_name = 'sun_est_differential_reflectivity'
        datatype_odim = 'ZDR_SUNEST'
    elif datatype == 'sun_pos_h':
        field_name = 'sun_hit_h'
        datatype_odim = 'POSH_SUNHIT'
    elif datatype == 'sun_pos_v':
        field_name = 'sun_hit_v'
        datatype_odim = 'POSV_SUNHIT'
    elif datatype == 'sun_pos_zdr':
        field_name = 'sun_hit_zdr'
        datatype_odim = 'POSZDR_SUNHIT'

    elif datatype == 'RhoHV':
        field_name = 'cross_correlation_ratio'
        datatype_odim = 'RHOHV'
    elif datatype == 'uRhoHV':
        field_name = 'uncorrected_cross_correlation_ratio'
        datatype_odim = 'URHOHV'
    elif datatype == 'RhoHVc':
        field_name = 'corrected_cross_correlation_ratio'
        datatype_odim = 'RHOHVC'
    elif datatype == 'RhoHV_rain':
        field_name = 'cross_correlation_ratio_in_rain'
        datatype_odim = 'RHOHVRAIN'
    elif datatype == 'L':
        field_name = 'logarithmic_cross_correlation_ratio'
        datatype_odim = 'LRHOHV'
    elif datatype == 'CDR':
        field_name = 'circular_depolarization_ratio'
        datatype_odim = 'CDR'
    elif datatype == 'LDR':
        field_name = 'linear_polarization_ratio'
        datatype_odim = 'LDR'

    elif datatype == 'PhiDP':
        field_name = 'differential_phase'
        datatype_odim = 'PHIDP'
    elif datatype == 'uPhiDP':
        field_name = 'uncorrected_differential_phase'
        datatype_odim = 'UPHIDP'
    elif datatype == 'PhiDPc':
        field_name = 'corrected_differential_phase'
        datatype_odim = 'PHIDPC'
    elif datatype == 'PhiDP0':
        field_name = 'system_differential_phase'
        datatype_odim = 'PHIDP0'
    elif datatype == 'PhiDP0_bin':
        field_name = 'first_gate_differential_phase'
        datatype_odim = 'PHIDP0_BIN'
    elif datatype == 'KDP':
        field_name = 'specific_differential_phase'
        datatype_odim = 'KDP'
    elif datatype == 'KDPc':
        field_name = 'corrected_specific_differential_phase'
        datatype_odim = 'KDPC'

    elif datatype == 'V':
        field_name = 'velocity'
        datatype_odim = 'VRADH'
    elif datatype == 'Vh':
        field_name = 'velocity'
        datatype_odim = 'VRADH'
    elif datatype == 'dealV':
        field_name = 'dealiased_velocity'
        datatype_odim = 'VRADDH'
    elif datatype == 'Vc':
        field_name = 'corrected_velocity'
        datatype_odim = 'VRADHC'
    elif datatype == 'dealVc':
        field_name = 'dealiased_corrected_velocity'
        datatype_odim = 'VRADDHC'
    elif datatype == 'estV':
        field_name = 'retrieved_velocity'
        datatype_odim = 'VRADEST'
    elif datatype == 'stdV':
        field_name = 'retrieved_velocity_std'
        datatype_odim = 'sd_vvp'
    elif datatype == 'diffV':
        field_name = 'velocity_difference'
        datatype_odim = 'VDIFF'
    elif datatype == 'Vv':
        field_name = 'velocity_vv'
        datatype_odim = 'VRADV'
    elif datatype == 'dealVv':
        field_name = 'dealiased_velocity_vv'
        datatype_odim = 'VRADDV'
    elif datatype == 'W':
        field_name = 'spectrum_width'
        datatype_odim = 'WRADH'
    elif datatype == 'Wc':
        field_name = 'corrected_spectrum_width'
        datatype_odim = 'WRADHC'
    elif datatype == 'Wv':
        field_name = 'spectrum_width_vv'
        datatype_odim = 'WRADV'
    elif datatype == 'wind_vel_h_az':
        field_name = 'azimuthal_horizontal_wind_component'
        datatype_odim = 'AHWND'
    elif datatype == 'wind_vel_v':
        field_name = 'vertical_wind_component'
        datatype_odim = 'w'
    elif datatype == 'wind_vel_h_u':
        field_name = 'eastward_wind_component'
        datatype_odim = 'UWND'
    elif datatype == 'wind_vel_h_v':
        field_name = 'northward_wind_component'
        datatype_odim = 'VWND'
    elif datatype == 'windshear_v':
        field_name = 'vertical_wind_shear'
        datatype_odim = 'VSHR'
    elif datatype == 'WIND_SPEED':
        field_name = 'wind_speed'
        datatype_odim = 'ff'
    elif datatype == 'WIND_DIRECTION':
        field_name = 'wind_direction'
        datatype_odim = 'dd'

    elif datatype == 'Ah':
        field_name = 'specific_attenuation'
        datatype_odim = 'AH'
    elif datatype == 'Ahc':
        field_name = 'corrected_specific_attenuation'
        datatype_odim = 'AHC'
    elif datatype == 'PIA':
        field_name = 'path_integrated_attenuation'
        datatype_odim = 'PIA'
    elif datatype == 'PIAc':
        field_name = 'corrected_path_integrated_attenuation'
        datatype_odim = 'PIAC'
    elif datatype == 'Adp':
        field_name = 'specific_differential_attenuation'
        datatype_odim = 'ADP'
    elif datatype == 'Adpc':
        field_name = 'corrected_specific_differential_attenuation'
        datatype_odim = 'ADPC'
    elif datatype == 'PIDA':
        field_name = 'path_integrated_differential_attenuation'
        datatype_odim = 'PIDA'
    elif datatype == 'PIDAc':
        field_name = 'corrected_path_integrated_differential_attenuation'
        datatype_odim = 'PIDAC'

    elif datatype == 'TEMP':
        field_name = 'temperature'
        datatype_odim = 'TEMP'
    elif datatype == 'ISO0':
        field_name = 'iso0'
        datatype_odim = 'ISO0'
    elif datatype == 'H_ISO0':
        field_name = 'height_over_iso0'
        datatype_odim = 'HISO0'
    elif datatype == 'cosmo_index':
        field_name = 'cosmo_index'
        datatype_odim = 'COSMOIND'
    elif datatype == 'hzt_index':
        field_name = 'hzt_index'
        datatype_odim = 'HZTIND'
    elif datatype == 'ml':
        field_name = 'melting_layer'
        datatype_odim = 'ML'

    elif datatype == 'VIS':
        field_name = 'visibility'
        datatype_odim = 'VIS'

    elif datatype == 'echoID':
        field_name = 'radar_echo_id'
        datatype_odim = 'ECHOID'
    elif datatype == 'CLT':
        field_name = 'clutter_exit_code'
        datatype_odim = 'CLT'
    elif datatype == 'occurrence':
        field_name = 'occurrence'
        datatype_odim = 'OCC'
    elif datatype == 'freq_occu':
        field_name = 'frequency_of_occurrence'
        datatype_odim = 'OCCFREQ'
    elif datatype == 'RR':
        field_name = 'radar_estimated_rain_rate'
        datatype_odim = 'RATE'

    elif datatype == 'hydro':
        field_name = 'radar_echo_classification'
        datatype_odim = 'CLASS'
    elif datatype == 'entropy':
        field_name = 'hydroclass_entropy'
        datatype_odim = 'ENTROPY'
    elif datatype == 'propAG':
        field_name = 'proportion_AG'
        datatype_odim = 'propAG'
    elif datatype == 'propCR':
        field_name = 'proportion_CR'
        datatype_odim = 'propCR'
    elif datatype == 'propLR':
        field_name = 'proportion_LR'
        datatype_odim = 'propLR'
    elif datatype == 'propRP':
        field_name = 'proportion_RP'
        datatype_odim = 'propRP'
    elif datatype == 'propRN':
        field_name = 'proportion_RN'
        datatype_odim = 'propRN'
    elif datatype == 'propVI':
        field_name = 'proportion_VI'
        datatype_odim = 'propVI'
    elif datatype == 'propWS':
        field_name = 'proportion_WS'
        datatype_odim = 'propWS'
    elif datatype == 'propMH':
        field_name = 'proportion_MH'
        datatype_odim = 'propMH'
    elif datatype == 'propIH':
        field_name = 'proportion_IH'
        datatype_odim = 'propIH'

    elif datatype == 'time_avg_flag':
        field_name = 'time_avg_flag'
        datatype_odim = 'TAFLAG'
    elif datatype == 'colocated_gates':
        field_name = 'colocated_gates'
        datatype_odim = 'COLGATES'
    elif datatype == 'nsamples':
        field_name = 'number_of_samples'
        datatype_odim = 'ns'
    elif datatype == 'bird_density':
        field_name = 'bird_density'
        datatype_odim = 'dens'
    elif datatype == 'std':
        field_name = 'standard_deviation'
        datatype_odim = 'STD'
    elif datatype == 'sum':
        field_name = 'sum'
        datatype_odim = 'SUM'
    elif datatype == 'sum2':
        field_name = 'sum_squared'
        datatype_odim = 'SUM2'

    # vol2bird field names
    elif datatype == 'ff':
        field_name = 'wind_speed'
        datatype_odim = 'ff'
    elif datatype == 'dd':
        field_name = 'wind_direction'
        datatype_odim = 'dd'
    elif datatype == 'u':
        field_name = 'eastward_wind_component'
        datatype_odim = 'UWND'
    elif datatype == 'v':
        field_name = 'northward_wind_component'
        datatype_odim = 'VWND'
    elif datatype == 'w':
        field_name = 'vertical_wind_component'
        datatype_odim = 'w'
    elif datatype == 'width':
        field_name = 'height_resolution'
        datatype_odim = 'width'
    elif datatype == 'gap':
        field_name = 'gap'
        datatype_odim = 'gap'
    elif datatype == 'dbz':
        field_name = 'bird_reflectivity'
        datatype_odim = 'eta'
    elif datatype == 'eta':
        field_name = 'volumetric_reflectivity'
        datatype_odim = 'etah'
    elif datatype == 'dens':
        field_name = 'bird_density'
        datatype_odim = 'dens'
    elif datatype == 'n':
        field_name = 'number_of_samples_velocity'
        datatype_odim = 'n'
    elif datatype == 'n_dbz':
        field_name = 'number_of_samples_reflectivity'
        datatype_odim = 'n_dbz'
    elif datatype == 'sd_vvp':
        field_name = 'retrieved_velocity_std'
        datatype_odim = 'sd_vvp'
    elif datatype == 'DBZH':
        field_name = 'reflectivity'
        datatype_odim = 'DBZH'
    elif datatype == 'n_all':
        field_name = 'number_of_samples_velocity_all'
        datatype_odim = 'n_all'
    elif datatype == 'n_dbz_all':
        field_name = 'number_of_samples_reflectivity_all'
        datatype_odim = 'n_dbz_all'
    else:
        raise ValueError(
            'ERROR: ODIM fields do not contain datatype '+datatype)

    return {datatype_odim: field_name}


def get_fieldname_pyart(datatype):
    """
    maps the config file radar data type name into the corresponding rainbow
    Py-ART field name

    Parameters
    ----------
    datatype : str
        config file radar data type name

    Returns
    -------
    field_name : str
        Py-ART field name

    """
    if datatype == 'dBZ':
        field_name = 'reflectivity'
    elif datatype == 'dBuZ':
        field_name = 'unfiltered_reflectivity'
    elif datatype == 'dBZc':
        field_name = 'corrected_reflectivity'
    elif datatype == 'dBuZc':
        field_name = 'corrected_unfiltered_reflectivity'
    elif datatype == 'dBZv':
        field_name = 'reflectivity_vv'
    elif datatype == 'dBZvc':
        field_name = 'corrected_reflectivity_vv'
    elif datatype == 'dBuZv':
        field_name = 'unfiltered_reflectivity_vv'
    elif datatype == 'dBuZvc':
        field_name = 'corrected_unfiltered_reflectivity_vv'
    elif datatype == 'dBZ_bias':
        field_name = 'reflectivity_bias'
    elif datatype == 'eta_h':
        field_name = 'volumetric_reflectivity'
    elif datatype == 'eta_v':
        field_name = 'volumetric_reflectivity_vv'
    elif datatype == 'rcs_h':
        field_name = 'radar_cross_section_hh'
    elif datatype == 'rcs_v':
        field_name = 'radar_cross_section_vv'

    elif datatype == 'ZDR':
        field_name = 'differential_reflectivity'
    elif datatype == 'ZDRu':
        field_name = 'unfiltered_differential_reflectivity'
    elif datatype == 'ZDRc':
        field_name = 'corrected_differential_reflectivity'
    elif datatype == 'ZDRuc':
        field_name = 'corrected_unfiltered_differential_reflectivity'
    elif datatype == 'ZDR_prec':
        field_name = 'differential_reflectivity_in_precipitation'
    elif datatype == 'ZDR_snow':
        field_name = 'differential_reflectivity_in_snow'
    elif datatype == 'ZDR_col':
        field_name = 'differential_reflectivity_column_height'

    elif datatype == 'dBm':
        field_name = 'signal_power_hh'
    elif datatype == 'dBmv':
        field_name = 'signal_power_vv'

    elif datatype == 'Nh':
        field_name = 'noisedBZ_hh'
    elif datatype == 'Nv':
        field_name = 'noisedBZ_vv'
    elif datatype == 'NdBADUh':
        field_name = 'noisedBADU_hh'
    elif datatype == 'NdBADUv':
        field_name = 'noisedBADU_vv'
    elif datatype == 'NdBmh':
        field_name = 'noisedBm_hh'
    elif datatype == 'NdBmv':
        field_name = 'noisedBm_vv'
    elif datatype == 'NADUh':
        field_name = 'noiseADU_hh'
    elif datatype == 'NADUv':
        field_name = 'noiseADU_vv'

    elif datatype == 'TXh':
        field_name = 'transmitted_signal_power_h'
    elif datatype == 'TXv':
        field_name = 'transmitted_signal_power_v'

    elif datatype == 'SNRh':
        field_name = 'signal_to_noise_ratio_hh'
    elif datatype == 'SNRv':
        field_name = 'signal_to_noise_ratio_vv'

    # spectral data
    elif datatype == 'ShhADU':
        field_name = 'complex_spectra_hh_ADU'
    elif datatype == 'SvvADU':
        field_name = 'complex_spectra_vv_ADU'
    elif datatype == 'sPhhADU':
        field_name = 'spectral_power_hh_ADU'
    elif datatype == 'sPvvADU':
        field_name = 'spectral_power_vv_ADU'
    elif datatype == 'sPhhdBADU':
        field_name = 'spectral_power_hh_dBADU'
    elif datatype == 'sPvvdBADU':
        field_name = 'spectral_power_vv_dBADU'
    elif datatype == 'sPhhdBm':
        field_name = 'spectral_power_hh_dBm'
    elif datatype == 'sPvvdBm':
        field_name = 'spectral_power_vv_dBm'
    elif datatype == 'sPhasehh':
        field_name = 'spectral_phase_hh'
    elif datatype == 'sPhasevv':
        field_name = 'spectral_phase_vv'

    elif datatype == 'sdBZ':
        field_name = 'spectral_reflectivity_hh'
    elif datatype == 'sdBZv':
        field_name = 'spectral_reflectivity_vv'
    elif datatype == 'sZDR':
        field_name = 'spectral_differential_reflectivity'
    elif datatype == 'sPhiDP':
        field_name = 'spectral_differential_phase'
    elif datatype == 'sRhoHV':
        field_name = 'spectral_copolar_correlation_coefficient'

    elif datatype == 'dBm_sun_hit':
        field_name = 'sun_hit_power_h'
    elif datatype == 'dBmv_sun_hit':
        field_name = 'sun_hit_power_v'
    elif datatype == 'ZDR_sun_hit':
        field_name = 'sun_hit_differential_reflectivity'
    elif datatype == 'dBm_sun_est':
        field_name = 'sun_est_power_h'
    elif datatype == 'dBmv_sun_est':
        field_name = 'sun_est_power_v'
    elif datatype == 'ZDR_sun_est':
        field_name = 'sun_est_differential_reflectivity'
    elif datatype == 'sun_pos_h':
        field_name = 'sun_hit_h'
    elif datatype == 'sun_pos_v':
        field_name = 'sun_hit_v'
    elif datatype == 'sun_pos_zdr':
        field_name = 'sun_hit_zdr'

    elif datatype == 'RhoHV':
        field_name = 'cross_correlation_ratio'
    elif datatype == 'RhoHVu':
        field_name = 'unfiltered_cross_correlation_ratio'
    elif datatype == 'uRhoHV':
        field_name = 'uncorrected_cross_correlation_ratio'
    elif datatype == 'RhoHVc':
        field_name = 'corrected_cross_correlation_ratio'
    elif datatype == 'RhoHV_rain':
        field_name = 'cross_correlation_ratio_in_rain'
    elif datatype == 'L':
        field_name = 'logarithmic_cross_correlation_ratio'
    elif datatype == 'CDR':
        field_name = 'circular_depolarization_ratio'

    elif datatype == 'PhiDP':
        field_name = 'differential_phase'
    elif datatype == 'uPhiDPu':
        field_name = 'uncorrected_unfiltered_differential_phase'
    elif datatype == 'uPhiDP':
        field_name = 'uncorrected_differential_phase'
    elif datatype == 'PhiDPc':
        field_name = 'corrected_differential_phase'
    elif datatype == 'PhiDP0':
        field_name = 'system_differential_phase'
    elif datatype == 'PhiDP0_bin':
        field_name = 'first_gate_differential_phase'
    elif datatype == 'KDP':
        field_name = 'specific_differential_phase'
    elif datatype == 'KDPc':
        field_name = 'corrected_specific_differential_phase'

    elif datatype == 'V':
        field_name = 'velocity'
    elif datatype == 'Vu':
        field_name = 'unfiltered_velocity'
    elif datatype == 'dealV':
        field_name = 'dealiased_velocity'
    elif datatype == 'Vc':
        field_name = 'corrected_velocity'
    elif datatype == 'dealVc':
        field_name = 'dealiased_corrected_velocity'
    elif datatype == 'estV':
        field_name = 'retrieved_velocity'
    elif datatype == 'stdV':
        field_name = 'retrieved_velocity_std'
    elif datatype == 'diffV':
        field_name = 'velocity_difference'
    elif datatype == 'W':
        field_name = 'spectrum_width'
    elif datatype == 'Wu':
        field_name = 'unfiltered_spectrum_width'
    elif datatype == 'Wc':
        field_name = 'corrected_spectrum_width'
    elif datatype == 'wind_vel_h_az':
        field_name = 'azimuthal_horizontal_wind_component'
    elif datatype == 'wind_vel_v':
        field_name = 'vertical_wind_component'
    elif datatype == 'wind_vel_h_u':
        field_name = 'eastward_wind_component'
    elif datatype == 'wind_vel_h_v':
        field_name = 'northward_wind_component'
    elif datatype == 'windshear_v':
        field_name = 'vertical_wind_shear'
    elif datatype == 'WIND_SPEED':
        field_name = 'wind_speed'
    elif datatype == 'WIND_DIRECTION':
        field_name = 'wind_direction'

    elif datatype == 'Ah':
        field_name = 'specific_attenuation'
    elif datatype == 'Ahc':
        field_name = 'corrected_specific_attenuation'
    elif datatype == 'PIA':
        field_name = 'path_integrated_attenuation'
    elif datatype == 'PIAc':
        field_name = 'corrected_path_integrated_attenuation'
    elif datatype == 'Adp':
        field_name = 'specific_differential_attenuation'
    elif datatype == 'Adpc':
        field_name = 'corrected_specific_differential_attenuation'
    elif datatype == 'PIDA':
        field_name = 'path_integrated_differential_attenuation'
    elif datatype == 'PIDAc':
        field_name = 'corrected_path_integrated_differential_attenuation'

    elif datatype == 'TEMP':
        field_name = 'temperature'
    elif datatype == 'ISO0':
        field_name = 'iso0'
    elif datatype == 'H_ISO0':
        field_name = 'height_over_iso0'
    elif datatype == 'HZT':
        field_name = 'iso0_height'
    elif datatype == 'cosmo_index':
        field_name = 'cosmo_index'
    elif datatype == 'hzt_index':
        field_name = 'hzt_index'
    elif datatype == 'ml':
        field_name = 'melting_layer'

    elif datatype == 'VIS':
        field_name = 'visibility'
    elif datatype == 'minvisel':
        field_name = 'minimum_visible_elevation'
    elif datatype == 'minvisalt':
        field_name = 'minimum_visible_altitude'

    elif datatype == 'echoID':
        field_name = 'radar_echo_id'
    elif datatype == 'CLT':
        field_name = 'clutter_exit_code'
    elif datatype == 'occurrence':
        field_name = 'occurrence'
    elif datatype == 'freq_occu':
        field_name = 'frequency_of_occurrence'
    elif datatype == 'RR':
        field_name = 'radar_estimated_rain_rate'
    elif datatype == 'RRc':
        field_name = 'corrected_radar_estimated_rain_rate'
    elif datatype == 'Raccu':
        field_name = 'rainfall_accumulation'

    elif datatype == 'hydro':
        field_name = 'radar_echo_classification'
    elif datatype == 'hydroc':
        field_name = 'corrected_radar_echo_classification'
    elif datatype == 'entropy':
        field_name = 'hydroclass_entropy'
    elif datatype == 'propAG':
        field_name = 'proportion_AG'
    elif datatype == 'propCR':
        field_name = 'proportion_CR'
    elif datatype == 'propLR':
        field_name = 'proportion_LR'
    elif datatype == 'propRP':
        field_name = 'proportion_RP'
    elif datatype == 'propRN':
        field_name = 'proportion_RN'
    elif datatype == 'propVI':
        field_name = 'proportion_VI'
    elif datatype == 'propWS':
        field_name = 'proportion_WS'
    elif datatype == 'propMH':
        field_name = 'proportion_MH'
    elif datatype == 'propIH':
        field_name = 'proportion_IH'

    elif datatype == 'time_avg_flag':
        field_name = 'time_avg_flag'
    elif datatype == 'colocated_gates':
        field_name = 'colocated_gates'
    elif datatype == 'nsamples':
        field_name = 'number_of_samples'
    elif datatype == 'bird_density':
        field_name = 'bird_density'
    elif datatype == 'std':
        field_name = 'standard_deviation'
    elif datatype == 'sum':
        field_name = 'sum'
    elif datatype == 'sum2':
        field_name = 'sum_squared'

    elif datatype == 'POH':
        field_name = 'probability_of_hail'
    elif datatype == 'VIL':
        field_name = 'vertically_integrated_liquid'
    elif datatype == 'ETOP15':
        field_name = 'echo_top_15dBZ'
    elif datatype == 'ETOP20':
        field_name = 'echo_top_20dBZ'
    elif datatype == 'ETOP45':
        field_name = 'echo_top_45dBZ'
    elif datatype == 'ETOP50':
        field_name = 'echo_top_50dBZ'
    elif datatype == 'MAXECHO':
        field_name = 'maximum_echo'
    elif datatype == 'HMAXECHO':
        field_name = 'maximum_echo_height'

    # rad4alp cartesian products
    # rainfall accumulation products
    elif datatype == 'AZC01':
        field_name = 'rainfall_accumulation'
    elif datatype == 'AZC03':
        field_name = 'rainfall_accumulation'
    elif datatype == 'AZC06':
        field_name = 'rainfall_accumulation'
    elif datatype == 'aZC01':
        field_name = 'rainfall_accumulation'
    elif datatype == 'aZC03':
        field_name = 'rainfall_accumulation'
    elif datatype == 'aZC06':
        field_name = 'rainfall_accumulation'

    # CPC
    elif datatype == 'CPC0005':
        field_name = 'radar_estimated_rain_rate'
    elif datatype == 'CPC0060':
        field_name = 'rainfall_accumulation'
    elif datatype == 'CPC0180':
        field_name = 'rainfall_accumulation'
    elif datatype == 'CPC0360':
        field_name = 'rainfall_accumulation'
    elif datatype == 'CPC0720':
        field_name = 'rainfall_accumulation'
    elif datatype == 'CPC1440':
        field_name = 'rainfall_accumulation'
    elif datatype == 'CPC2880':
        field_name = 'rainfall_accumulation'
    elif datatype == 'CPC4320':
        field_name = 'rainfall_accumulation'

    elif datatype == 'CPCH0005':
        field_name = 'radar_estimated_rain_rate'
    elif datatype == 'CPCH0060':
        field_name = 'rainfall_accumulation'
    elif datatype == 'CPCH0180':
        field_name = 'rainfall_accumulation'
    elif datatype == 'CPCH0360':
        field_name = 'rainfall_accumulation'
    elif datatype == 'CPCH0720':
        field_name = 'rainfall_accumulation'
    elif datatype == 'CPCH1440':
        field_name = 'rainfall_accumulation'
    elif datatype == 'CPCH2880':
        field_name = 'rainfall_accumulation'
    elif datatype == 'CPCH4320':
        field_name = 'rainfall_accumulation'

    # Nowpal
    elif datatype == 'nowpal60_P60':
        field_name = 'rainfall_accumulation'
    elif datatype == 'nowpal90_P90':
        field_name = 'rainfall_accumulation'
    elif datatype == 'nowpal180_P180':
        field_name = 'rainfall_accumulation'
    elif datatype == 'nowpal360_P360':
        field_name = 'rainfall_accumulation'
    elif datatype == 'nowpal720_P720':
        field_name = 'rainfall_accumulation'

    elif datatype == 'nowpal90_P30':
        field_name = 'rainfall_accumulation'
    elif datatype == 'nowpal90_P30_F60':
        field_name = 'rainfall_accumulation'
    elif datatype == 'nowpal90_F60':
        field_name = 'rainfall_accumulation'
    elif datatype == 'nowpal180_P60':
        field_name = 'rainfall_accumulation'
    elif datatype == 'nowpal180_P60_F120':
        field_name = 'rainfall_accumulation'
    elif datatype == 'nowpal180_F120':
        field_name = 'rainfall_accumulation'
    elif datatype == 'nowpal360_P120':
        field_name = 'rainfall_accumulation'
    elif datatype == 'nowpal360_P120_F240':
        field_name = 'rainfall_accumulation'
    elif datatype == 'nowpal360_F240':
        field_name = 'rainfall_accumulation'
    elif datatype == 'nowpal720_P360':
        field_name = 'rainfall_accumulation'
    elif datatype == 'nowpal720_P360_F360':
        field_name = 'rainfall_accumulation'
    elif datatype == 'nowpal720_F360':
        field_name = 'rainfall_accumulation'

    elif datatype == 'dACC':
        field_name = 'rainfall_accumulation'
    elif datatype == 'dACCH':
        field_name = 'rainfall_accumulation'
    elif datatype == 'dARC':
        field_name = 'rainfall_accumulation'

    # rainfall rate products
    elif datatype == 'RZC':
        field_name = 'radar_estimated_rain_rate'
    elif datatype == 'R1F':
        field_name = 'radar_estimated_rain_rate'
    elif datatype == 'rZC':
        field_name = 'radar_estimated_rain_rate'
    elif datatype == 'RZF':
        field_name = 'radar_estimated_rain_rate'
    elif datatype == 'dRZC':
        field_name = 'radar_estimated_rain_rate'

    # hail products
    elif datatype == 'BZC':
        field_name = 'probability_of_hail'
    elif datatype == 'dBZC':
        field_name = 'probability_of_hail'
    elif datatype == 'MZC':
        field_name = 'maximum_expected_severe_hail_size'
    elif datatype == 'dMZC':
        field_name = 'maximum_expected_severe_hail_size'
    elif datatype == 'GZC':
        field_name = 'probability_of_hail'
    elif datatype == 'dGZC':
        field_name = 'probability_of_hail'

    # echo tops
    elif datatype == 'CZC':
        field_name = 'maximum_echo'
    elif datatype == 'dCZC':
        field_name = 'maximum_echo' # Daily max echo
    elif datatype == 'HZC':
        field_name = 'maximum_echo_height' # Max echo height
    elif datatype == 'EZC15':
        field_name = 'echo_top_15dBz'
    elif datatype == 'EZC20':
        field_name = 'echo_top_20dBz'
    elif datatype == 'EZC45':
        field_name = 'echo_top_45dBz'
    elif datatype == 'EZC50':
        field_name = 'echo_top_50dBz'
    elif datatype == 'dEZC15':
        field_name = 'echo_top_15dBZ' # Daily echo top
    elif datatype == 'dEZC20':
        field_name = 'echo_top_20dBz'
    elif datatype == 'dEZC45':
        field_name = 'echo_top_45dBz'
    elif datatype == 'dEZC50':
        field_name = 'echo_top_50dBz'
    elif datatype == 'LZC':
        field_name = 'vertically_integrated_liquid'
    elif datatype == 'dLZC':
        field_name = 'vertically_integrated_liquid'

    # reflectivity CAPPI
    elif datatype == 'OZC01':
        field_name = 'reflectivity'
    elif datatype == 'OZC02':
        field_name = 'reflectivity'
    elif datatype == 'OZC03':
        field_name = 'reflectivity'
    elif datatype == 'OZC04':
        field_name = 'reflectivity'
    elif datatype == 'OZC05':
        field_name = 'reflectivity'
    elif datatype == 'OZC06':
        field_name = 'reflectivity'
    elif datatype == 'OZC07':
        field_name = 'reflectivity'
    elif datatype == 'OZC08':
        field_name = 'reflectivity'
    elif datatype == 'OZC09':
        field_name = 'reflectivity'
    elif datatype == 'OZC10':
        field_name = 'reflectivity'
    elif datatype == 'OZC11':
        field_name = 'reflectivity'
    elif datatype == 'OZC12':
        field_name = 'reflectivity'
    elif datatype == 'OZC13':
        field_name = 'reflectivity'
    elif datatype == 'OZC14':
        field_name = 'reflectivity'
    elif datatype == 'OZC15':
        field_name = 'reflectivity'
    elif datatype == 'OZC16':
        field_name = 'reflectivity'
    elif datatype == 'OZC17':
        field_name = 'reflectivity'
    elif datatype == 'OZC18':
        field_name = 'reflectivity'

    # vol2bird field names
    elif datatype == 'ff':
        field_name = 'wind_speed'
    elif datatype == 'dd':
        field_name = 'wind_direction'
    elif datatype == 'u':
        field_name = 'eastward_wind_component'
    elif datatype == 'v':
        field_name = 'northward_wind_component'
    elif datatype == 'w':
        field_name = 'vertical_wind_component'
    elif datatype == 'width':
        field_name = 'height_resolution'
    elif datatype == 'gap':
        field_name = 'gap'
    elif datatype == 'dbz':
        field_name = 'bird_reflectivity'
    elif datatype == 'eta':
        field_name = 'volumetric_reflectivity'
    elif datatype == 'dens':
        field_name = 'bird_density'
    elif datatype == 'n':
        field_name = 'number_of_samples_velocity'
    elif datatype == 'n_dbz':
        field_name = 'number_of_samples_reflectivity'
    elif datatype == 'sd_vvp':
        field_name = 'retrieved_velocity_std'
    elif datatype == 'DBZH':
        field_name = 'reflectivity'
    elif datatype == 'n_all':
        field_name = 'number_of_samples_velocity_all'
    elif datatype == 'n_dbz_all':
        field_name = 'number_of_samples_reflectivity_all'
    else:
        raise ValueError('ERROR: Unknown data type '+datatype)

    return field_name


def get_fieldname_cosmo(field_name):
    """
    maps the Py-ART field name into the corresponding COSMO variable name

    Parameters
    ----------
    field_name : str
        Py-ART field name

    Returns
    -------
    cosmo_name : str
        Py-ART variable name

    """
    if field_name == 'temperature':
        cosmo_name = 'T'
    elif field_name == 'wind_speed':
        cosmo_name = 'FF'
    elif field_name == 'wind_direction':
        cosmo_name = 'DD'
    elif field_name == 'vertical_wind_shear':
        cosmo_name = 'WSHEAR'
    else:
        raise ValueError('ERROR: Unknown field name '+field_name)

    return cosmo_name


def get_file_list(datadescriptor, starttimes, endtimes, cfg, scan=None):
    """
    gets the list of files with a time period

    Parameters
    ----------
    datadescriptor : str
        radar field type. Format : [radar file type]:[datatype]
    startimes : array of datetime objects
        start of time periods
    endtimes : array of datetime object
        end of time periods
    cfg: dictionary of dictionaries
        configuration info to figure out where the data is
    scan : str
        scan name

    Returns
    -------
    filelist : list of strings
        list of files within the time period

    """
    radarnr, datagroup, datatype, dataset, product = get_datatype_fields(
        datadescriptor)
    ind_rad = int(radarnr[5:8])-1

    if datatype in ('Nh', 'Nv'):
        datatype = 'dBZ'

    filelist = []
    for starttime, endtime in zip(starttimes, endtimes):
        startdate = starttime.replace(
            hour=0, minute=0, second=0, microsecond=0)
        enddate = endtime.replace(hour=0, minute=0, second=0, microsecond=0)
        ndays = int((enddate-startdate).days)+1
        t_filelist = []
        for i in range(ndays):
            if datagroup == 'RAINBOW':
                if scan is None:
                    warn('Unknown scan name')
                    return None
                daydir = (
                    starttime+datetime.timedelta(days=i)).strftime('%Y-%m-%d')
                dayinfo = (starttime+datetime.timedelta(days=i)).strftime(
                    '%Y%m%d')
                datapath = cfg['datapath'][ind_rad] + scan + daydir + '/'
                if not os.path.isdir(datapath):
                    # warn("WARNING: Unknown datapath '%s'" % datapath)
                    continue
                dayfilelist = glob.glob(datapath+dayinfo+'*00'+datatype+'.*')
                for filename in dayfilelist:
                    t_filelist.append(filename)
            elif datagroup == 'RAD4ALP':
                if scan is None:
                    warn('Unknown scan name')
                    return None

                datapath, basename = get_rad4alp_dir(
                    cfg['datapath'][ind_rad],
                    starttime+datetime.timedelta(days=i),
                    radar_name=cfg['RadarName'][ind_rad],
                    radar_res=cfg['RadarRes'][ind_rad], scan=scan,
                    path_convention=cfg['path_convention'])

                if not os.path.isdir(datapath):
                    warn("WARNING: Unknown datapath '%s'" % datapath)
                    continue
                dayfilelist = glob.glob(datapath+basename+'*.'+scan+'*')
                for filename in dayfilelist:
                    t_filelist.append(filename)
            elif datagroup in('RAD4ALPGRID', 'RAD4ALPGIF', 'RAD4ALPBIN'):
                acronym, termination = get_rad4alp_prod_fname(datatype)
                dir_day = starttime+datetime.timedelta(days=i)
                dayinfo = dir_day.strftime('%y%j')
                basename = acronym+dayinfo

                datapath = get_rad4alp_grid_dir(
                    cfg['datapath'][ind_rad], dir_day, datatype, acronym,
                    path_convention=cfg['path_convention'])

                if not os.path.isdir(datapath):
                    warn("WARNING: Unknown datapath '%s'" % datapath)
                    continue

                dayfilelist = glob.glob(datapath+basename+'*'+termination)
                for filename in dayfilelist:
                    t_filelist.append(filename)

            elif datagroup == 'ODIM':
                if scan is None:
                    warn('Unknown scan name')
                    return None
                if cfg['path_convention'] == 'MCH':
                    dayinfo = (starttime+datetime.timedelta(days=i)).strftime(
                        '%y%j')
                    basename = ('M'+cfg['RadarRes'][ind_rad] +
                                cfg['RadarName'][ind_rad]+dayinfo)
                    datapath = (
                        cfg['datapath'][ind_rad]+dayinfo+'/'+basename+'/')

                    # check that M files exist. if not search P files
                    dayfilelist = glob.glob(datapath+basename+'*'+scan+'*')
                    if not dayfilelist:
                        basename = ('P'+cfg['RadarRes'][ind_rad] +
                                    cfg['RadarName'][ind_rad]+dayinfo)
                        datapath = (cfg['datapath'][ind_rad]+dayinfo+'/' +
                                    basename+'/')
                elif cfg['path_convention'] == 'ODIM':
                    try:
                        fpath_strf = dataset[
                            dataset.find("D")+2:dataset.find("F")-2]
                    except AttributeError:
                        warn('Unknown ODIM directory and/or date ' +
                             'convention, check product config file')
                    daydir = (
                        starttime+datetime.timedelta(days=i)).strftime(
                            fpath_strf)
                    datapath = (cfg['datapath'][ind_rad] + daydir+'/')
                    dayfilelist = glob.glob(datapath+'*'+scan+'*.h5')
                else:
                    dayinfo = (starttime+datetime.timedelta(days=i)).strftime(
                        '%y%j')
                    basename = ('M'+cfg['RadarRes'][ind_rad] +
                                cfg['RadarName'][ind_rad]+dayinfo)
                    datapath = (
                        cfg['datapath'][ind_rad]+'M' +
                        cfg['RadarRes'][ind_rad]+cfg['RadarName'][ind_rad] +
                        '/')

                    # check that M files exist. if not search P files
                    dayfilelist = glob.glob(datapath+basename+'*'+scan+'*')
                    if not dayfilelist:
                        basename = ('P'+cfg['RadarRes'][ind_rad] +
                                    cfg['RadarName'][ind_rad]+dayinfo)
                        datapath = (
                            cfg['datapath'][ind_rad]+'P' +
                            cfg['RadarRes'][ind_rad] +
                            cfg['RadarName'][ind_rad]+'/')

                if not os.path.isdir(datapath):
                    warn("WARNING: Unknown datapath '%s'" % datapath)
                    continue
                for filename in dayfilelist:
                    t_filelist.append(filename)
            elif datagroup in ('CFRADIAL', 'ODIMPYRAD', 'PYRADGRID'):
                termination = '.nc'
                if datagroup == 'ODIMPYRAD':
                    termination = '.h5'

                daydir = (
                    starttime+datetime.timedelta(days=i)).strftime(
                        '%Y-%m-%d')
                dayinfo = (starttime+datetime.timedelta(days=i)).strftime(
                    '%Y%m%d')
                datapath = (
                    cfg['loadbasepath'][ind_rad]+cfg['loadname'][ind_rad] +
                    '/'+daydir+'/'+dataset+'/'+product+'/')
                if not os.path.isdir(datapath):
                    warn("WARNING: Unknown datapath '%s'" % datapath)
                    continue
                dayfilelist = glob.glob(
                    datapath+dayinfo+'*'+datatype+termination)
                for filename in dayfilelist:
                    t_filelist.append(filename)
            elif datagroup == 'MXPOL':
                if scan is None:
                    warn('Unknown scan name')
                    return None
                if cfg['path_convention'] == 'LTE':
                    sub1 = str(starttime.year)
                    sub2 = starttime.strftime('%m')
                    sub3 = starttime.strftime('%d')
                    datapath = (
                        cfg['datapath'][ind_rad]+'/'+sub1+'/'+sub2 +'/'+sub3 +
                        '/')
                    basename = (
                        'MXPol-polar-'+starttime.strftime('%Y%m%d')+'-*-' +
                        scan+'*')
                    dayfilelist = glob.glob(datapath+basename)
                else:
                    daydir = (
                        starttime+datetime.timedelta(days=i)).strftime(
                            '%Y-%m-%d')
                    dayinfo = (
                        starttime+datetime.timedelta(days=i)).strftime(
                            '%Y%m%d')
                    datapath = cfg['datapath'][ind_rad]+scan+'/'+daydir+'/'
                    if not os.path.isdir(datapath):
                        warn("WARNING: Unknown datapath '%s'" % datapath)
                        continue
                    dayfilelist = glob.glob(
                        datapath+'MXPol-polar-'+dayinfo+'-*-'+scan+'.nc')
                for filename in dayfilelist:
                    t_filelist.append(filename)

        for filename in t_filelist:
            filenamestr = str(filename)
            fdatetime = get_datetime(filenamestr, datadescriptor)
            if fdatetime is not None:
                if starttime <= fdatetime <= endtime:
                    filelist.append(filenamestr)

    return sorted(filelist)


def get_rad4alp_dir(basepath, voltime, radar_name='A', radar_res='L',
                    scan='001', path_convention='MCH'):
    """
    gets the directory where rad4alp data is stored

    Parameters
    ----------
    basepath : str
        base path
    voltime : datetime object
        nominal time
    radar_name : str
        radar name (A, D, L, P, W)
    radar_res : str
        radar resolution (H, L)
    scan : str
        scan
    path_convention : str
        The path convention. Can be 'LTE', 'MCH' or 'RT'

    Returns
    -------
    datapath : str
        The data path
    basename : str
        The base name. ex: PHA17213

    """
    dayinfo = voltime.strftime('%y%j')
    basename = 'M'+radar_res+radar_name+dayinfo
    if path_convention == 'LTE':
        yy = dayinfo[0:2]
        dy = dayinfo[2:]
        subf = 'M'+radar_res+radar_name+yy+'hdf'+dy
        datapath = basepath+subf+'/'

        # check that M files exist. if not search P files
        dayfilelist = glob.glob(datapath+basename+'*.'+scan+'*')
        if not dayfilelist:
            subf = 'P'+radar_res+radar_name+yy+'hdf'+dy
            datapath = basepath+subf+'/'
            basename = 'P'+radar_res+radar_name+dayinfo
    elif path_convention == 'MCH':
        datapath = basepath+dayinfo+'/'+basename+'/'

        # check that M files exist. if not search P files
        dayfilelist = glob.glob(datapath+basename+'*.'+scan+'*')
        if not dayfilelist:
            basename = 'P'+radar_res+radar_name+dayinfo
            datapath = basepath+dayinfo+'/'+basename+'/'
    else:
        datapath = basepath+'M'+radar_res+radar_name+'/'

        # check that M files exist. if not search P files
        dayfilelist = glob.glob(datapath+basename+'*.'+scan+'*')
        if not dayfilelist:
            basename = 'P'+radar_res+radar_name+dayinfo
            datapath = basepath+'P'+radar_res+radar_name+'/'

    return datapath, basename


def get_rad4alp_grid_dir(basepath, voltime, datatype, acronym,
                         path_convention='MCH'):
    """
    gets the directory where rad4alp grid data is stored

    Parameters
    ----------
    basepath : str
        base path
    voltime : datetime object
        nominal time
    datatype : str
        data type
    acronym : str
        acronym identifying the data type
    path_convention : str
        The path convention. Can be 'LTE', 'MCH' or 'RT'

    Returns
    -------
    datapath : str
        The data path

    """
    nowpal_accu = (
        'nowpal60_P60', 'nowpal90_P90', 'nowpal180_P180', 'nowpal360_P360',
        'nowpal720_P720')
    nowpal = (
        'nowpal90_P30', 'nowpal90_P30_F60', 'nowpal90_F60',
        'nowpal180_P60', 'nowpal180_P60_F120', 'nowpal180_F120',
        'nowpal360_P120', 'nowpal360_P120_F240', 'nowpal360_F240',
        'nowpal720_P360', 'nowpal720_P360_F360', 'nowpal720_F360')

    cpch = (
        'CPCH0005', 'CPCH0060', 'CPCH0180', 'CPCH0360', 'CPCH0720',
        'CPCH1440', 'CPCH2880', 'CPCH4320')

    dayinfo = voltime.strftime('%y%j')
    if datatype in nowpal_accu:
        dirbase = 'nowpal_accu'
    elif datatype in nowpal:
        dirbase = 'nowpal'
    elif datatype.startswith('d') and datatype != 'dGZC':
        dirbase = 'd'+acronym
        if datatype.endswith('H'):
            dirbase = dirbase+'H'
    elif datatype in cpch:
        dirbase = acronym+'H'
    else:
        dirbase = acronym

    if path_convention == 'LTE':
        yy = dayinfo[0:2]
        dy = dayinfo[2:]
        subf = acronym+yy+'hdf'+ dy
        datapath = basepath+subf+'/'
    elif path_convention == 'MCH':
        datapath = basepath+dayinfo+'/'+dirbase+dayinfo+'/'
    else:
        datapath = basepath+dirbase+'/'

    return datapath


def get_trtfile_list(basepath, starttime, endtime):
    """
    gets the list of TRT files with a time period

    Parameters
    ----------
    datapath : str
        directory where to look for data
    startime : datetime object
        start of time period
    endtime : datetime object
        end of time period

    Returns
    -------
    filelist : list of strings
        list of files within the time period

    """
    startdate = starttime.date()
    enddate = endtime.date()
    ndays = int((enddate-startdate).days)+1

    t_filelist = []
    for i in range(ndays):
        daydir = (startdate+datetime.timedelta(days=i)).strftime('%y%j')
        datapath = basepath+daydir+'/TRTC'+daydir+'/'
        dayfilelist = glob.glob(datapath+'CZC*0T.trt')
        if not dayfilelist:
            warn('No TRT files in '+datapath)
            continue
        t_filelist.extend(dayfilelist)

    filelist = []
    for filename in t_filelist:
        bfile = os.path.basename(filename)
        datetimestr = bfile[3:12]
        fdatetime = datetime.datetime.strptime(datetimestr, '%y%j%H%M')
        if starttime <= fdatetime <= endtime:
            filelist.append(filename)
        # filelist.append(filename)

    return sorted(filelist)


def get_scan_list(scandescriptor_list):
    """
    determine which is the scan list for each radar

    Parameters
    ----------
    scandescriptor : list of string
        the list of all scans for all radars

    Returns
    -------
    scan_list : list of lists
        the list of scans corresponding to each radar

    """
    descrfields = scandescriptor_list[0].split(':')
    if len(descrfields) == 1:
        # one radar
        return [scandescriptor_list]

    # one or more radars
    # check how many radars are there
    radar_list = set()
    for scandescriptor in scandescriptor_list:
        radar_list.add(scandescriptor.split(':')[0])
    nradar = len(radar_list)

    # create the list of lists
    scan_list = [[] for i in range(nradar)]
    for scandescriptor in scandescriptor_list:
        descrfields = scandescriptor.split(':')
        ind_rad = int(descrfields[0][5:8])-1
        scan_list[ind_rad].append(descrfields[1])

    return scan_list


def get_new_rainbow_file_name(master_fname, master_datadescriptor, datatype):
    """
    get the rainbow file name containing datatype from a master file name
    and data type

    Parameters
    ----------
    master_fname : str
        the master file name
    master_datadescriptor : str
        the master data type descriptor
    datatype : str
        the data type of the new file name to be created

    Returns
    -------
    new_fname : str
        the new file name

    """
    _, _, master_datatype, _, _ = get_datatype_fields(master_datadescriptor)
    datapath = os.path.dirname(master_fname)
    voltime = get_datetime(master_fname, master_datatype)
    voltype = os.path.basename(master_fname).split('.')[1]

    return (datapath+'/'+voltime.strftime('%Y%m%d%H%M%S')+'00'+datatype+'.' +
            voltype)


def get_datatype_fields(datadescriptor):
    """
    splits the data type descriptor and provides each individual member

    Parameters
    ----------
    datadescriptor : str
        radar field type. Format : [radar file type]:[datatype]

    Returns
    -------
    radarnr : str
        radar number, i.e. RADAR1, RADAR2, ...
    datagroup : str
        data type group, i.e. RAINBOW, RAD4ALP, ODIM, CFRADIAL, COSMO, MXPOL ...
    datatype : str
        data type, i.e. dBZ, ZDR, ISO0, ...
    dataset : str
        dataset type (for saved data only)
    product : str
        product type (for saved data only)

    """
    descrfields = datadescriptor.split(':')
    if len(descrfields) == 1:
        radarnr = 'RADAR001'
        datagroup = 'RAINBOW'
        datatype = descrfields[0]
        dataset = None
        product = None
    elif descrfields[0].startswith('RADAR'):
        radarnr = descrfields[0]
        if len(descrfields) == 2:
            radarnr = descrfields[0]
            datagroup = 'RAINBOW'
            datatype = descrfields[1]
            dataset = None
            product = None
        else:
            datagroup = descrfields[1]
            if datagroup in ('CFRADIAL', 'ODIMPYRAD', 'PYRADGRID'):
                descrfields2 = descrfields[2].split(',')
                datatype = descrfields2[0]
                dataset = descrfields2[1]
                product = descrfields2[2]
            elif datagroup == 'MXPOL':
                datatype = descrfields[2]
                dataset = None
                product = None
            elif datagroup == 'ODIM':
                descrfields2 = descrfields[2].split(',')
                datatype = descrfields2[0]
                product = None
                dataset = None
                if np.size(descrfields2) == 2:
                    dataset = descrfields2[1]
            else:
                datatype = descrfields[2]
                dataset = None
                product = None
    else:
        radarnr = 'RADAR001'
        datagroup = descrfields[0]
        if datagroup in ('CFRADIAL', 'ODIMPYRAD', 'PYRADGRID'):
            descrfields2 = descrfields[1].split(',')
            datatype = descrfields2[0]
            dataset = descrfields2[1]
            product = descrfields2[2]
        elif datagroup == 'MXPOL':
            datatype = descrfields[1]
            dataset = None
            product = None
        elif datagroup == 'ODIM':
            descrfields2 = descrfields[1].split(',')
            #warn(" descrfields2:  '%s'" % descrfields2[1])
            if len(descrfields2) == 2:
                datatype = descrfields2[0]
                dataset = descrfields2[1]
                product = None
                #warn(" dataset:  '%s'" % dataset)
            else:
                datatype = descrfields[1]
                dataset = None
                product = None
        else:
            datatype = descrfields[1]
            dataset = None
            product = None
    #warn(" dataset:  '%s'" % dataset)
    return radarnr, datagroup, datatype, dataset, product


def get_dataset_fields(datasetdescr):
    """
    splits the dataset type descriptor and provides each individual member

    Parameters
    ----------
    datasetdescr : str
        dataset type. Format : [processing level]:[dataset type]

    Returns
    -------
    proclevel : str
        dataset processing level

    dataset : str
        dataset type, i.e. dBZ, ZDR, ISO0, ...

    """
    descrfields = datasetdescr.split(':')
    if len(descrfields) == 1:
        proclevel = 'l00'
        dataset = descrfields[0]
    else:
        proclevel = descrfields[0]
        dataset = descrfields[1]
        if len(proclevel) == 2:
            proclevel = proclevel[0]+'0'+proclevel[1]

    return proclevel, dataset


def get_datetime(fname, datadescriptor):
    """
    Given a data descriptor gets date and time from file name

    Parameters
    ----------
    fname : str
        file name
    datadescriptor : str
        radar field type. Format : [radar file type]:[datatype]

    Returns
    -------
    fdatetime : datetime object
        date and time in file name

    """
    _, datagroup, _, dataset, _ = get_datatype_fields(datadescriptor)

    return _get_datetime(fname, datagroup, ftime_format=dataset)


def find_cosmo_file(voltime, datatype, cfg, scanid, ind_rad=0):
    """
    Search a COSMO file in Rainbow format

    Parameters
    ----------
    voltime : datetime object
        volume scan time
    datatype : str
        type of COSMO data to look for
    cfg : dictionary of dictionaries
        configuration info to figure out where the data is
    scanid : str
        name of the scan
    ind_rad : int
        radar index

    Returns
    -------
    fname : str
        Name of COSMO file if it exists. None otherwise

    """
    # hour rounded date-time
    fdatetime = voltime.strftime('%Y%m%d%H')+'000000'

    # initial run time to look for
    hvol = int(voltime.strftime('%H'))
    runhour0 = int(hvol/cfg['CosmoRunFreq'])*cfg['CosmoRunFreq']
    runtime0 = voltime.replace(hour=runhour0, minute=0, second=0)

    # look for cosmo file
    found = False
    nruns_to_check = int((cfg['CosmoForecasted']-1)/cfg['CosmoRunFreq'])
    for i in range(nruns_to_check):
        runtime = runtime0-datetime.timedelta(hours=i * cfg['CosmoRunFreq'])
        runtimestr = runtime.strftime('%Y%m%d%H')+'000000'

        daydir = runtime.strftime('%Y-%m-%d')
        datapath = cfg['cosmopath'][ind_rad]+datatype+'/'+scanid+daydir+'/'

        search_name = (
            datapath+datatype+'_RUN'+runtimestr+'_DX50'+fdatetime+'.*')
        print('Looking for file: '+search_name)
        fname = glob.glob(search_name)
        if fname:
            found = True
            break

    if found:
        return fname[0]

    warn('WARNING: Unable to get COSMO '+datatype+' information')
    return None




def find_raw_cosmo_file(voltime, datatype, cfg, ind_rad=0):
    """
    Search a COSMO file in netcdf format

    Parameters
    ----------
    voltime : datetime object
        volume scan time
    datatype : str
        type of COSMO data to look for
    cfg : dictionary of dictionaries
        configuration info to figure out where the data is
    ind_rad : int
        radar index

    Returns
    -------
    fname : str
        Name of COSMO file if it exists. None otherwise

    """
    # initial run time to look for
    runhour0 = int(voltime.hour/cfg['CosmoRunFreq'])*cfg['CosmoRunFreq']
    runtime0 = voltime.replace(hour=runhour0, minute=0, second=0)

    # look for cosmo file in raw
    found = False
    nruns_to_check = int(cfg['CosmoForecasted']/cfg['CosmoRunFreq'])
    for i in range(nruns_to_check):
        runtime = runtime0-datetime.timedelta(hours=i * cfg['CosmoRunFreq'])
        runtimestr = runtime.strftime('%Y%m%d%H')

        daydir = runtime.strftime('%Y-%m-%d')
        datapath = cfg['cosmopath'][ind_rad]+datatype+'/raw/'+daydir+'/'
        for model in ('cosmo-1', 'cosmo-2', 'cosmo-7'):
            if datatype == 'TEMP':
                search_name = (datapath+model+'_MDR_3D_'+runtimestr+'.nc')
            elif datatype == 'WIND':
                search_name = (datapath+model+'_MDR_3DWIND_'+runtimestr+'.nc')
            else:
                warn('Unable to get COSMO '+datatype+'. Unknown variable')
            print('Looking for file: '+search_name)
            fname = glob.glob(search_name)
            if fname:
                found = True
                break

        if found:
            break

    if found:
        return fname[0]

    # look for cosmo file in raw1
    found = False
    for i in range(nruns_to_check):
        runtime = runtime0-datetime.timedelta(hours=i * cfg['CosmoRunFreq'])
        runtimestr = runtime.strftime('%Y%m%d%H')

        daydir = runtime.strftime('%Y-%m-%d')
        datapath = cfg['cosmopath'][ind_rad]+datatype+'/raw1/'+daydir+'/'
        for model in ('cosmo-1', 'cosmo-2', 'cosmo-7'):
            if datatype == 'TEMP':
                search_name = (datapath+model+'_MDR_3D_'+runtimestr+'.nc')
            elif datatype == 'WIND':
                search_name = (datapath+model+'_MDR_3DWIND_'+runtimestr+'.nc')
            else:
                warn('Unable to get COSMO '+datatype+'. Unknown variable')
            print('Looking for file: '+search_name)
            fname = glob.glob(search_name)
            if fname:
                found = True
                break

        if found:
            break

    if found:
        return fname[0]

    warn('WARNING: Unable to get COSMO '+datatype+' information')
    return None


def find_hzt_file(voltime, cfg, ind_rad=0):
    """
    Search an ISO-0 degree file in HZT format

    Parameters
    ----------
    voltime : datetime object
        volume scan time
    cfg : dictionary of dictionaries
        configuration info to figure out where the data is
    ind_rad : int
        radar index

    Returns
    -------
    fname : str
        Name of HZT file if it exists. None otherwise

    """
    # initial run time to look for
    runhour0 = int(voltime.hour/cfg['CosmoRunFreq'])*cfg['CosmoRunFreq']
    runtime0 = voltime.replace(hour=runhour0, minute=0, second=0)

    # look for cosmo file
    found = False
    nruns_to_check = int((cfg['CosmoForecasted']-1)/cfg['CosmoRunFreq'])
    for i in range(nruns_to_check):
        runtime = runtime0-datetime.timedelta(hours=i * cfg['CosmoRunFreq'])
        target_hour = int((voltime - runtime).total_seconds() / 3600.)
        runtimestr = runtime.strftime('%y%j%H00')

        daydir = runtime.strftime('%y%j')
        if cfg['path_convention'] == 'RT':
            datapath = cfg['cosmopath'][ind_rad]+'HZT/'
        else:
            datapath = cfg['cosmopath'][ind_rad]+'HZT/'+daydir+'/'
        search_name = datapath+'HZT'+runtimestr+'0L.8'+'{:02d}'.format(
            target_hour)

        print('Looking for file: '+search_name)
        fname = glob.glob(search_name)
        if fname:
            found = True
            break

    if not found:
        warn('WARNING: Unable to find HZT file')
        return None

    return fname[0]


def find_rad4alpcosmo_file(voltime, datatype, cfg, scanid, ind_rad=0):
    """
    Search a COSMO file

    Parameters
    ----------
    voltime : datetime object
        volume scan time
    datatype : str
        type of COSMO data to look for
    cfg: dictionary of dictionaries
        configuration info to figure out where the data is
    ind_rad: int
        radar index

    Returns
    -------
    fname : str
        Name of COSMO file if it exists. None otherwise

    scanid: str
        name of the scan

    """
    # hour rounded date-time
    fdatetime = voltime.strftime('%y%j%H')+'00'

    # initial run time to look for
    hvol = int(voltime.strftime('%H'))
    runhour0 = int(hvol/cfg['CosmoRunFreq'])*cfg['CosmoRunFreq']
    runtime0 = voltime.replace(hour=runhour0, minute=0, second=0)

    # look for cosmo file
    found = False
    nruns_to_check = int((cfg['CosmoForecasted']-1)/cfg['CosmoRunFreq'])
    rad_id = 'P'+cfg['RadarRes'][ind_rad]+cfg['RadarName'][ind_rad]
    for i in range(nruns_to_check):
        runtime = runtime0-datetime.timedelta(hours=i * cfg['CosmoRunFreq'])
        runtimestr = runtime.strftime('%y%j%H')+'00'

        daydir = runtime.strftime('%y%j')
        datapath = (
            cfg['cosmopath'][ind_rad]+datatype+'/'+rad_id+'/'+daydir+'/')

        search_name = (
            datapath+datatype+'_RUN'+runtimestr+'_'+rad_id+fdatetime+'.' +
            scanid+'.bin')
        print('Looking for file: '+search_name)
        fname = glob.glob(search_name)
        if fname:
            found = True
            break

    if not found:
        warn('WARNING: Unable to get COSMO '+datatype+' information')
        return None

    return fname[0]


def _get_datetime(fname, datagroup, ftime_format=None):
    """
    Given a data group gets date and time from file name

    Parameters
    ----------
    fname : str
        file name
    datadescriptor : str
        radar field type. Format : [radar file type]:[datatype]
    ftime_format : str or None
        if the file is of type ODIM this contain the file time format

    Returns
    -------
    fdatetime : datetime object
        date and time in file name

    """
    bfile = os.path.basename(fname)
    if datagroup in ('RAINBOW', 'CFRADIAL', 'ODIMPYRAD', 'PYRADGRID'):
        datetimestr = bfile[0:14]
        fdatetime = datetime.datetime.strptime(datetimestr, '%Y%m%d%H%M%S')
    elif datagroup in ('RAD4ALP', 'RAD4ALPGRID', 'RAD4ALPGIF', 'RAD4ALPBIN'):
        datestr = bfile[3:8]
        timestr = bfile[8:12]
        if timestr != '2400':
            fdatetime = datetime.datetime.strptime(
                datestr+timestr, '%y%j%H%M')
        else:
            fdatetime = datetime.datetime.strptime(
                datestr, '%y%j')+datetime.timedelta(days=1)
    elif datagroup == 'ODIM':
        if ftime_format is None:
            # we assume is rad4alp format
            datetimestr = bfile[3:12]
            fdatetime = datetime.datetime.strptime(datetimestr, '%y%j%H%M')
        else:
            return find_date_in_file_name(
                bfile, date_format=ftime_format[ftime_format.find("F")+2:-1])
    elif datagroup == 'MXPOL':
        datetimestr = re.findall(r"([0-9]{8}-[0-9]{6})", bfile)[0]
        fdatetime = datetime.datetime.strptime(datetimestr, '%Y%m%d-%H%M%S')
    else:
        warn('unknown data group')
        return None

    return fdatetime


def find_date_in_file_name(filename, date_format='%Y%m%d%H%M%S'):
    """
    Find a date with date format defined in date_format in a file name.
    If no date is found returns None

    Parameters
    ----------
    filename : str
        file name
    date_format : str
        The time format

    Returns
    -------
    fdatetime : datetime object
        date and time in file name

    """
    today = datetime.datetime.now()
    len_datestr = len(today.strftime(date_format))
    count = 0
    bfile = os.path.basename(filename)
    while True:
        try:
            fdatetime = datetime.datetime.strptime(
                bfile[count:count+len_datestr], date_format)
        except ValueError:
            count = count + 1
            if count+len_datestr >= len(bfile):
                warn('Unable to find date from string name. ' +
                     'date format '+date_format+'. File name ' +
                     bfile)
                return None
        else:
            # No error, stop the loop
            break

    return fdatetime
