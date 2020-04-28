from rest_framework import serializers
from rest_framework.schemas.openapi import AutoSchema
from rest_framework.schemas.utils import is_list_view


class MinutesSchema(AutoSchema):
    def get_components(self, path, method):
        components = super().get_components(path, method)
        if is_list_view(path, method, self.view):
            component_name = self.get_component_name(self.get_serializer(path, method))
            response_component_name = self.get_response_name(path, method)
            components[response_component_name] = self.get_paginator().get_paginated_response_schema({
                'type': 'array',
                'items': {
                    '$ref': '#/components/schemas/{0}'.format(component_name)
                }
            })
        return components

    def get_response_name(self, path, method):
        return '{0}Response'.format(self.get_component_name(self.get_serializer(path, method)))

    def get_responses(self, path, method):
        if method == 'DELETE':
            return {
                '204': {
                    'description': ''
                }
            }

        self.response_media_types = self.map_renderers(path, method)

        serializer = self.get_serializer(path, method)

        if not isinstance(serializer, serializers.Serializer):
            item_schema = {}
        else:
            item_schema = self._get_reference(serializer)
        if is_list_view(path, method, self.view):
            response_schema = {
                'type': 'array',
                'items': item_schema,
            }
            paginator = self.get_paginator()
            if paginator:
                response_schema = {'$ref': '#/components/schemas/{0}'.format(self.get_response_name(path, method))}
        else:
            response_schema = item_schema
        status_code = '201' if method == 'POST' else '200'
        return {
            status_code: {
                'content': {
                    ct: {'schema': response_schema}
                    for ct in self.response_media_types
                },
                # description is a mandatory property,
                # https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md#responseObject
                # TODO: put something meaningful into it
                'description': ""
            }
        }
