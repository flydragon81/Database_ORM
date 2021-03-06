"""
    SPS Parser
"""
from function.Parser import Parser

SRC_DATA_RECORD = 'S'
RCV_DATA_RECORD = 'R'
REL_DATA_RECORD = 'X'
HEADER_RECORD = 'H'

# H00 SPS format version num.     SPS 2.1, JAN2006
# H26
# H26 Item  Definition of field       Cols   Format  Min to Max     Default  Units
# H26 ----  -------------------       ----   ------  ----------     -------  -----
# H26 0     Record identification     1-1    A1      R or S         None     -
# H26 1     Line name    (right)      2-11   F10.2                  None     -
# H26 2     Point number (right)      12-21  F10.2                  None     -
# H26 3     Point index               24-24  I1      1   9          1        -
# H26 4     Point code                25-26  A2      Free           None     -
# H26 5     Static correction         27-30  I4      -999 - 999     Blank    Msec
# H26 6     Point Depth               31-34  F4.1    0 - 99.9       None     Metre
# H26 7     Seismic datum             35-38  I4      -999 - 9999    None     Metre
# H26 8     Uphole time               39-40  I2      0 - 99         Blank    Msec
# H26 9     Water depth               41-46  F6.1    0 to 9999.9    Blank    Metre
# H26 10    Map grid easting          47-55  F9.1    Free           None     metre
# H26 11    Map grid northing         56-65  F10.1   Free           None     metre
# H26 12    Map grid elevation        66-71  F6.1    -999.9 9999.9  None     metre
# H26 13    Day of Year               72-74  I3      1 999          None     -
# H26 14    Time hhmmss               75-80  3I2     000000 235959  None     -
# H26      1         2         3         4         5         6         7         8
# H26 5678901234567890123456789012345678901234567890123456789012345678901234567890
# S   3762.00   3961.00  1A2     7.2   0    64.8 454773.4 3008241.9  -0.2177042821
# S   3762.00   3959.00  1A2     7.2   0    64.7 454762.9 3008193.0  -0.2177042841
sps21point = [
    ['RECORD_ID', 0, 1, 'string'],
    ['LINE', 1, 10, 'float'],
    ['POINT', 11, 10, 'float'],
    ['POINT_IDX', 23, 1, 'integer', 1],
    ['POINT_CODE', 24, 2, 'string'],
    ['STATIC_COR', 26, 4, 'integer'],
    ['POINT_DEPTH', 30, 4, 'float'],
    ['DATUM', 34, 4, 'integer'],
    ['UPHOLE_TIME', 38, 2, 'integer'],
    ['WATER_DEPTH', 40, 6, 'float'],
    ['EASTING', 46, 9, 'float'],
    ['NORTHING', 55, 10, 'float'],
    ['ELEVATION', 65, 6, 'float'],
    ['DAY_OF_YEAR', 71, 3, 'integer'],
    ['TIME', 74, 6, 'string'],
]

# H00 SPS format version number   SPS 2.1, JAN2006
# H26 ---------------------------------------------------------------------------
# H26 Item  Definition of field       Cols   Format  Min to Max     Default Units
# H26 ----  -------------------       ----   ------  ----------     ------- -----
# H26 0     Record identification     1-1    A1      'X'            None    -
# H26 1     Field tape number (r adj) 2-7    3A2     Free           None    -
# H26 2     Field record number       8-15   I8      0-16777216     None    -
# H26 3     Field record increment    16-16  I1      1-9            1       -
# H26 4     Instrument code           17-17  A1      1-9            1       -
# H26 5     Line name (r adj)         18-27  F10.2   -999999.99 to  None    -
# H26                                                9999999.99
# H26 6     Point number (r adj)      28-37  F10.2   -999999.99 to  None    -
# H26                                                 9999999.99
# H26 7     Point index               38-38  I1      1-9            1       -
# H26 8     From channel              39-43  I5      1-99999        None    -
# H26 9     To channel                44-48  I5      1-99999        None    -
# H26 10    Channel increment         49-49  I1      1-9            None    -
# H26 11    Line name (r adj)         50-59  F10.2   -999999.99 to  None    -
# H26                                                 9999999.99
# H26 12    From receiver (r adj)     60-69  F10.2   -999999.99 to  None    -
# H26                                                 9999999.99
# H26 13    To receiver (r adj)       70-79  F10.2   no default     None    -
# H26 14    Receiver Index            80-80  I1      1-9            1       -
# X  1001   8287311  19248.00  27516.001    1  4351  27023.00  18875.00  19743.001
# X  1001   8287311  19248.00  27516.001  436  8711  27039.00  18873.00  19743.001
sps21relation = [
    ['RECORD_ID', 0, 1, 'string'],
    ['TAPE_NUMBER', 1, 6, 'string'],
    ['RECORD_NUMBER', 7, 8, 'integer'],
    ['RECORD_INCREMENT', 15, 1, 'integer', 1],
    ['INSTRUMENT_CODE', 16, 1, 'string', '1'],
    ['S_LINE', 17, 10, 'float'],
    ['POINT', 27, 10, 'float'],
    ['POINT_IDX', 37, 1, 'integer'],
    ['FROM_CHANNEL', 38, 5, 'integer'],
    ['TO_CHANNEL', 43, 5, 'integer'],
    ['CHANNEL_INCREMENT', 48, 1, 'float'],
    ['R_LINE', 49, 10, 'float'],
    ['FROM_RECEIVER', 59, 10, 'float'],
    ['TO_RECEIVER', 69, 10, 'float'],
    ['RECEIVER_IDX', 79, 1, 'integer'],
]


class Sps21Parser(Parser):
    """
        SPS version 2.1 Parser
    """

    def parse_point(self, text_line):
        """
        Parser SPS Point record
        :param text_line:
        :return:
        """
        record_type = self.substr(text_line, sps21point[0][1], sps21point[0][2]).strip()
        if record_type not in (SRC_DATA_RECORD, RCV_DATA_RECORD):
            return
        self.set_definition(sps21point)
        return self.parse(text_line)

    def parse_relation(self, text_line):
        """
        Parser SPS Relation record
        :param text_line:
        :return:
        """
        record_type = self.substr(text_line, sps21point[0][1], sps21point[0][2]).strip()
        if record_type not in REL_DATA_RECORD:
            return

        self.set_definition(sps21relation)
        return self.parse(text_line)

    def get_fields_point(self):
        """
        Get Point fields description
        :return:
        """
        self.set_definition(sps21point)
        return self.get_fields()

    def get_fields_relation(self):
        """
        Get Relation fields description
        :return:
        """
        self.set_definition(sps21relation)
        return self.get_fields()


# H00 SPS format version num.         SPS001,08OCT1990 (SHELL EP 90-2935);
# H26
# H26 Item  Definition of field       Cols   Format  Min to Max     Default  Units
# H26 ----  -------------------       ----   ------  ----------     -------  -----
# H26 1     Record identification     1-1    A1      R or S         None     -
# H26 2     Line name (left just)     2-17   4A4     Free           None     -
# H26 3     Point number              18-25  2A4     Free           None     -
# H26 4     Point index               26-26  I1      1   9          1        -
# H26 5     Point code                27-28  A2      Free           None     -
# H26 6     Static correction         29-32  I4      -999 - 999     Blank    Msec
# H26 7     Point Depth               33-36  F4.1    0 - 99.9       None     Metre
# H26 8     Seismic datum             37-40  I4      -999 - 9999    None     Metre
# H26 9     Uphole time               41-42  I2      0 - 99         Blank    Msec
# H26 10    Water depth               43-46  F4.1    0 to 99.9/999  Blank    Metre
# H26 11    Map grid easting          47-55  F9.1    Free           None     metre
# H26 12    Map grid northing         56-65  F10.1   Free           None     metre
# H26 13    Map grid elevation        66-71  F6.1    -999.9 9999.9  None     metre
# H26 14    Day of Year               72-74  I3      1 999          None     -
# H26 15    Time hhmmss               75-80  3I2     000000 235959  None     -
# H26      1         2         3         4         5         6         7         8
# H26 5678901234567890123456789012345678901234567890123456789012345678901234567890
# S3762                39611A2     7.2   0  64.8 454773.4 3008241.9  -0.2177042821
# S3762                39591A2     7.2   0  64.7 454762.9 3008193.0  -0.2177042841
sps00point = []
sps00relation = []


class Sps00Parser(Parser):
    """
        SPS Parser of first version
    """

    pass


class Point:
    def __init__(self, data_array):
        self.type = data_array[0]
        self.line = data_array[1]
        self.point = data_array[2]
        self.point_idx = data_array[3]
        self.point_code = data_array[4]
        self.static_cor = data_array[5]
        self.point_depth = data_array[6]
        self.datum = data_array[7]
        self.uphole_time = data_array[8]
        self.water_depth = data_array[9]
        self.easting = data_array[10]
        self.northing = data_array[11]
        self.elevation = data_array[12]
        self.day_of_year = data_array[13]
        self.time = data_array[14]
