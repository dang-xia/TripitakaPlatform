from django.test import TestCase
from django.conf import settings
from .utils.punct_process import PunctProcess
from tasks.common import clean_separators
from django.utils.encoding import smart_text
# Create your tests here.

class BaseModelTest(TestCase):
    """
    In [13]: a = "qcabxcd"

    In [14]: b = "abyvvcddf"

    delete    a[0:2] --> b[0:0]     'qc' --> ''
    equal     a[2:4] --> b[0:2]     'ab' --> 'ab'
    replace   a[4:5] --> b[2:5]      'x' --> 'yvv'
    equal     a[5:7] --> b[5:7]     'cd' --> 'cd'
    insert    a[7:7] --> b[7:9]       '' --> 'df'


    delete: from j1=0 note
                offset = offset- ((i2-i1)-(j2-j1)),
    equal: none
    replace: from j1=2
                offset  = offset - ((i2-i1)-(j2-j1))
    insert: from j1
                offset = offset -((i2-i1)-(j2-j1))
    base_punct = [[1,'\n'],[2,'\n'],[3,'\n'],[4,","],[5,","],[6,"."]]

    a = "q\nc\na\nb,x,c.d"

    """
    def test_punct_case1(self):
        base_text = "qcabxcd"
        b = "abyvvcddf"
        base_punct = [[3,'\n'],[6,","]]
        o = 'qca\nbxc,d'
        s = 'a\nbyvvc,ddf'
        self.assertEqual(s, PunctProcess().reel_align_punct(base_text, base_punct, b))

    def test_punct_case2(self):
        base_text = "qcabxcd"
        b = "abyvvcddf"
        base_punct = [[7,",,,"]]
        o = "qcabxcd,,,"
        s = "abyvvcd,,,df"
        self.assertEqual(s, PunctProcess().reel_align_punct(base_text, base_punct, b))

    def test_punct_case3(self):
        base_text = "qcabxcd"
        b = "abyv"
        base_punct = [[7, ",,,"]]
        o = "qcabxcd,,,"
        s = "abyv,,,"
        self.assertEqual(s, PunctProcess().reel_align_punct(base_text, base_punct, b))

    def test_punct_case4(self):
        base_text = "qcabxcd"
        b = "abyvvcddf"
        base_punct = [[-1, '\n'], [2, '\n'], [3, '\n'], [4, ','], [5, ','], [6, '.']]
        o = "q\\nc\\na\\nb,x,c.d"
        s = '\na\nb,yvv,c.ddf'
        self.assertEqual(s,PunctProcess().reel_align_punct(base_text, base_punct, b))


    def test_realworld_case(self):
        base_punct = [[10,'\n'],[22,'\n'],[31,'\n'],[35,'\uff1a'],[35,'\n'],[37,'\uff0c'],[51,'\u3002'],[59,'\uff0c'],[67,'\uff0c'],[75,'\uff0c'],[83,'\uff0c'],[95,'\uff1b'],[99,'\uff0c'],[103,'\uff0c'],[111,'\uff0c'],[119,'\uff0c'],[127,'\uff0c'],[131,'\uff1b'],[139,'\uff0c'],[143,'\uff0c'],[151,'\u3002'],[159,'\uff0c'],[167,'\uff0c'],[175,'\uff0c'],[183,'\uff0c'],[191,'\u3002'],[199,'\uff0c'],[207,'\uff0c'],[215,'\uff0c'],[223,'\uff0c'],[227,'\uff0c'],[235,'\uff0c'],[239,'\uff1b'],[247,'\uff0c'],[255,'\uff0c'],[259,'\uff1b'],[263,'\uff0c'],[267,'\uff0c'],[275,'\uff0c'],[279,'\uff0c'],[291,'\uff0c'],[295,'\uff0c'],[299,'\u3002'],[299,'\n'],[307,'\uff0c'],[311,'\uff0c'],[319,'\uff0c'],[327,'\uff1b'],[331,'\uff0c'],[339,'\u3002'],[355,'\uff0c'],[363,'\uff0c'],[371,'\u3002'],[379,'\uff0c'],[387,'\uff0c'],[395,'\uff0c'],[399,'\uff0c'],[403,'\uff0c'],[411,'\uff1b'],[415,'\uff0c'],[423,'\u3002'],[431,'\uff0c'],[439,'\uff0c'],[447,'\uff0c'],[455,'\u3002'],[467,'\uff0c'],[475,'\uff0c'],[483,'\u3002'],[495,'\uff0c'],[503,'\uff0c'],[511,'\u3002'],[515,'\uff0c'],[519,'\u3002'],[527,'\uff0c'],[535,'\u3002'],[551,'\uff0c'],[555,'\uff0c'],[559,'\uff0c'],[567,'\u3002'],[567,'\n'],[580,'\uff0c'],[583,'\uff1a'],[587,'\u3001'],[593,'\u3001'],[599,'\u3001'],[605,'\u3001'],[611,'\u3001'],[617,'\u3001'],[623,'\u3001'],[629,'\u3001'],[635,'\u3001'],[641,'\u3001'],[647,'\u3001'],[653,'\u3001'],[659,'\u3001'],[668,'\u3001'],[674,'\u3001'],[682,'\u3001'],[690,'\u3001'],[696,'\u3001'],[702,'\u3001'],[708,'\uff0c'],[716,'\uff0c'],[726,'\uff1b'],[734,'\uff0c'],[742,'\uff0c'],[746,'\uff0c'],[750,'\uff0c'],[758,'\uff1b'],[766,'\uff0c'],[774,'\uff1b'],[782,'\uff0c'],[786,'\uff0c'],[794,'\uff1b'],[798,'\uff0c'],[802,'\uff0c'],[806,'\uff0c'],[810,'\uff0c'],[814,'\uff0c'],[822,'\uff0c'],[830,'\uff0c'],[838,'\uff0c'],[846,'\uff0c'],[852,'\u3001'],[854,'\uff0c'],[864,'\uff0c'],[872,'\uff0c'],[876,'\uff0c'],[880,'\u3002'],[888,'\uff0c'],[900,'\uff0c'],[904,'\uff1b'],[912,'\uff0c'],[920,'\uff0c'],[932,'\uff1b'],[940,'\uff0c'],[948,'\uff0c'],[956,'\uff0c'],[964,'\u3002'],[964,'\n'],[976,'\uff0c'],[979,'\uff1a'],[985,'\u3001'],[990,'\u3001'],[995,'\u3001'],[1000,'\u3001'],[1006,'\u3001'],[1011,'\u3001'],[1016,'\u3001'],[1021,'\u3001'],[1027,'\u3001'],[1033,'\uff0c'],[1041,'\uff0c'],[1051,'\uff0c'],[1055,'\u3002'],[1063,'\uff0c'],[1071,'\uff0c'],[1079,'\uff0c'],[1083,'\uff0c'],[1091,'\uff0c'],[1103,'\uff0c'],[1107,'\uff0c'],[1115,'\uff0c'],[1123,'\uff0c'],[1131,'\u3002'],[1131,'\n'],[1143,'\uff0c'],[1146,'\uff1a'],[1150,'\u3001'],[1155,'\u3001'],[1159,'\u3001'],[1163,'\u3001'],[1168,'\u3001'],[1172,'\u3001'],[1176,'\u3001'],[1180,'\u3001'],[1184,'\uff0c'],[1192,'\uff0c'],[1200,'\u3002'],[1200,'\n'],[1212,'\uff0c'],[1215,'\uff1a'],[1219,'\u3001'],[1223,'\u3001'],[1227,'\u3001'],[1231,'\u3001'],[1235,'\u3001'],[1239,'\uff0c'],[1243,'\uff0c'],[1255,'\uff0c'],[1263,'\u3002'],[1263,'\n'],[1275,'\uff0c'],[1278,'\uff1a'],[1282,'\u3001'],[1287,'\u3001'],[1292,'\u3001'],[1296,'\u3001'],[1301,'\u3001'],[1305,'\u3001'],[1310,'\u3001'],[1315,'\uff0c'],[1319,'\uff0c'],[1323,'\uff0c'],[1332,'\u3002'],[1332,'\n'],[1342,'\uff0c'],[1345,'\uff1a'],[1349,'\u3001'],[1353,'\u3001'],[1357,'\u3001'],[1361,'\u3001'],[1365,'\u3001'],[1369,'\u3001'],[1373,'\u3001'],[1377,'\uff0c'],[1381,'\uff0c'],[1389,'\u3002'],[1389,'\n'],[1397,'\uff0c'],[1400,'\uff1a'],[1403,'\u3001'],[1407,'\u3001'],[1410,'\uff0c'],[1413,'\u3001'],[1416,'\u3001'],[1419,'\u3001'],[1422,'\u3001'],[1425,'\u3001'],[1428,'\uff0c'],[1432,'\uff0c'],[1440,'\u3002'],[1440,'\n'],[1448,'\uff0c'],[1451,'\uff1a'],[1454,'\u3001'],[1457,'\u3001'],[1460,'\u3001'],[1463,'\u3001'],[1466,'\u3001'],[1469,'\u3001'],[1472,'\u3001'],[1475,'\uff0c'],[1479,'\uff0c'],[1483,'\u3002'],[1483,'\n'],[1491,'\uff0c'],[1494,'\uff1a'],[1497,'\u3001'],[1501,'\u3001'],[1505,'\u3001'],[1509,'\u3001'],[1513,'\u3001'],[1516,'\u3001'],[1519,'\u3001'],[1522,'\u3001'],[1526,'\uff0c'],[1530,'\uff0c'],[1538,'\u3002'],[1538,'\n'],[1548,'\uff0c'],[1551,'\uff1a'],[1556,'\u3001'],[1560,'\u3001'],[1564,'\u3001'],[1569,'\u3001'],[1574,'\u3001'],[1579,'\u3001'],[1583,'\uff0c'],[1587,'\uff0c'],[1599,'\u3002'],[1599,'\n'],[1610,'\uff0c'],[1613,'\uff1a'],[1618,'\u3001'],[1623,'\u3001'],[1627,'\u3001'],[1630,'\u3001'],[1634,'\u3001'],[1639,'\u3001'],[1644,'\uff0c'],[1648,'\uff0c'],[1656,'\u3002'],[1656,'\n'],[1664,'\uff0c'],[1667,'\uff1a'],[1674,'\u3001'],[1678,'\u3001'],[1682,'\u3001'],[1686,'\u3001'],[1690,'\u3001'],[1695,'\u3001'],[1700,'\u3001'],[1704,'\uff0c'],[1708,'\uff0c'],[1714,'\uff0c'],[1718,'\u3002'],[1718,'\n'],[1726,'\uff0c'],[1729,'\uff1a'],[1734,'\u3001'],[1739,'\u3001'],[1742,'\u3001'],[1747,'\u3001'],[1750,'\u3001'],[1755,'\u3001'],[1760,'\u3001'],[1765,'\u3001'],[1770,'\uff0c'],[1774,'\uff0c'],[1778,'\uff0c'],[1782,'\u3002'],[1782,'\n'],[1790,'\uff0c'],[1793,'\uff1a'],[1796,'\u3001'],[1799,'\u3001'],[1804,'\u3001'],[1808,'\u3001'],[1813,'\u3001'],[1817,'\u3001'],[1822,'\u3001'],[1827,'\u3001'],[1831,'\uff0c'],[1835,'\uff0c'],[1843,'\u3002'],[1843,'\n'],[1851,'\uff0c'],[1854,'\uff1a'],[1857,'\u3001'],[1860,'\u3001'],[1865,'\u3001'],[1870,'\u3001'],[1875,'\u3001'],[1881,'\u3001'],[1886,'\u3001'],[1893,'\u3001'],[1896,'\u3001'],[1900,'\uff0c'],[1904,'\uff0c'],[1912,'\u3002'],[1912,'\n'],[1920,'\uff0c'],[1923,'\uff1a'],[1927,'\u3001'],[1934,'\u3001'],[1940,'\u3001'],[1944,'\u3001'],[1949,'\u3001'],[1953,'\u3001'],[1960,'\u3001'],[1965,'\u3001'],[1970,'\u3001'],[1975,'\uff0c'],[1979,'\uff0c'],[1987,'\u3002'],[1987,'\n'],[1996,'\uff0c'],[1999,'\uff1a'],[2003,'\u3001'],[2009,'\u3001'],[2013,'\u3001'],[2016,'\u3001'],[2021,'\u3001'],[2026,'\u3001'],[2031,'\uff0c'],[2035,'\uff0c'],[2043,'\u3002'],[2043,'\n'],[2052,'\uff0c'],[2055,'\uff1a'],[2060,'\u3001'],[2065,'\u3001'],[2070,'\u3001'],[2075,'\u3001'],[2080,'\u3001'],[2085,'\u3001'],[2090,'\u3001'],[2095,'\u3001'],[2100,'\u3001'],[2105,'\uff0c'],[2109,'\uff0c'],[2113,'\uff0c'],[2117,'\u3002'],[2117,'\n'],[2126,'\uff0c'],[2129,'\uff1a'],[2132,'\u3001'],[2135,'\u3001'],[2139,'\u3001'],[2144,'\u3001'],[2149,'\u3001'],[2153,'\u3001'],[2157,'\u3001'],[2161,'\u3001'],[2164,'\u3001'],[2167,'\uff0c'],[2171,'\uff0c'],[2179,'\uff0c'],[2183,'\u3002'],[2183,'\n'],[2193,'\uff0c'],[2196,'\uff1a'],[2199,'\u3001'],[2204,'\u3001'],[2209,'\u3001'],[2212,'\u3001'],[2215,'\u3001'],[2220,'\u3001'],[2225,'\u3001'],[2230,'\uff0c'],[2234,'\uff0c'],[2242,'\u3002'],[2242,'\n'],[2251,'\uff0c'],[2254,'\uff1a'],[2258,'\u3001'],[2262,'\u3001'],[2267,'\u3001'],[2272,'\u3001'],[2277,'\u3001'],[2282,'\u3001'],[2287,'\uff0c'],[2291,'\uff0c'],[2299,'\u3002'],[2299,'\n'],[2307,'\uff0c'],[2310,'\uff1a'],[2314,'\u3001'],[2318,'\u3001'],[2321,'\u3001'],[2324,'\u3001'],[2327,'\u3001'],[2331,'\u3001'],[2336,'\u3001'],[2341,'\u3001'],[2345,'\uff0c'],[2349,'\uff0c'],[2357,'\u3002'],[2357,'\n'],[2366,'\uff0c'],[2369,'\uff1a'],[2372,'\u3001'],[2376,'\u3001'],[2382,'\u3001'],[2388,'\u3001'],[2392,'\u3001'],[2396,'\u3001'],[2402,'\u3001'],[2407,'\u3001'],[2411,'\u3001'],[2417,'\uff0c'],[2421,'\uff0c'],[2433,'\u3002'],[2433,'\n'],[2441,'\uff0c'],[2444,'\uff1a'],[2447,'\u3001'],[2452,'\u3001'],[2458,'\u3001'],[2463,'\u3001'],[2469,'\u3001'],[2475,'\u3001'],[2479,'\u3001'],[2483,'\u3001'],[2488,'\u3001'],[2493,'\uff0c'],[2497,'\uff0c'],[2505,'\uff0c'],[2513,'\u3002'],[2513,'\n'],[2523,'\uff0c'],[2526,'\uff1a'],[2532,'\u3001'],[2537,'\u3001'],[2541,'\u3001'],[2546,'\u3001'],[2550,'\u3001'],[2554,'\u3001'],[2558,'\u3001'],[2562,'\uff0c'],[2566,'\uff0c'],[2574,'\uff0c'],[2582,'\u3002'],[2582,'\n'],[2591,'\uff0c'],[2594,'\uff1a'],[2598,'\u3001'],[2603,'\u3001'],[2608,'\u3001'],[2613,'\u3001'],[2618,'\u3001'],[2624,'\u3001'],[2628,'\u3001'],[2633,'\u3001'],[2638,'\u3001'],[2643,'\uff0c'],[2647,'\uff0c'],[2655,'\uff0c'],[2659,'\u3002'],[2659,'\n'],[2668,'\uff0c'],[2671,'\uff1a'],[2675,'\u3001'],[2679,'\u3001'],[2683,'\u3001'],[2688,'\u3001'],[2692,'\u3001'],[2697,'\u3001'],[2702,'\u3001'],[2708,'\u3001'],[2712,'\uff0c'],[2716,'\uff0c'],[2724,'\u3002'],[2724,'\n'],[2735,'\uff0c'],[2738,'\uff1a'],[2742,'\u3001'],[2746,'\u3001'],[2752,'\u3001'],[2758,'\u3001'],[2763,'\u3001'],[2768,'\u3001'],[2772,'\uff0c'],[2776,'\uff0c'],[2784,'\uff0c'],[2788,'\u3002'],[2788,'\n'],[2799,'\uff0c'],[2802,'\uff1a'],[2807,'\u3001'],[2811,'\u3001'],[2816,'\u3001'],[2821,'\u3001'],[2826,'\u3001'],[2831,'\u3001'],[2836,'\u3001'],[2841,'\u3001'],[2847,'\u3001'],[2852,'\uff0c'],[2856,'\uff0c'],[2864,'\u3002'],[2864,'\n'],[2874,'\uff0c'],[2877,'\uff1a'],[2881,'\u3001'],[2885,'\u3001'],[2889,'\u3001'],[2893,'\u3001'],[2898,'\u3001'],[2906,'\u3001'],[2911,'\u3001'],[2916,'\uff0c'],[2920,'\uff0c'],[2924,'\uff0c'],[2928,'\uff0c'],[2936,'\u3002'],[2936,'\n'],[2945,'\uff0c'],[2948,'\uff1a'],[2952,'\u3001'],[2956,'\u3001'],[2960,'\u3001'],[2965,'\u3001'],[2970,'\u3001'],[2975,'\u3001'],[2980,'\u3001'],[2985,'\u3001'],[2991,'\uff0c'],[2995,'\uff0c'],[3003,'\u3002'],[3003,'\n'],[3012,'\uff0c'],[3015,'\uff1a'],[3019,'\u3001'],[3022,'\u3001'],[3025,'\u3001'],[3029,'\u3001'],[3033,'\u3001'],[3038,'\u3001'],[3042,'\u3001'],[3047,'\u3001'],[3052,'\u3001'],[3055,'\uff0c'],[3059,'\uff0c'],[3067,'\u3002'],[3067,'\n'],[3076,'\uff0c'],[3079,'\uff1a'],[3083,'\u3001'],[3087,'\u3001'],[3090,'\u3001'],[3094,'\u3001'],[3099,'\u3001'],[3103,'\u3001'],[3108,'\u3001'],[3111,'\uff0c'],[3115,'\uff0c'],[3123,'\u3002'],[3123,'\n'],[3137,'\uff0c'],[3140,'\uff1a'],[3143,'\u3001'],[3146,'\u3001'],[3150,'\u3001'],[3155,'\u3001'],[3160,'\u3001'],[3165,'\u3001'],[3169,'\u3001'],[3173,'\u3001'],[3177,'\u3001'],[3181,'\uff0c'],[3185,'\uff0c'],[3193,'\uff0c'],[3201,'\u3002'],[3201,'\n'],[3210,'\uff0c'],[3218,'\uff1b'],[3226,'\uff0c'],[3234,'\uff0c'],[3242,'\uff0c'],[3250,'\u3002'],[3254,'\uff0c'],[3258,'\uff0c'],[3266,'\uff0c'],[3270,'\uff0c'],[3278,'\u3002'],[3282,'\uff1f'],[3295,'\uff0c'],[3303,'\u3002'],[3311,'\uff0c'],[3315,'\uff0c'],[3323,'\uff0c'],[3331,'\uff0c'],[3339,'\uff1b'],[3347,'\uff0c'],[3355,'\u3002'],[3363,'\uff0c'],[3367,'\uff0c'],[3371,'\uff0c'],[3379,'\uff1b'],[3387,'\uff0c'],[3395,'\u3002'],[3395,'\n'],[3402,'\uff0c'],[3415,'\uff0c'],[3419,'\uff1b'],[3426,'\uff0c'],[3434,'\uff0c'],[3438,'\uff1b'],[3443,'\uff0c'],[3455,'\uff0c'],[3459,'\uff1b'],[3463,'\uff0c'],[3475,'\uff0c'],[3479,'\uff1b'],[3483,'\uff0c'],[3495,'\uff0c'],[3499,'\uff1b'],[3503,'\uff0c'],[3511,'\uff0c'],[3515,'\uff1b'],[3519,'\uff0c'],[3529,'\uff0c'],[3533,'\uff1b'],[3537,'\uff0c'],[3551,'\uff0c'],[3555,'\uff1b'],[3559,'\uff0c'],[3567,'\uff0c'],[3571,'\uff1b'],[3575,'\uff0c'],[3582,'\uff0c'],[3586,'\u3002'],[3586,'\n'],[3595,'\uff0c'],[3601,'\uff0c'],[3609,'\uff0c'],[3613,'\uff1a'],[3613,'\n'],[3620,'\uff0c'],[3627,'\uff0c'],[3627,'\n'],[3634,'\uff0c'],[3641,'\u3002'],[3641,'\n'],[3648,'\uff0c'],[3655,'\uff0c'],[3655,'\n'],[3662,'\uff0c'],[3669,'\u3002'],[3669,'\n'],[3676,'\uff0c'],[3683,'\uff0c'],[3683,'\n'],[3690,'\uff0c'],[3697,'\u3002'],[3697,'\n'],[3704,'\uff0c'],[3711,'\uff0c'],[3711,'\n'],[3718,'\uff0c'],[3725,'\u3002'],[3725,'\n'],[3732,'\uff0c'],[3739,'\uff0c'],[3739,'\n'],[3746,'\uff0c'],[3753,'\u3002'],[3753,'\n'],[3760,'\uff0c'],[3767,'\uff0c'],[3767,'\n'],[3774,'\uff0c'],[3781,'\u3002'],[3781,'\n'],[3788,'\uff0c'],[3795,'\uff0c'],[3795,'\n'],[3802,'\uff0c'],[3809,'\u3002'],[3809,'\n'],[3816,'\uff0c'],[3823,'\uff0c'],[3823,'\n'],[3830,'\uff0c'],[3837,'\u3002'],[3837,'\n'],[3844,'\uff0c'],[3851,'\uff0c'],[3851,'\n'],[3858,'\uff0c'],[3865,'\u3002'],[3865,'\n'],[3872,'\uff0c'],[3879,'\uff0c'],[3879,'\n'],[3886,'\uff0c'],[3893,'\u3002'],[3893,'\n'],[3901,'\uff0c'],[3913,'\uff0c'],[3917,'\uff1b'],[3921,'\uff0c'],[3933,'\uff0c'],[3937,'\uff1b'],[3941,'\uff0c'],[3957,'\uff0c'],[3961,'\uff1b'],[3966,'\uff0c'],[3976,'\uff0c'],[3980,'\uff1b'],[3984,'\uff0c'],[3996,'\uff0c'],[4000,'\uff1b'],[4004,'\uff0c'],[4018,'\uff0c'],[4022,'\uff1b'],[4027,'\uff0c'],[4040,'\uff0c'],[4044,'\uff1b'],[4048,'\uff0c'],[4060,'\uff0c'],[4064,'\u3002'],[4064,'\n'],[4066,'\uff0c'],[4076,'\uff0c'],[4084,'\uff0c'],[4088,'\uff1a'],[4088,'\n'],[4093,'\uff0c'],[4098,'\uff0c'],[4098,'\n'],[4103,'\uff0c'],[4108,'\u3002'],[4108,'\n'],[4113,'\uff0c'],[4118,'\uff0c'],[4118,'\n'],[4123,'\uff0c'],[4128,'\u3002'],[4128,'\n'],[4133,'\uff0c'],[4138,'\uff0c'],[4138,'\n'],[4143,'\uff0c'],[4148,'\uff0c'],[4148,'\n'],[4153,'\uff0c'],[4158,'\uff0c'],[4158,'\n'],[4163,'\uff0c'],[4168,'\u3002'],[4168,'\n'],[4173,'\uff0c'],[4178,'\uff0c'],[4178,'\n'],[4183,'\uff0c'],[4188,'\u3002'],[4188,'\n'],[4193,'\uff0c'],[4198,'\uff0c'],[4198,'\n'],[4203,'\uff0c'],[4208,'\u3002'],[4208,'\n'],[4213,'\uff0c'],[4218,'\uff0c'],[4218,'\n'],[4223,'\uff0c'],[4228,'\u3002'],[4228,'\n'],[4233,'\uff0c'],[4238,'\uff0c'],[4238,'\n'],[4243,'\uff0c'],[4248,'\u3002'],[4248,'\n'],[4253,'\uff0c'],[4258,'\uff0c'],[4258,'\n'],[4263,'\uff0c'],[4268,'\u3002'],[4268,'\n'],[4273,'\uff0c'],[4278,'\uff0c'],[4278,'\n'],[4283,'\uff0c'],[4288,'\uff0c'],[4288,'\n'],[4293,'\uff0c'],[4298,'\uff0c'],[4298,'\n'],[4303,'\uff0c'],[4308,'\u3002'],[4308,'\n'],[4313,'\uff0c'],[4318,'\uff0c'],[4318,'\n'],[4323,'\uff0c'],[4328,'\u3002'],[4328,'\n'],[4333,'\uff0c'],[4338,'\uff0c'],[4338,'\n'],[4343,'\uff0c'],[4348,'\u3002'],[4348,'\n'],[4353,'\uff0c'],[4358,'\uff0c'],[4358,'\n'],[4363,'\uff0c'],[4368,'\u3002'],[4368,'\n'],[4373,'\uff0c'],[4378,'\uff0c'],[4378,'\n'],[4383,'\uff0c'],[4388,'\u3002'],[4388,'\n'],[4393,'\uff0c'],[4398,'\uff0c'],[4398,'\n'],[4403,'\uff0c'],[4408,'\u3002'],[4408,'\n'],[4413,'\uff0c'],[4418,'\uff0c'],[4418,'\n'],[4423,'\uff0c'],[4428,'\u3002'],[4428,'\n'],[4433,'\uff0c'],[4438,'\uff0c'],[4438,'\n'],[4443,'\uff0c'],[4448,'\u3002'],[4448,'\n'],[4453,'\uff0c'],[4458,'\uff0c'],[4458,'\n'],[4463,'\uff0c'],[4468,'\u3002'],[4468,'\n'],[4474,'\uff0c'],[4483,'\uff0c'],[4487,'\uff1b'],[4491,'\uff0c'],[4499,'\uff0c'],[4503,'\uff1b'],[4507,'\uff0c'],[4514,'\uff0c'],[4518,'\uff1b'],[4522,'\uff0c'],[4531,'\uff0c'],[4535,'\uff1b'],[4539,'\uff0c'],[4554,'\uff0c'],[4558,'\uff1b'],[4562,'\uff0c'],[4575,'\uff0c'],[4579,'\uff1b'],[4583,'\uff0c'],[4598,'\uff0c'],[4602,'\u3002'],[4602,'\n'],[4604,'\uff0c'],[4612,'\uff0c'],[4618,'\uff0c'],[4622,'\uff1a'],[4622,'\n'],[4629,'\uff0c'],[4636,'\uff0c'],[4636,'\n'],[4643,'\uff0c'],[4650,'\u3002'],[4650,'\n'],[4657,'\uff0c'],[4664,'\uff0c'],[4664,'\n'],[4671,'\uff0c'],[4678,'\u3002'],[4678,'\n'],[4685,'\uff0c'],[4692,'\uff0c'],[4692,'\n'],[4699,'\uff0c'],[4706,'\u3002'],[4706,'\n'],[4713,'\uff0c'],[4720,'\uff0c'],[4720,'\n'],[4727,'\uff0c'],[4734,'\u3002'],[4734,'\n'],[4741,'\uff0c'],[4748,'\uff0c'],[4748,'\n'],[4755,'\uff0c'],[4762,'\u3002'],[4762,'\n'],[4769,'\uff0c'],[4776,'\uff0c'],[4776,'\n'],[4783,'\uff0c'],[4790,'\u3002'],[4790,'\n'],[4797,'\uff0c'],[4804,'\uff0c'],[4804,'\n'],[4811,'\uff0c'],[4818,'\u3002'],[4818,'\n'],[4825,'\uff0c'],[4832,'\uff0c'],[4832,'\n'],[4839,'\uff0c'],[4846,'\u3002'],[4846,'\n'],[4853,'\uff0c'],[4860,'\uff0c'],[4860,'\n'],[4867,'\uff0c'],[4874,'\u3002'],[4874,'\n'],[4881,'\uff0c'],[4888,'\uff0c'],[4888,'\n'],[4895,'\uff0c'],[4902,'\u3002'],[4902,'\n'],[4909,'\uff0c'],[4916,'\uff0c'],[4916,'\n'],[4923,'\uff0c'],[4930,'\u3002'],[4930,'\n'],[4936,'\uff0c'],[4947,'\uff0c'],[4951,'\uff1b'],[4955,'\uff0c'],[4969,'\uff0c'],[4973,'\uff1b'],[4977,'\uff0c'],[4996,'\uff0c'],[5000,'\uff1b'],[5004,'\uff0c'],[5008,'\u3001'],[5009,'\u3001'],[5018,'\uff0c'],[5022,'\uff1b'],[5026,'\uff0c'],[5041,'\uff0c'],[5045,'\uff1b'],[5049,'\uff0c'],[5067,'\uff0c'],[5071,'\uff1b'],[5076,'\uff0c'],[5083,'\uff0c'],[5087,'\uff1b'],[5091,'\uff0c'],[5102,'\uff0c'],[5106,'\uff1b'],[5110,'\uff0c'],[5122,'\uff0c'],[5126,'\uff1b'],[5130,'\uff0c'],[5147,'\uff0c'],[5151,'\u3002'],[5153,'\uff0c'],[5161,'\uff0c'],[5167,'\uff0c'],[5171,'\uff1a'],[5171,'\n'],[5178,'\uff0c'],[5185,'\uff0c'],[5185,'\n'],[5192,'\uff0c'],[5199,'\u3002'],[5199,'\n'],[5206,'\uff0c'],[5213,'\uff0c'],[5213,'\n'],[5220,'\uff0c'],[5227,'\u3002'],[5227,'\n'],[5234,'\uff0c'],[5241,'\uff0c'],[5241,'\n'],[5248,'\uff0c'],[5255,'\u3002'],[5255,'\n'],[5262,'\uff0c'],[5269,'\uff0c'],[5269,'\n'],[5276,'\uff0c'],[5283,'\u3002'],[5283,'\n'],[5290,'\uff0c'],[5297,'\uff0c'],[5297,'\n'],[5304,'\uff0c'],[5311,'\u3002'],[5311,'\n'],[5318,'\uff0c'],[5325,'\uff0c'],[5325,'\n'],[5332,'\uff0c'],[5339,'\u3002'],[5339,'\n'],[5346,'\uff0c'],[5353,'\uff0c'],[5353,'\n'],[5360,'\uff0c'],[5367,'\u3002'],[5367,'\n'],[5374,'\uff0c'],[5381,'\uff0c'],[5381,'\n'],[5388,'\uff0c'],[5395,'\u3002'],[5395,'\n'],[5402,'\uff0c'],[5409,'\uff0c'],[5409,'\n'],[5416,'\uff0c'],[5423,'\u3002'],[5423,'\n'],[5430,'\uff0c'],[5437,'\uff0c'],[5437,'\n'],[5444,'\uff0c'],[5451,'\u3002'],[5451,'\n'],[5458,'\uff0c'],[5469,'\uff0c'],[5473,'\uff1b'],[5477,'\uff0c'],[5489,'\uff0c'],[5493,'\uff1b'],[5497,'\uff0c'],[5510,'\uff0c'],[5514,'\uff1b'],[5518,'\uff0c'],[5532,'\uff0c'],[5536,'\uff1b'],[5540,'\uff0c'],[5549,'\uff0c'],[5553,'\uff1b'],[5557,'\uff0c'],[5571,'\uff0c'],[5575,'\uff1b'],[5578,'\uff0c'],[5588,'\uff0c'],[5592,'\uff1b'],[5595,'\uff0c'],[5605,'\uff0c'],[5609,'\uff1b'],[5613,'\uff0c'],[5629,'\uff0c'],[5633,'\uff1b'],[5637,'\uff0c'],[5647,'\uff0c'],[5651,'\u3002'],[5651,'\n'],[5653,'\uff0c'],[5661,'\uff0c'],[5669,'\uff0c'],[5673,'\uff1a'],[5673,'\n'],[5680,'\uff0c'],[5687,'\uff0c'],[5687,'\n'],[5694,'\uff0c'],[5701,'\u3002'],[5701,'\n'],[5708,'\uff0c'],[5715,'\uff0c'],[5715,'\n'],[5722,'\uff0c'],[5729,'\u3002'],[5729,'\n'],[5736,'\uff0c'],[5743,'\uff0c'],[5743,'\n'],[5750,'\uff0c'],[5757,'\u3002'],[5757,'\n'],[5764,'\uff0c'],[5771,'\uff0c'],[5771,'\n'],[5778,'\uff0c'],[5785,'\u3002'],[5785,'\n'],[5792,'\uff0c'],[5799,'\uff0c'],[5799,'\n'],[5806,'\uff0c'],[5813,'\u3002'],[5813,'\n'],[5820,'\uff0c'],[5827,'\uff0c'],[5827,'\n'],[5834,'\uff0c'],[5841,'\u3002'],[5841,'\n'],[5848,'\uff0c'],[5855,'\uff0c'],[5855,'\n'],[5862,'\uff0c'],[5869,'\u3002'],[5869,'\n'],[5876,'\uff0c'],[5883,'\uff0c'],[5883,'\n'],[5890,'\uff0c'],[5897,'\u3002'],[5897,'\n'],[5903,'\uff0c'],[5913,'\uff0c'],[5917,'\uff1b'],[5921,'\uff0c'],[5931,'\uff0c'],[5935,'\uff1b'],[5939,'\uff0c'],[5951,'\uff0c'],[5955,'\uff1b'],[5960,'\uff0c'],[5968,'\uff0c'],[5972,'\uff1b'],[5977,'\uff0c'],[5987,'\uff0c'],[5991,'\uff1b'],[5996,'\uff0c'],[6006,'\uff0c'],[6010,'\uff1b'],[6014,'\uff0c'],[6022,'\uff0c'],[6026,'\uff1b'],[6030,'\uff0c'],[6040,'\uff0c'],[6044,'\uff1b'],[6049,'\uff0c'],[6064,'\uff0c'],[6068,'\uff1b'],[6072,'\uff0c'],[6080,'\uff0c'],[6084,'\u3002'],[6084,'\n'],[6086,'\uff0c'],[6094,'\uff0c'],[6102,'\uff0c'],[6106,'\uff1a'],[6106,'\n'],[6113,'\uff0c'],[6120,'\uff0c'],[6120,'\n'],[6127,'\uff0c'],[6134,'\u3002'],[6134,'\n'],[6141,'\uff0c'],[6148,'\uff0c'],[6148,'\n'],[6155,'\uff0c'],[6162,'\u3002'],[6162,'\n'],[6169,'\uff0c'],[6176,'\uff0c'],[6176,'\n'],[6183,'\uff0c'],[6190,'\u3002'],[6190,'\n'],[6197,'\uff0c'],[6204,'\uff0c'],[6204,'\n'],[6211,'\uff0c'],[6218,'\u3002'],[6218,'\n'],[6225,'\uff0c'],[6232,'\uff0c'],[6232,'\n'],[6239,'\uff0c'],[6246,'\u3002'],[6246,'\n'],[6253,'\uff0c'],[6260,'\uff0c'],[6260,'\n'],[6267,'\uff0c'],[6274,'\u3002'],[6274,'\n'],[6281,'\uff0c'],[6288,'\uff0c'],[6288,'\n'],[6295,'\uff0c'],[6302,'\u3002'],[6302,'\n'],[6309,'\uff0c'],[6316,'\uff0c'],[6316,'\n'],[6323,'\uff0c'],[6330,'\u3002'],[6330,'\n'],[6337,'\uff0c'],[6344,'\uff0c'],[6344,'\n'],[6351,'\uff0c'],[6358,'\u3002'],[6358,'\n'],[6365,'\uff0c'],[6372,'\uff0c'],[6372,'\n'],[6379,'\uff0c'],[6386,'\u3002'],[6386,'\n'],[6392,'\uff0c'],[6401,'\uff0c'],[6405,'\uff1b'],[6409,'\uff0c'],[6420,'\uff0c'],[6424,'\uff1b'],[6428,'\uff0c'],[6440,'\uff0c'],[6444,'\uff1b'],[6447,'\uff0c'],[6462,'\uff0c'],[6466,'\uff1b'],[6469,'\uff0c'],[6483,'\uff0c'],[6487,'\uff1b'],[6491,'\uff0c'],[6506,'\uff0c'],[6510,'\uff1b'],[6514,'\uff0c'],[6529,'\uff0c'],[6533,'\uff1b'],[6537,'\uff0c'],[6550,'\uff0c'],[6554,'\uff1b'],[6558,'\uff0c'],[6570,'\uff0c'],[6574,'\uff1b'],[6578,'\uff0c'],[6590,'\uff0c'],[6594,'\u3002'],[6594,'\n'],[6596,'\uff0c'],[6604,'\uff0c'],[6610,'\uff0c'],[6614,'\uff1a'],[6614,'\n'],[6621,'\uff0c'],[6628,'\uff0c'],[6628,'\n'],[6635,'\uff0c'],[6642,'\u3002'],[6642,'\n'],[6649,'\uff0c'],[6656,'\uff0c'],[6656,'\n'],[6663,'\uff0c'],[6670,'\u3002'],[6670,'\n'],[6677,'\uff0c'],[6684,'\uff0c'],[6684,'\n'],[6691,'\uff0c'],[6698,'\u3002'],[6698,'\n'],[6705,'\uff0c'],[6712,'\uff0c'],[6712,'\n'],[6719,'\uff0c'],[6726,'\u3002'],[6726,'\n'],[6733,'\uff0c'],[6740,'\uff0c'],[6740,'\n'],[6747,'\uff0c'],[6754,'\u3002'],[6754,'\n'],[6761,'\uff0c'],[6768,'\uff0c'],[6768,'\n'],[6775,'\uff0c'],[6782,'\u3002'],[6782,'\n'],[6789,'\uff0c'],[6796,'\uff0c'],[6796,'\n'],[6803,'\uff0c'],[6810,'\u3002'],[6810,'\n'],[6817,'\uff0c'],[6824,'\uff0c'],[6824,'\n'],[6831,'\uff0c'],[6838,'\u3002'],[6838,'\n'],[6845,'\uff0c'],[6852,'\uff0c'],[6852,'\n'],[6859,'\uff0c'],[6866,'\u3002'],[6866,'\n'],[6873,'\uff0c'],[6880,'\uff0c'],[6880,'\n'],[6887,'\uff0c'],[6894,'\u3002'],[6894,'\n'],[6900,'\uff0c'],[6910,'\uff0c'],[6914,'\uff1b'],[6918,'\uff0c'],[6926,'\uff0c'],[6930,'\uff1b'],[6933,'\uff0c'],[6945,'\uff0c'],[6949,'\uff1b'],[6953,'\uff0c'],[6965,'\uff0c'],[6969,'\uff1b'],[6973,'\uff0c'],[6983,'\uff0c'],[6987,'\uff1b'],[6991,'\uff0c'],[7004,'\uff0c'],[7008,'\uff1b'],[7012,'\uff0c'],[7025,'\uff0c'],[7029,'\uff1b'],[7033,'\uff0c'],[7048,'\uff0c'],[7052,'\u3002'],[7052,'\n'],[7054,'\uff0c'],[7062,'\uff0c'],[7068,'\uff0c'],[7072,'\uff1a'],[7072,'\n'],[7079,'\uff0c'],[7086,'\uff0c'],[7086,'\n'],[7093,'\uff0c'],[7100,'\u3002'],[7100,'\n'],[7107,'\uff0c'],[7114,'\uff0c'],[7114,'\n'],[7121,'\uff0c'],[7128,'\u3002'],[7128,'\n'],[7135,'\uff0c'],[7142,'\uff0c'],[7142,'\n'],[7149,'\uff0c'],[7156,'\u3002'],[7156,'\n'],[7163,'\uff0c'],[7170,'\uff0c'],[7170,'\n'],[7177,'\uff0c'],[7184,'\u3002'],[7184,'\n'],[7191,'\uff0c'],[7198,'\uff0c'],[7198,'\n'],[7205,'\uff0c'],[7212,'\u3002'],[7212,'\n'],[7219,'\uff0c'],[7226,'\uff0c'],[7226,'\n'],[7233,'\uff0c'],[7240,'\u3002'],[7240,'\n'],[7247,'\uff0c'],[7254,'\uff0c'],[7254,'\n'],[7261,'\uff0c'],[7268,'\u3002'],[7268,'\n'],[7275,'\uff0c'],[7282,'\uff0c'],[7282,'\n'],[7289,'\uff0c'],[7296,'\u3002'],[7296,'\n'],[7302,'\uff0c'],[7314,'\uff0c'],[7318,'\uff1b'],[7322,'\uff0c'],[7328,'\uff0c'],[7332,'\uff1b'],[7336,'\uff0c'],[7346,'\uff0c'],[7350,'\uff1b'],[7354,'\uff0c'],[7361,'\uff0c'],[7365,'\uff1b'],[7369,'\uff0c'],[7378,'\uff0c'],[7382,'\uff1b'],[7387,'\uff0c'],[7400,'\uff0c'],[7404,'\uff1b'],[7407,'\uff0c'],[7417,'\uff0c'],[7421,'\uff1b'],[7426,'\uff0c'],[7436,'\uff0c'],[7440,'\uff1b'],[7444,'\uff0c'],[7452,'\uff0c'],[7456,'\uff1b'],[7461,'\uff0c'],[7473,'\uff0c'],[7477,'\u3002'],[7477,'\n'],[7479,'\uff0c'],[7487,'\uff0c'],[7493,'\uff0c'],[7497,'\uff1a'],[7497,'\n'],[7504,'\uff0c'],[7511,'\uff0c'],[7511,'\n'],[7518,'\uff0c'],[7525,'\u3002'],[7525,'\n'],[7532,'\uff0c'],[7539,'\uff0c'],[7539,'\n'],[7546,'\uff0c'],[7553,'\u3002'],[7553,'\n'],[7560,'\uff0c'],[7567,'\uff0c'],[7567,'\n'],[7574,'\uff0c'],[7581,'\u3002'],[7581,'\n'],[7588,'\uff0c'],[7595,'\uff0c'],[7595,'\n'],[7602,'\uff0c'],[7609,'\u3002'],[7609,'\n'],[7616,'\uff0c'],[7623,'\uff0c'],[7623,'\n'],[7630,'\uff0c'],[7637,'\u3002'],[7637,'\n'],[7644,'\uff0c'],[7651,'\uff0c'],[7651,'\n'],[7658,'\uff0c'],[7665,'\u3002'],[7665,'\n'],[7672,'\uff0c'],[7679,'\uff0c'],[7679,'\n'],[7686,'\uff0c'],[7693,'\u3002'],[7693,'\n'],[7700,'\uff0c'],[7707,'\uff0c'],[7707,'\n'],[7714,'\uff0c'],[7721,'\u3002'],[7721,'\n'],[7731,'\n']]
        base_cebta_reel001 = clean_separators(open(settings.BASE_DIR+"/data/sutra_text/CBETA_HUAYAN_0001.txt").read())
        yb_reel001_content = clean_separators(open(settings.BASE_DIR+"/data/sutra_text/YB000860_001_fixed.txt").read())
        # open(settings.BASE_DIR+"/data/sutra_text/YB000860_001_puncted.txt", 'w').write(
        #     smart_text(PunctProcess().reel_align_punct(base_cebta_reel001, base_punct, yb_reel001_content))
        # )
        self.assertEqual(smart_text(PunctProcess().reel_align_punct(base_cebta_reel001, base_punct, yb_reel001_content)), open(settings.BASE_DIR+"/data/sutra_text/YB000860_001_puncted.txt").read())
