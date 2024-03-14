import json
import os
from dataclasses import dataclass
from typing import Any, Mapping, Optional, Union

import requests
from orchestrate._internal.exceptions import (
    OrchestrateClientError,
    OrchestrateHttpError,
)
from orchestrate._internal.fhir import Bundle


def _get_priority_base_url() -> str:
    if "ORCHESTRATE_BASE_URL" in os.environ:
        return os.environ["ORCHESTRATE_BASE_URL"]
    return "https://api.careevolutionapi.com"


def _get_priority_api_key(api_key: Optional[str]) -> Optional[str]:
    if api_key is not None:
        return api_key
    if "ORCHESTRATE_API_KEY" in os.environ:
        return os.environ["ORCHESTRATE_API_KEY"]
    return None


def _get_additional_headers() -> Mapping[str, str]:
    if "ORCHESTRATE_ADDITIONAL_HEADERS" in os.environ:
        return json.loads(os.environ["ORCHESTRATE_ADDITIONAL_HEADERS"])
    return {}


@dataclass
class _OperationalOutcomeIssue:
    severity: str
    code: str
    diagnostics: str

    def __str__(self) -> str:
        return f"{self.severity}: {self.code} - {self.diagnostics}"


def _read_json_outcomes(response: requests.Response) -> list[_OperationalOutcomeIssue]:
    try:
        json_response = response.json()
        if "issue" in json_response:
            return [
                _OperationalOutcomeIssue(
                    issue.get("severity", ""),
                    issue.get("code", ""),
                    issue.get("diagnostics", ""),
                )
                for issue in json_response["issue"]
            ]
        if (
            json_response.get("type")
            == "https://tools.ietf.org/html/rfc9110#section-15.5.1"
        ):
            return [
                _OperationalOutcomeIssue(
                    severity="error",
                    code=json_response.get("title", ""),
                    diagnostics=json_response.get("detail", ""),
                )
            ]
    except Exception:
        pass

    return []


def _read_operational_outcomes(response: requests.Response) -> list[str]:
    outcomes = _read_json_outcomes(response)
    if outcomes:
        return [str(outcome) for outcome in outcomes]

    return [response.text]


def _exception_from_response(response: requests.Response) -> OrchestrateHttpError:
    operational_outcomes = _read_operational_outcomes(response)
    if response.status_code >= 400 and response.status_code < 600:
        return OrchestrateClientError(response.text, operational_outcomes)
    return OrchestrateHttpError()


def _prepare_body(body: Union[bytes, str, Mapping[Any, Any]]) -> bytes:
    if isinstance(body, dict):
        return json.dumps(body).encode("utf-8")
    if isinstance(body, str):
        return body.encode("utf-8")

    return body  # type: ignore


class HttpHandler:
    def __init__(
        self,
        base_url: str,
        default_headers: dict,
    ) -> None:
        self.base_url = base_url
        self.__default_headers = default_headers

    def __repr__(self) -> str:
        return f"HttpHandler(base_url={self.base_url})"

    def __merge_headers(self, headers: Optional[dict]) -> dict:
        if headers is None:
            return self.__default_headers
        return {**self.__default_headers, **headers}

    def post(
        self,
        path: str,
        body: Union[str, Mapping[Any, Any], bytes],
        headers: Optional[dict[str, str]] = None,
        parameters: Optional[Mapping[str, Optional[str]]] = None,
    ) -> Any:
        request_headers = self.__merge_headers(headers)

        prepared_body = _prepare_body(body)
        url = f"{self.base_url}{path}"

        response = requests.post(
            url,
            data=prepared_body,
            headers=request_headers,
            params=parameters,
        )
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as http_error:
            raise _exception_from_response(response) from http_error

        if (
            request_headers["Accept"] in ["application/zip", "application/pdf"]
        ) and response.content:
            return response.content

        if (request_headers["Accept"] == "application/json") and response.text:
            return response.json()

        return response.text

    def get(
        self,
        path: str,
        headers: Optional[dict] = None,
        parameters: Optional[Mapping[str, Optional[str]]] = None,
    ) -> Any:
        request_headers = self.__merge_headers(headers)

        url = f"{self.base_url}{path}"
        response = requests.get(
            url,
            headers=request_headers,
            params=parameters,
        )
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as http_error:
            raise _exception_from_response(response) from http_error

        if (request_headers["Accept"] == "application/json") and response.text:
            return response.json()

        return response.text


def create_http_handler(api_key: Optional[str] = None) -> HttpHandler:
    additional_headers = _get_additional_headers()
    base_url = _get_priority_base_url()
    default_headers = {
        **(additional_headers or {}),
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    priority_api_key = _get_priority_api_key(api_key)
    if priority_api_key is not None:
        default_headers["x-api-key"] = priority_api_key

    return HttpHandler(
        base_url=base_url,
        default_headers=default_headers,
    )
