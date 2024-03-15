import json
from typing import Annotated, Any, List, Optional, Union

from gable.client import GableClient, del_none
from gable.openapi import (
    CheckDataAssetCommentMarkdownResponse,
    CheckDataAssetDetailedResponse,
    CheckDataAssetErrorResponse,
    CheckDataAssetMissingAssetResponse,
    CheckDataAssetNoContractResponse,
    ErrorResponse,
    Input,
    ResponseType,
    ResponseType1,
    ResponseType2,
    ResponseType3,
    ResponseType4,
)
from gable.options import DATABASE_SOURCE_TYPE_VALUES, FILE_SOURCE_TYPE_VALUES
from pydantic import Field, parse_obj_as

# Discriminated union for the response from the /data-assets/check endpoint
CheckDataAssetDetailedResponseUnion = Annotated[
    Union[
        CheckDataAssetDetailedResponse,
        CheckDataAssetErrorResponse,
        CheckDataAssetNoContractResponse,
        CheckDataAssetMissingAssetResponse,
    ],
    Field(discriminator="responseType"),
]


def post_data_assets_check_requests(
    client: GableClient,
    responseType: ResponseType,
    source_type: str,
    source_names: List[str],
    realDbName: str,
    realDbSchema: str,
    schema_contents: List[str],
) -> Union[
    ErrorResponse,
    CheckDataAssetCommentMarkdownResponse,
    list[
        Union[
            CheckDataAssetDetailedResponse,
            CheckDataAssetErrorResponse,
            CheckDataAssetNoContractResponse,
            CheckDataAssetMissingAssetResponse,
        ]
    ],
]:
    requests = build_check_data_asset_inputs(
        source_type=source_type,
        source_names=source_names,
        schema_contents=schema_contents,
        realDbName=realDbName,
        realDbSchema=realDbSchema,
    )

    inputs = [del_none(input.dict()) for input in requests.values()]
    request = {
        "responseType": responseType.value,
        "inputs": inputs,
    }

    result = client.post_data_assets_check(request)
    if responseType == ResponseType.DETAILED:
        if type(result) == list:
            parsed_responses: list[CheckDataAssetDetailedResponseUnion] = []
            for r in result:
                parsed_response = parse_check_data_asset_response(r)
                parsed_responses.append(parsed_response)
            return parsed_responses
        else:
            return ErrorResponse.parse_obj(result)
    if responseType == ResponseType.COMMENT_MARKDOWN:
        return parse_obj_as(CheckDataAssetCommentMarkdownResponse, result)
    raise ValueError(f"Unknown response type: {responseType}, cannot parse result")


# Pylance was struggling to understand the union type when calling parse_obj_as
# I created this function to prevent a '# type ignore' annotation in the code
def parse_check_data_asset_response(response) -> CheckDataAssetDetailedResponseUnion:
    response_type = response["responseType"]
    if response_type == ResponseType1.NO_CONTRACT.value:
        return parse_obj_as(CheckDataAssetNoContractResponse, response)
    if response_type == ResponseType2.DETAILED.value:
        return parse_obj_as(CheckDataAssetDetailedResponse, response)
    if response_type == ResponseType3.ERROR.value:
        return parse_obj_as(CheckDataAssetErrorResponse, response)
    if response_type == ResponseType4.MISSING_DATA_ASSET.value:
        return parse_obj_as(CheckDataAssetMissingAssetResponse, response)
    raise ValueError(f"Unknown response type: {response_type} in response: {response}")


def build_check_data_asset_inputs(
    source_type: str,
    source_names: list[str],
    schema_contents: list[str],
    realDbName: Optional[str] = None,
    realDbSchema: Optional[str] = None,
) -> dict[str, Input]:
    requests: dict[str, Input] = {}
    # If this is a database, there might be multiple table's schemas within the information schema
    # returned from the DbApi reader. In that case, we need to post each table's schema separately.
    if source_type in DATABASE_SOURCE_TYPE_VALUES:
        schema_contents_str = schema_contents[0]
        source_name = source_names[0]
        information_schema = json.loads(schema_contents_str)
        grouped_table_schemas: dict[str, List[Any]] = {}
        for information_schema_row in information_schema:
            if information_schema_row["TABLE_NAME"] not in grouped_table_schemas:
                grouped_table_schemas[information_schema_row["TABLE_NAME"]] = []
            grouped_table_schemas[information_schema_row["TABLE_NAME"]].append(
                information_schema_row
            )
        for table_name, table_schema in grouped_table_schemas.items():
            requests[f"{realDbName}.{realDbSchema}.{table_name}"] = Input(
                sourceType=source_type,
                sourceName=source_name,
                realDbName=realDbName,
                realDbSchema=realDbSchema,
                schemaContents=json.dumps(table_schema),
            )
    elif source_type in FILE_SOURCE_TYPE_VALUES:
        for source_name, schema in zip(source_names, schema_contents):
            requests[source_name] = Input(
                sourceType=source_type,
                sourceName=source_name,
                schemaContents=schema,
            )
    else:  # source_type in PYTHON_SOURCE_TYPE_VALUES
        for source_name, schema in zip(source_names, schema_contents):
            requests[source_name] = Input(
                sourceType=source_type,
                sourceName=source_name,
                schemaContents=schema,
            )
    return requests
