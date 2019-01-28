from abc import (
    ABCMeta,
    abstractmethod
)


# -----------------------------------------------------------------------------
# CLASS CYPHER QUERY RESULT CONVERTER
# -----------------------------------------------------------------------------
class CypherQueryResultConverter(object):

    """

        An abstract class that works as a common interface that must be
        implemented across any implementation of CypherQueryResultConverter.
        A CypherQueryResultConverter converts that result_set returned in a
        CypherQuery into another structure easier to manipulate or to map into
        objects.

    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def update(self, result) -> bool:
        pass

    @abstractmethod
    def any(self) -> bool:
        pass

    @abstractmethod
    def get_results(self) -> list:
        pass

