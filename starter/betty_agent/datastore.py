"""
datastore.py

Provides the Document Q&A tool. This queries a Vertex AI Search Datastore
(populated with Betty's Bird Boutique's PDF documents -- hours, history,
staff bios, etc.) using the google-cloud-discoveryengine library, and
exposes a simple tool function the root agent can call.

Based on the general pattern shown in Google's Vertex AI Search "Search
with generic API" sample
(https://cloud.google.com/generative-ai-app-builder/docs/preview-search-results),
adapted here to use the discoveryengine_v1 client classes and to return
plain strings instead of raw response objects, so the results are easy for
the agent's model to read.
"""

import os

from google.cloud import discoveryengine_v1 as discoveryengine

# Environment configuration, with sensible local-dev defaults.
DATASTORE_PROJECT_ID = os.environ.get("DATASTORE_PROJECT_ID", "")
DATASTORE_LOCATION = os.environ.get("DATASTORE_LOCATION", "global")
DATASTORE_ENGINE_ID = os.environ.get("DATASTORE_ENGINE_ID", "")


def search(
    search_query: str,
    project_id: str = DATASTORE_PROJECT_ID,
    location: str = DATASTORE_LOCATION,
    engine_id: str = DATASTORE_ENGINE_ID,
    page_size: int = 5,
) -> discoveryengine.services.search_service.pagers.SearchPager:
    """Runs a search against a Vertex AI Search Datastore/Engine.

    Args:
        search_query: The natural-language query to search for.
        project_id: GCP project ID that owns the Vertex AI Search app.
        location: Location of the search app (e.g. "global").
        engine_id: The Vertex AI Search app (engine) ID.
        page_size: Max number of results to request.

    Returns:
        A SearchPager of discoveryengine.SearchResponse.SearchResult objects.
    """
    # For "global" locations the API endpoint has no location prefix; for
    # regional locations it does. This mirrors Google's own sample code.
    client_options = (
        {"api_endpoint": f"{location}-discoveryengine.googleapis.com"}
        if location != "global"
        else None
    )
    client = discoveryengine.SearchServiceClient(client_options=client_options)

    # IMPORTANT: the serving config must be the *engine's* serving config
    # (projects/*/locations/*/collections/*/engines/*/servingConfigs/*), not
    # the data store's. The discoveryengine client's serving_config_path()
    # helper only builds the data-store-based path, so we build the
    # engine-based path manually here.
    serving_config = (
        f"projects/{project_id}/locations/{location}/collections/"
        f"default_collection/engines/{engine_id}/servingConfigs/default_config"
    )

    # NOTE: extractive answers/segments require an Enterprise-edition
    # engine. This project uses a Standard-edition engine, which only
    # supports snippets, so we request snippet_spec only. If you upgrade
    # the engine to Enterprise edition later, you can add
    # extractive_content_spec back in for richer, pre-extracted answers.
    content_search_spec = discoveryengine.SearchRequest.ContentSearchSpec(
        snippet_spec=discoveryengine.SearchRequest.ContentSearchSpec.SnippetSpec(
            return_snippet=True,
        ),
    )

    request = discoveryengine.SearchRequest(
        serving_config=serving_config,
        query=search_query,
        page_size=page_size,
        content_search_spec=content_search_spec,
    )

    return client.search(request)


def _extract_result_text(result) -> str:
    """Pulls the most useful piece of text out of a single search result."""
    document = result.document
    derived = document.derived_struct_data if document else None
    if not derived:
        return ""

    # Prefer extractive answers, then extractive segments, then snippets.
    extractive_answers = derived.get("extractive_answers", [])
    if extractive_answers:
        return extractive_answers[0].get("content", "")

    extractive_segments = derived.get("extractive_segments", [])
    if extractive_segments:
        return extractive_segments[0].get("content", "")

    snippets = derived.get("snippets", [])
    if snippets:
        return snippets[0].get("snippet", "")

    return ""


def search_store_documents(query: str) -> list[str]:
    """Searches Betty's Bird Boutique's store documents for an answer.

    Use this tool to answer questions about the store itself, such as its
    hours of operation, location, history, or staff (including staff bios
    and the birds staff members own). The documents are PDFs that have been
    indexed in a Vertex AI Search Datastore.

    Args:
        query: The customer's question, in natural language (e.g.
            "What time do you open on Thursday?" or "Who is Betty?").

    Returns:
        A list of short text excerpts pulled from the store's documents that
        are most relevant to the query. The list may be empty if nothing
        relevant was found -- in that case, tell the customer you couldn't
        find that information rather than guessing.
    """
    results = search(query)

    excerpts = []
    for result in results:
        text = _extract_result_text(result)
        if text:
            excerpts.append(text)

    return excerpts