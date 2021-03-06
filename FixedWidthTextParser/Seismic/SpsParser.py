"""
    SPS Parser
"""
from FixedWidthTextParser.Parser import Parser


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


class Relation:
    def __init__(self, data_array):
        self.type = data_array[0]
        self.tape = data_array[1]
        self.ffid = data_array[2]
        self.ffid_increment = data_array[3]
        self.instrument = data_array[4]
        self.line = data_array[5]
        self.point = data_array[6]
        self.point_idx = data_array[7]
        self.from_channel = data_array[8]
        self.to_channel = data_array[9]
        self.channel_increment = data_array[10]
        self.rcv_line = data_array[11]
        self.from_rcv = data_array[12]
        self.to_rcv = data_array[13]
        self.rcv_idx = data_array[14]


class SpsParser(Parser):
    def __init__(self, point_def: dict, relation_def: dict):
        super().__init__()
        self._point_def = point_def
        self._relation_def = relation_def

    def parse_point(self, text_line):
        """
        Parser SPS Point record
        :param text_line:
        :return:
        """
        record_type = self.substr(text_line, self._point_def['RECORD_ID'][0], self._point_def['RECORD_ID'][1]).strip()
        if record_type not in (SRC_DATA_RECORD, RCV_DATA_RECORD):
            return
        self.set_definition(self._point_def)
        return self.parse(text_line)

    def parse_point2obj(self, text_line):
        data = self.parse_point(text_line)

        if data is not None:
            return Point(data)
        else:
            return

    def parse_relation(self, text_line):
        """
        Parser SPS Relation record
        :param text_line:
        :return:
        """
        record_type = self.substr(text_line, self._point_def['RECORD_ID'][0], self._point_def['RECORD_ID'][1]).strip()
        if REL_DATA_RECORD != record_type:
            return

        self.set_definition(self._relation_def)
        return self.parse(text_line)

    def get_fields_point(self):
        """
        Get Point fields description
        :return:
        """
        self.set_definition(self._point_def)
        return self.get_fields()

    def get_fields_relation(self):
        """
        Get Relation fields description
        :return:
        """
        self.set_definition(self._relation_def)
        return self.get_fields()


SRC_DATA_RECORD = 'S'
RCV_DATA_RECORD = 'R'
REL_DATA_RECORD = 'X'
HEADER_RECORD = 'H'


class Sps21Parser(SpsParser):
    """
        SPS version 2.1 Parser
    """
    POINT_DEF = {
        'RECORD_ID': [0, 1, 'string'],
        'LINE': [1, 10, 'float'],
        'POINT': [11, 10, 'float'],
        'POINT_IDX': [23, 1, 'integer', 1],
        'POINT_CODE': [24, 2, 'string'],
        'STATIC_COR': [26, 4, 'integer'],
        'POINT_DEPTH': [30, 4, 'float'],
        'DATUM': [34, 4, 'integer'],
        'UPHOLE_TIME': [38, 2, 'integer'],
        'WATER_DEPTH': [40, 6, 'float'],
        'EASTING': [46, 9, 'float'],
        'NORTHING': [55, 10, 'float'],
        'ELEVATION': [65, 6, 'float'],
        'DAY_OF_YEAR': [71, 3, 'integer'],
        'TIME': [74, 6, 'string'],
    }
    RELATION_DEF = {
        'RECORD_ID': [0, 1, 'string'],
        'TAPE_NUMBER': [1, 6, 'string'],
        'RECORD_NUMBER': [7, 8, 'integer'],
        'RECORD_INCREMENT': [15, 1, 'integer', 1],
        'INSTRUMENT_CODE': [16, 1, 'string', '1'],
        'S_LINE': [17, 10, 'float'],
        'POINT': [27, 10, 'float'],
        'POINT_IDX': [37, 1, 'integer'],
        'FROM_CHANNEL': [38, 5, 'integer'],
        'TO_CHANNEL': [43, 5, 'integer'],
        'CHANNEL_INCREMENT': [48, 1, 'float'],
        'R_LINE': [49, 10, 'float'],
        'FROM_RECEIVER': [59, 10, 'float'],
        'TO_RECEIVER': [69, 10, 'float'],
        'RECEIVER_IDX': [79, 1, 'integer'],
    }

    def __init__(self, point_def=None, relation_def=None):
        if point_def is None:
            point_def = self.POINT_DEF
        if relation_def is None:
            relation_def = self.RELATION_DEF
        super().__init__(point_def, relation_def)

    def format_point(self, point: Point):
        """ get formatted sps string from Point objects"""
        pattern = "%1s%10.2f%10.2f  %1d%2s            %2d      %9.1f%10.1f%6.1f%3d%6s"

        return pattern % (
            point.type,
            point.line,
            point.point,
            point.point_idx,
            point.point_code if point.point_code is not None else '',
            point.uphole_time if point.uphole_time is not None else 0,
            point.easting,
            point.northing,
            point.elevation if point.elevation is not None else 0.0,
            point.day_of_year if point.day_of_year is not None else 0,
            point.time if point.time is not None else ''
        )


class Sps00Parser(SpsParser):
    """
        SPS Parser of first version
    """
    POINT_DEF = {
        'RECORD_ID': [0, 1, 'string'],
        'LINE': [1, 16, 'float'],
        'POINT': [17, 8, 'float'],
        'POINT_IDX': [25, 1, 'integer', 1],
        'POINT_CODE': [26, 2, 'string'],
        'STATIC_COR': [28, 4, 'integer'],
        'POINT_DEPTH': [32, 4, 'float'],
        'DATUM': [36, 4, 'integer'],
        'UPHOLE_TIME': [40, 2, 'integer'],
        'WATER_DEPTH': [42, 4, 'float'],
        'EASTING': [46, 9, 'float'],
        'NORTHING': [55, 10, 'float'],
        'ELEVATION': [65, 6, 'float'],
        'DAY_OF_YEAR': [71, 3, 'integer'],
        'TIME': [74, 6, 'string'],
    }
    RELATION_DEF = {}

    def __init__(self, point_def=None, relation_def=None):
        if point_def is None:
            point_def = self.POINT_DEF
        if relation_def is None:
            relation_def = self.RELATION_DEF
        super().__init__(point_def, relation_def)
