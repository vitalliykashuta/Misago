from typing import Any, Dict, List, Tuple

from ariadne import MutationType, convert_kwargs_to_snake_case
from graphql import GraphQLResolveInfo
from pydantic import PositiveInt, create_model

from ...errors import ErrorsList
from ...hooks import (
    delete_threads_hook,
    delete_threads_input_hook,
    delete_threads_input_model_hook,
)
from ...loaders import clear_all_posts, clear_threads, load_threads
from ...threads.delete import delete_threads
from ...types import (
    AsyncValidator,
    GraphQLContext,
    DeleteThreadsInput,
    DeleteThreadsInputModel,
)
from ...validation import (
    CategoryModeratorValidator,
    ThreadCategoryValidator,
    ThreadExistsValidator,
    ThreadsBulkValidator,
    UserIsAuthorizedRootValidator,
    bulkactionidslist,
    validate_data,
    validate_model,
)
from ..errorhandler import error_handler


delete_threads_mutation = MutationType()


@delete_threads_mutation.field("deleteThreads")
@convert_kwargs_to_snake_case
@error_handler
async def resolve_delete_threads(
    _, info: GraphQLResolveInfo, *, input: dict  # pylint: disable=redefined-builtin
):
    input_model = await delete_threads_input_model_hook.call_action(
        create_input_model, info.context
    )
    cleaned_data, errors = validate_model(input_model, input)

    if cleaned_data.get("threads"):
        # prime threads cache for bulk action
        await load_threads(info.context, cleaned_data["threads"])

    if cleaned_data:
        validators: Dict[str, List[AsyncValidator]] = {
            "threads": [
                ThreadsBulkValidator(
                    [
                        ThreadExistsValidator(info.context),
                        ThreadCategoryValidator(
                            info.context, CategoryModeratorValidator(info.context)
                        ),
                    ]
                )
            ],
            ErrorsList.ROOT_LOCATION: [UserIsAuthorizedRootValidator(info.context)],
        }
        cleaned_data, errors = await delete_threads_input_hook.call_action(
            validate_input_data, info.context, validators, cleaned_data, errors
        )

    result: Dict[str, Any] = {}

    if await is_valid(cleaned_data, errors):
        await delete_threads_hook.call_action(
            delete_threads_action, info.context, cleaned_data
        )
        result["deleted"] = True
    else:
        result["deleted"] = False

    if errors:
        result["errors"] = errors

    return result


async def create_input_model(context: GraphQLContext) -> DeleteThreadsInputModel:
    return create_model(
        "DeleteThreadsInputModel",
        threads=(bulkactionidslist(PositiveInt, context["settings"]), ...),
    )


async def validate_input_data(
    context: GraphQLContext,
    validators: Dict[str, List[AsyncValidator]],
    data: DeleteThreadsInput,
    errors: ErrorsList,
) -> Tuple[DeleteThreadsInput, ErrorsList]:
    return await validate_data(data, validators, errors)


async def is_valid(
    cleaned_data: DeleteThreadsInput, errors_locations: ErrorsList
) -> bool:
    if errors_locations.has_root_errors:
        return False
    if not cleaned_data.get("threads"):
        return False
    return True


async def delete_threads_action(
    context: GraphQLContext, cleaned_data: DeleteThreadsInput
):
    await delete_threads(cleaned_data["threads"])
    clear_threads(context, cleaned_data["threads"])
    clear_all_posts(context)
