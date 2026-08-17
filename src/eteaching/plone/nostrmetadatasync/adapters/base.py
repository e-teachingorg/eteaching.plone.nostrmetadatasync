import hashlib

from eteaching.plone.nostrmetadatasync.utils import replace_base_url


class NostrEventMixin:
    """Common methods for various event adapters."""

    def uid(self):
        s = self.context.UID()
        return hashlib.sha256(s.encode()).hexdigest()

    def content(self):
        return self.context.description

    def _title(self):
        return self.context.title

    def _description(self):
        return self.context.description

    def _url(self):
        url = self.context.absolute_url()
        return replace_base_url(url)

    def _expand_tags(self, *tags):
        """Respect flattening rules
        1. ("keywords": ("Math", "Physics"))
        ---> ("t", "Math"), ("t", "Physics")
        2. ('creator', ({'id': 'ka', 'name': 'Karl'},
        {'id': 'tr', 'name': 'Trude'}))
        ---> ('creator:id', 'ka'), ('creator:name', 'Karl'),
        ('creator:id', 'tr'), ('creator:name', 'Trude')
        3. ('creator', ({'name': 'Karl'}, {'name': 'Trude'}))
        ---> ('creator:name', 'Karl'), ('creator:name', 'Trude')
        """
        result = []

        def flatten(prefix, obj):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    yield from flatten(f"{prefix}:{k}", v)
            elif isinstance(obj, (tuple, list)) and not isinstance(
                obj, str
            ):  # Iterable
                for v in obj:
                    yield from flatten(prefix, v)
            else:  # Simple value
                yield (prefix, obj)

        for tag in tags:

            if len(tag) != 2:
                result.append(tag)
                continue

            key, value = tag

            # Iterable
            if isinstance(value, (tuple, list)) and not isinstance(value, str):
                for v in value:
                    # Dict or simple value
                    result += list(flatten(key, v))
                continue

            # Simple Dict
            if isinstance(value, dict):
                result += list(flatten(key, value))
                continue

            # Simple Value
            result.append((key, value))

        return tuple(result)
