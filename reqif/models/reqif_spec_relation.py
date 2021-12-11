class ReqIFSpecRelation:
    def __init__(
        self, identifier: str, relation_type_ref, source: str, target: str
    ):
        self.identifier: str = identifier
        self.relation_type_ref = relation_type_ref
        self.source: str = source
        self.target: str = target
