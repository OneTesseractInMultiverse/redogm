class RNode:

    def __eq__(self, other):
        if not isinstance(other, (RNode,)):
            return False
        if hasattr(self, 'id') and hasattr(other, 'id'):
            return self.id == other.id
