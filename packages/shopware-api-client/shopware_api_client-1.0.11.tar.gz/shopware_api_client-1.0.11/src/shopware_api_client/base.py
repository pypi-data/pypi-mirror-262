import json
from typing import Any, AsyncGenerator, Generic, Self, Type, TypeVar, overload

import httpx
from pydantic import BaseModel

from .endpoints.base_fields import IdField
from .exceptions import SWAPIError, SWFilterException, SWNoClientProvided
from .logging import logger

EndpointClass = TypeVar("EndpointClass", bound="EndpointBase[Any]")
ModelClass = TypeVar("ModelClass", bound="ApiModelBase[Any]")


class ConfigBase:
    def __init__(self, url: str):
        self.url = url.rstrip("/")


class ClientBase:
    api_url: str
    raw: bool

    def __init__(self, config: ConfigBase, raw: bool = False):
        self.api_url = config.url
        self.raw = raw

    async def __aenter__(self) -> "Self":
        self._get_client()
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self._get_client().aclose()

    async def log_request(self, request: httpx.Request) -> None:
        logger.debug(f"Request: {request.method} {request.url} - {request.content!r} <headers: {request.headers}>")

    async def log_response(self, response: httpx.Response) -> None:
        await response.aread()
        logger.debug(
            f"Response: {response.status_code} - {response.status_code} - {response.content!r} "
            f"<headers: {response.headers}>"
        )

    def _get_client(self) -> httpx.AsyncClient:
        raise NotImplementedError()

    @staticmethod
    def _get_headers() -> dict[str, str]:
        return {"Content-Type": "application/json", "Accept": "application/vnd.api+json"}

    async def _make_request(self, method: str, relative_url: str, **kwargs: Any) -> httpx.Response:
        if relative_url.startswith("http://") or relative_url.startswith("https://"):
            url = relative_url
        else:
            url = f"{self.api_url}{relative_url}"
        client = self._get_client()

        headers = self._get_headers()
        headers.update(kwargs.pop("headers", {}))

        response = await client.request(method, url, headers=headers, **kwargs)

        if response.status_code >= 400:
            try:
                raise SWAPIError(response.json().get("errors"))
            except json.JSONDecodeError:
                raise SWAPIError(f"Status: {response.status_code}: {response.text}")

        return response

    async def get(self, relative_url: str, **kwargs: Any) -> httpx.Response:
        return await self._make_request(method="GET", relative_url=relative_url, **kwargs)

    async def post(self, relative_url: str, **kwargs: Any) -> httpx.Response:
        # we need to set a response type, otherwise we don't get one
        relative_url += "?_response=basic"
        return await self._make_request(method="POST", relative_url=relative_url, **kwargs)

    async def patch(self, relative_url: str, **kwargs: Any) -> httpx.Response:
        # we need to set a reponse type, otherwise we don't get one
        relative_url += "?_response=basic"
        return await self._make_request(method="PATCH", relative_url=relative_url, **kwargs)

    async def delete(self, relative_url: str, **kwargs: Any) -> httpx.Response:
        return await self._make_request(method="DELETE", relative_url=relative_url, **kwargs)

    async def close(self) -> None:
        await self._get_client().aclose()

    async def bulk_upsert(
        self, name: str, objs: list[ModelClass] | list[dict[str, Any]], **request_kwargs: dict[str, Any]
    ) -> dict[str, Any] | None:
        raise Exception("bulk_upsert is only supported in the admin API")

    async def bulk_delete(
        self, name: str, objs: list[ModelClass] | list[dict[str, Any]], **request_kwargs: dict[str, Any]
    ) -> dict[str, Any]:
        raise Exception("bulk_delete is only supported in the admin API")


class ApiModelBase(BaseModel, Generic[EndpointClass]):
    _identifier: str

    id: IdField | None

    def __init__(self, client: ClientBase | None = None, **kwargs: dict[str, Any]) -> None:
        super().__init__(**kwargs)
        self._client = client

    @classmethod
    def using(cls: type[Self], client: ClientBase) -> EndpointClass:
        # we want a fresh endpoint
        endpoint: EndpointClass = getattr(client, cls._identifier.get_default()).__class__(client)  # type: ignore
        return endpoint

    def _get_client(self) -> ClientBase:
        if self._client is None:
            raise SWNoClientProvided("Model has no api client set. Use `using` to set a client.")
        return self._client

    def _get_endpoint(self) -> EndpointClass:
        # we want a fresh endpoint
        endpoint: EndpointClass = getattr(self._get_client(), self._identifier).__class__(self._get_client())  # type: ignore
        return endpoint

    async def save(self) -> Self | dict:
        endpoint = self._get_endpoint()

        if self.id is None:
            result = await endpoint.create(obj=self)
        else:
            result = await endpoint.update(pk=self.id, obj=self)

        return result

    async def delete(self) -> bool:
        endpoint = self._get_endpoint()

        # without id we can't delete
        if self.id is None:
            return False

        return await endpoint.delete(pk=self.id)


class EndpointBase(Generic[ModelClass]):
    name: str
    path: str
    model_class: Type[ModelClass]
    raw: bool

    def __init__(self, client: ClientBase):
        self.client = client
        self.raw = client.raw
        self._filter: list[dict[str, Any]] = []
        self._limit: int | None = None
        self._sort: list[dict[str, Any]] = []

    def _is_search_query(self) -> bool:
        return len(self._filter) > 0 or len(self._sort) > 0

    def _get_data_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {}

        if len(self._filter) > 0:
            data["filter"] = self._filter

        if len(self._sort) > 0:
            data["sort"] = self._sort

        if self._limit is not None:
            data["limit"] = self._limit

        return data

    def _reset_endpoint(self) -> None:
        self._filter = []
        self._limit = None
        self._sort = []

    @overload
    def _parse_response(self, data: list[dict[str, Any]]) -> list[ModelClass]:
        pass

    @overload
    def _parse_response(self, data: dict[str, Any]) -> ModelClass:
        pass

    def _parse_response(self, data: list[dict[str, Any]] | dict[str, Any]) -> list[ModelClass] | ModelClass:
        single = False

        if isinstance(data, dict):
            single = True
            data = [data]

        result_list: list[ModelClass] = []

        for entry in data:
            api_type = entry.get("type", None)

            if api_type is None:
                model_class = self.model_class
            else:
                model_class = getattr(self.client, api_type).model_class

            if "attributes" in entry:
                obj = model_class(client=self.client, id=entry["id"], **entry["attributes"])
            else:
                obj = model_class(client=self.client, **entry)

            result_list.append(obj)

        if single:
            return result_list[0]

        return result_list

    def _parse_data(self, response_dict: dict[str, Any]) -> list[dict[str, Any]]:
        if "data" in response_dict:
            key = "data"
        elif "elements" in response_dict:
            key = "elements"
        else:
            key = None

        data: list[dict[str, Any]] | dict[str, Any] = response_dict[key] if key else response_dict

        if isinstance(data, dict):
            return [data]

        return data

    def _prase_data_single(self, reponse_dict: dict[str, Any]) -> dict[str, Any]:
        return self._parse_data(reponse_dict)[0]

    async def all(self) -> list[ModelClass] | list[dict[str, Any]]:
        data = self._get_data_dict()

        if self._is_search_query():
            result = await self.client.post(f"/search{self.path}", json=data)
        else:
            result = await self.client.get(f"{self.path}", params=data)

        result_data: list[dict[str, Any]] = self._parse_data(result.json())

        self._reset_endpoint()

        if self.raw:
            return result_data

        return self._parse_response(result_data)

    async def get(self, pk: str) -> ModelClass | dict[str, Any]:
        result = await self.client.get(f"{self.path}/{pk}")
        result_data: dict[str, Any] = self._prase_data_single(result.json())

        if self.raw:
            return result_data

        return self._parse_response(result_data)

    async def update(self, pk: str, obj: ModelClass | dict[str, Any]) -> ModelClass | dict[str, Any]:
        if isinstance(obj, ApiModelBase):
            data = obj.model_dump_json(by_alias=True)
        else:
            data = json.dumps(obj)

        result = await self.client.patch(f"{self.path}/{pk}", data=data)
        result_data: dict[str, Any] = self._prase_data_single(result.json())

        if self.raw:
            return result_data

        return self._parse_response(result_data)

    async def first(self) -> ModelClass | dict[str, Any] | None:
        self._limit = 1
        result = await self.all()

        self._reset_endpoint()

        # return None instead of an KeyError, if result is empty
        if len(result) == 0:
            return None

        return result[0]

    async def create(self, obj: ModelClass | dict[str, Any]) -> ModelClass | dict[str, Any]:
        if isinstance(obj, ApiModelBase):
            data = obj.model_dump_json(by_alias=True)
        else:
            data = json.dumps(obj)

        result = await self.client.post(f"{self.path}", data=data)
        result_data: dict[str, Any] = self._prase_data_single(result.json())

        if self.raw:
            return result_data

        return self._parse_response(result_data)

    async def delete(self, pk: str) -> bool:
        response = await self.client.delete(f"{self.path}/{pk}")

        if response.status_code == 204:
            return True

        return False

    async def get_related(self, parent: ModelClass, relation: str) -> list[ModelClass] | list[dict[str, Any]]:
        parent_endpoint = parent._get_endpoint()
        result = await self.client.get(f"{parent_endpoint.path}/{parent.id}/{relation}")
        result_data: list[dict[str, Any]] = self._parse_data(result.json())

        if self.raw:
            return result_data

        return self._parse_response(result_data)

    def filter(self, **kwargs: str) -> Self:
        for key, value in kwargs.items():
            filter_term = ""
            filter_type = "equals"

            field_parts = key.split("__")

            if len(field_parts) > 1:
                filter_term = field_parts[-1]

                match filter_term:
                    case "in":
                        filter_type = "equalsAny"
                    case "contains":
                        filter_type = "contains"
                    case "gt":
                        filter_type = "range"
                    case "gte":
                        filter_type = "range"
                    case "lt":
                        filter_type = "range"
                    case "lte":
                        filter_type = "range"
                    case "range":
                        filter_type = "range"
                    case "startswith":
                        filter_type = "prefix"
                    case "endswith":
                        filter_type = "suffix"
                    case _:
                        filter_term = ""

            if field_parts[0] not in self.model_class.model_fields:
                raise SWFilterException(
                    f"Unknown Field: {field_parts[0]}. Available fields: {self.model_class.model_fields.keys()}"
                )

            if filter_term != "":
                field_parts = field_parts[:-1]

            # Todo: Maybe add filter over related attributes
            if len(field_parts) >= 2:
                field = "%s.%s" % (
                    self.model_class.model_fields[field_parts[0]].alias or field_parts[0],
                    ".".join(field_parts[1:]),
                )
            else:
                field = self.model_class.model_fields[field_parts[0]].alias or field_parts[0]

            parameters = {}

            # range has additional parameters
            if filter_type == "range":
                if filter_term == "range":
                    parameters = {"gte": value[0], "lte": value[1]}
                else:
                    parameters = {filter_term: value}

            self._filter.append({"type": filter_type, "field": field, "value": value, "parameters": parameters})

        return self

    async def bulk_upsert(
        self, objs: list[ModelClass] | list[dict[str, Any]], **request_kwargs: dict[str, Any]
    ) -> dict[str, Any] | None:
        return await self.client.bulk_upsert(self.name, objs, **request_kwargs)

    async def bulk_delete(
        self, objs: list[ModelClass] | list[dict[str, Any]], **request_kwargs: dict[str, Any]
    ) -> dict[str, Any]:
        return await self.client.bulk_delete(self.name, objs, **request_kwargs)

    def limit(self, count: int | None) -> "Self":
        self._limit = count
        return self

    def order_by(self, fields: str | tuple[str]) -> "Self":
        if isinstance(fields, str):
            fields = (fields,)

        for field in fields:
            if field.startswith("-"):
                field = field[1:]
                order = "DESC"
            else:
                order = "ASC"

            if field not in self.model_class.model_fields:
                raise SWFilterException(
                    f"Unknown Field: {field}. Available fields: " f"{self.model_class.model_fields.keys()}"
                )
            else:
                field = self.model_class.model_fields[field].alias or field

            self._sort.append({"field": field, "order": order})

        return self

    async def iter(self, batch_size: int = 100) -> AsyncGenerator[ModelClass | dict[str, Any], None]:
        self._limit = batch_size
        data = self._get_data_dict()
        page = 1

        if self._is_search_query():
            url = f"/search{self.path}"
        else:
            url = self.path

        while True:
            data["page"] = page
            if self._is_search_query():
                result = await self.client.post(url, json=data)
            else:
                result = await self.client.get(url, params=data)

            result_dict: dict[str, Any] = result.json()
            result_data: list[dict[str, Any]] = self._parse_data(result_dict)

            for entry in result_data:
                if self.raw:
                    yield entry
                else:
                    yield self._parse_response(entry)

            if "next" in result_dict.get("links", {}) and len(result_data) > 0:
                page += 1
            else:
                break
