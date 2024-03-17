import graphene


class CountableConnection(graphene.relay.Connection):
    class Meta:
        abstract = True

    total_count = graphene.Int()

    def resolve_total_count(self, info, **kwargs) -> int:
        return self.iterable.count()  # type: ignore
