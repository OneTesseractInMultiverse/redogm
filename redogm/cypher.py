from redogm.abstractions import (
    CypherQueryResultConverter
)

from redisgraph.query_result import (
    QueryResult
)


# -----------------------------------------------------------------------------
# CLASS CYPHER QUERY RESULT TO DICTIONARY CONVERTER
# -----------------------------------------------------------------------------
class CypherQueryResultToDictionaryListConverter(CypherQueryResultConverter):

    __converted_results: list

    # -------------------------------------------------------------------------
    # CLASS CONSTRUCTOR
    # -------------------------------------------------------------------------
    def __init__(self, result: QueryResult, encoding='ascii'):
        """
        :type result: object
        """
        self.number_of_nodes = 0
        self.result_set = []
        self.encoding = encoding
        self.update(result)

    # -------------------------------------------------------------------------
    # METHOD VALIDATE RESULT SET
    # -------------------------------------------------------------------------
    def __validate_result_set(self, query_result):
        if query_result is not None:
            if not query_result.is_empty():
                self.result_set = query_result.result_set
                self.number_of_nodes = len(self.result_set) - 1
                return True
            self.number_of_nodes = 0
        return False

    # -------------------------------------------------------------------------
    # METHOD REMOVE COLUMN PREFIX
    # -------------------------------------------------------------------------
    @staticmethod
    def __remove_column_prefix(column_name):
        return column_name[column_name.find(".") + 1:]

    # -------------------------------------------------------------------------
    # METHOD DECODE COLUMN NAMES
    # -------------------------------------------------------------------------
    def __decode_column_names(self, column_list: list):
        columns = []
        for column in column_list:
            columns.append(self.__remove_column_prefix(column.decode(self.encoding)))
        return columns

    # -------------------------------------------------------------------------
    # METHOD DECODE AS INT
    # -------------------------------------------------------------------------
    @staticmethod
    def __decode_as_int(value: str):
        return int(value)

    # -------------------------------------------------------------------------
    # METHOD DECODE AS NONE
    # -------------------------------------------------------------------------
    @staticmethod
    def __decode_as_none():
        return None

    # -------------------------------------------------------------------------
    # METHOD DECODE AS FLOAT
    # -------------------------------------------------------------------------
    @staticmethod
    def __decode_as_float(value: str):
        return float(value)

    # -------------------------------------------------------------------------
    # METHOD IS NULL
    # -------------------------------------------------------------------------
    @staticmethod
    def __is_null(value: str) -> bool:
        return value == 'NULL'

    # -------------------------------------------------------------------------
    # METHOD IS INTEGER
    # -------------------------------------------------------------------------
    @staticmethod
    def __is_integer(value: str) -> bool:
        return value.isdigit()

    # -------------------------------------------------------------------------
    # METHOD IS FLOAT
    # -------------------------------------------------------------------------
    @staticmethod
    def __is_float(value: str) -> bool:
        return value.replace('.', '', 1).isdigit()

    # -------------------------------------------------------------------------
    # METHOD DECODE IF REQUIRED
    # -------------------------------------------------------------------------
    def __map_data_type(self, value):
        if isinstance(value, bytes):
            decoded_value = value.decode('ascii')
            if self.__is_null(decoded_value):
                return self.__decode_as_none()
            elif self.__is_integer(decoded_value):
                return self.__decode_as_int(decoded_value)
            elif self.__is_float(decoded_value):
                return self.__decode_as_float(decoded_value)
            return decoded_value
        return value

    # -------------------------------------------------------------------------
    # METHOD MAP RESULT SET TO DICTIONARY
    # -------------------------------------------------------------------------
    def __map_result_set_to_dictionary(self, result_list: list, column_list: list) -> dict:
        result_row = {}
        if len(result_list) == len(column_list):
            for index in range(len(column_list)):
                result_row[column_list[index]] = self.__map_data_type(result_list[index])
            return result_row
        else:
            raise IndexError("Mismatch between number of columns defined and columns inside result_row")

    # -------------------------------------------------------------------------
    # METHOD CONVERT QUERY RESULT TO DICT
    # -------------------------------------------------------------------------
    def __convert_query_result_to_list_of_dict(self, result_set: list) -> object:
        if len(result_set) > 1:
            columns = self.__decode_column_names(result_set[0])
            query_result = []
            # we iterate over the rows except the first column that contains the column names
            for row in result_set[1:]:
                query_result.append(self.__map_result_set_to_dictionary(row, columns))
            return query_result
        return []

    # -------------------------------------------------------------------------
    # METHOD ANY
    # -------------------------------------------------------------------------
    def any(self) -> bool:
        return self.number_of_nodes > 0

    # -------------------------------------------------------------------------
    # METHOD GET CONVERTED
    # -------------------------------------------------------------------------
    def get_results(self) -> list:
        return self.__converted_results

    # -------------------------------------------------------------------------
    # METHOD UPDATE
    # -------------------------------------------------------------------------
    def update(self, result: QueryResult) -> bool:
        self.__validate_result_set(result)
        self.__converted_results = []
        if self.any():
            self.__converted_results = self.__convert_query_result_to_list_of_dict(
                self.result_set
            )
            return True
        return False
