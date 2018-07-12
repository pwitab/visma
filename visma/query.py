import json

"""
THe aim of the query module is to enable adding query parameters to our API Calls
In the Visma API they use OData parameters to enable extensive filtering.
But they also give another way of adding the parameters to the URL than what is normaly used.

Query parameters is also not available on all endpoints.

We can only filter on specified attributes. standard should be model attributes.
If supplied filtering attributes use those instead. If supplied exlude attributes remove them from the standard one.

It should be possible to filter and order by.

we want to use Django standards. Customer.objects.filter(name__eq='MyName')

# To start with we should only handle AND cases. If we need OR functinallity we should implement it in a way simmular to Q objects in django.

exclude() should give Different from (not equal) -> odata ne

we want to be able to chain querysets. Customer.objects.filter(name__eq='MyName').filter(city='Helsingborg')


There should be a hook to transform the QuerySet to query parameters. So differnet APIs can use differnet methods.

Pagination.

By handling the data in a QuerySet before returning it should be possible for a
first implementation similar to the .iterator()

# we will not support selecting in the API. It messes with schema integrity.

# TODO: access to date functions.

psuedo-code

manager.filter() -> queryset.filter()
queryset -> basequeryset -> api-queryset
queryparam register in chain. -> allowed param? (exists in model). allowed method?
on eval queryset.compile_query_params

Actually no need for chainging of filtering. (well might as well do it..) Since we only support AND and we can't work with subsets and joins as in a db.
.filter(name__exact='Henrik', year__lt=2017).order_by('name')
same as:
.filter(name__exact='Henrik').filter(year__lt=2017).order_by('name')
"""


class QueryParam:

    def __init__(self, attribute, value, *args, **kwargs):
        self.attribute = attribute
        self.value = value


class APIModelIterable:

    def __init__(self, queryset):
        self.queryset = queryset

    def __iter__(self):
        queryset = self.queryset
        compiler = self.queryset.query.query_compiler(queryset.query)
        compiler.compile()
        endpoint = queryset.model.Meta.endpoint

        query_params = compiler.get_query_params()
        print(query_params)

        #api_result = queryset.api.get(endpoint, params=query_params).json()

        # test
        endpoint = endpoint + '?$filter=Id eq "91ff2390-968b-4ef7-877d-dd7aef616ae4"'

        api_result = queryset.api.get(endpoint).json()

        # TODO: Handle pagination
        if queryset.envelope:

            objs = queryset.envelope.load(api_result).data

        else:
            objs = queryset.schema.load(data=api_result, many=True)

        for obj in objs:
            yield obj


class APIQuerySet:

    def __init__(self, model, api, schema, query=None, envelope=None):
        self.model = model
        self.api = api
        self.schema = schema
        self.query = query or APIQuery(model=model,
                                       query_compiler=api.QUERY_COMPILER_CLASS)
        self.envelope = envelope

        self._iterable_class = APIModelIterable  # TODO: Implemnt pagination over this.
        # TODO: How to handle different pagination?
        self._result_cache = None

    def __iter__(self):

        self._fetch_all()
        return iter(self._result_cache)

    def filter(self, **kwargs):
        """
        Return a new QuerySet instance with the args ANDed to the existing
        set.
        """
        return self._filter_or_exclude(False, **kwargs)

    def exclude(self, **kwargs):
        """
        Return a new QuerySet instance with NOT (args) ANDed to the existing
        set.
        """
        return self._filter_or_exclude(True, **kwargs)

    def _filter_or_exclude(self, negate, **kwargs):
        clone = self._chain()

        clone.query.add_filter(negate, **kwargs)

        return clone

    def order_by(self, field_name):
        """Return a new QuerySet instance with the ordering changed."""
        obj = self._chain()
        obj.query.add_ordering(field_name)
        return obj

    def first(self):
        """Return the first object of a query or None if no match is found."""
        pass

    def _chain(self, **kwargs):
        """
        Return a copy of the current QuerySet that's ready for another
        operation.
        """
        obj = self._clone()
        obj.__dict__.update(kwargs)
        return obj

    def _clone(self):
        """
        Return a copy of the current QuerySet. A lightweight alternative
        to deepcopy().
        """
        c = self.__class__(model=self.model, query=self.query.chain(),
                           api=self.api, schema=self.schema,
                           envelope=self.envelope)
        return c

    def _fetch_all(self):
        if self._result_cache is None:
            self._result_cache = list(self._iterable_class(self))


class APIQuery:

    def __init__(self, model, query_compiler=None):
        self.model = model
        self.query_compiler = query_compiler or QueryCompiler
        self.filter_by = {}
        self.exclude_by = {}
        self.order_by = []

    def add_filter(self, negate, **kwargs):
        # TODO: Validate that it is possible to filter.
        if negate:
            self.exclude_by.update(**kwargs)
        else:
            self.filter_by.update(**kwargs)

    def add_ordering(self, field_name):
        # TODO: Validate it is possible to order by.
        """Will keep all the fields"""
        self.order_by.append(field_name)

    def chain(self, klass=None):
        """
        Return a copy of the current Query that's ready for another operation.
        The klass argument changes the type of the Query, e.g. UpdateQuery.
        """
        obj = self.clone()
        if klass and obj.__class__ != klass:
            obj.__class__ = klass

        return obj

    def clone(self):
        """
        Return a copy of the current Query. A lightweight alternative to
        to deepcopy().
        """
        c = self.__class__(model=self.model, query_compiler=self.query_compiler)
        c.filter_by = self.filter_by
        c.exclude_by = self.exclude_by
        c.order_by = self.order_by
        return c


class Param:
    allowed_value_instances = []

    def __init__(self, key, value, parser):
        self.key = key
        self.value = value
        self.validate()
        self.parser = parser(key, value)

    def validate(self):
        if type(self.value) not in self.allowed_value_instances:
            raise ValueError(f'Value {self.value} of type {self.value.__class__} '
                             f'and filter operation '
                             f'{self.__class__} not interoperable')

    def parse(self):
        return self.parser.parse()

    # TODO: Is parse the right word?


class Equals(Param):
    allowed_value_instances = [int, float, str]


class NotEquals(Param):
    allowed_value_instances = [int, float, str]


class GreaterThan(Param):
    allowed_value_instances = [int, float]


class GreaterThanOrEqual(Param):
    allowed_value_instances = [int, float]


class LessThan(Param):
    allowed_value_instances = [int, float]


class LessThanOrEquals(Param):
    allowed_value_instances = [int, float]


# TODO: Add string comparison funtions and date functions.

class ParamParser:
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def parse(self):
        raise NotImplementedError(f'The parse function on {self.__class__} '
                                  f'needs to be overridden')


class NoneParamParser(ParamParser):

    def parse(self):
        return ''


class QueryCompiler:
    """
    The QueryCompiler takes the filtering and excluding and ordering by options
    and return a query parameter string.
    """

    # TODO: What is a good standard parser?
    equals_parser_class = NoneParamParser
    not_equals_parser_class = NoneParamParser
    greater_than_parser_class = NoneParamParser
    greater_or_equal_parser_class = NoneParamParser
    less_than_parser_class = NoneParamParser
    less_or_equal_parser_class = NoneParamParser

    order_by_parser_class = NoneParamParser

    filter_param = '$filter'
    order_param = '$order_by'

    def __init__(self, query):
        self.query = query
        self.filters = list()
        self.order = None
        print(self.filter_map)

    @property
    def filter_map(self):
        return {
            'exact': (Equals, self.equals_parser_class),
            'not': (NotEquals, self.not_equals_parser_class),
            'gt': (GreaterThan, self.greater_than_parser_class),
            'gte': (GreaterThanOrEqual, self.greater_or_equal_parser_class),
            'lt': (LessThan, self.less_than_parser_class),
            'lte': (LessThanOrEquals, self.less_or_equal_parser_class)

        }

    @property
    def exclude_map(self):
        return {
            'exact': (NotEquals, self.not_equals_parser_class),
            'not': (Equals, self.equals_parser_class),
            'gt': (LessThan, self.less_than_parser_class),
            'gte': (LessThanOrEquals, self.less_or_equal_parser_class),
            'lt': (GreaterThan, self.greater_than_parser_class),
            'lte': (GreaterThanOrEqual, self.greater_or_equal_parser_class),
        }

    def compile(self):
        self.parse_kwarg(self.query.filter_by, self.filter_map)
        self.parse_kwarg(self.query.exclude_by, self.exclude_map)
        self.parse_order(self.query.order_by)

    def parse_order(self, order_list):
        # get the last called order by
        order_val = order_list[-1]
        self.order = self.order_by_parser_class(self.order_param, order_val)

    def get_filter_string(self):
        filter_params = [_filter.parse() for _filter in self.filters]
        filter_string = self.join_filter_params(filter_params)
        return filter_string

    def get_order_string(self):
        return self.order.parse()

    def get_query_params(self):

        query_params = dict()

        if self.filters:
            query_params.update({self.filter_param: self.get_filter_string()})

        if self.query.order_by:
            # get the last order by reference
            query_params.update({self.order_param: self.get_order_string()})

        return query_params

    @staticmethod
    def join_filter_params(param_list):
        # TODO: This is VISMA API dependant. Should be defined in the VIsmaAPICompiler.
        filter_string = ' and '.join(param_list)
        return filter_string

    def parse_kwarg(self, param_dict, mapping):
        """
        Will parse a key, ex name_equal=13 to attr name and function equal
        value 13.
        No function defaults to equals.
        Or size__gte, attr size, function greaterthanorequal
        :returns: Param
        """
        for filtering_attr, value in param_dict.items():
            filter_class = None
            key = None
            parser = None
            settings = filtering_attr.split('__')

            if len(settings) == 1:
                #  No __ in expression. Assume exact
                key = settings[0]
                filter_class = mapping.get('exact')[0]
                parser = mapping.get('exact')[1]
            elif len(settings) == 2:
                key, klass = settings
                filter_class = mapping.get(klass)[0]
                parser = mapping.get(klass)[1]

            if filter_class:
                print()
                self.filters.append(filter_class(key=key,
                                                 value=value,
                                                 parser=parser))
