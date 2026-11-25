import chromadb
from chromadb.config import Settings
from typing import Dict, List, Optional
from pathlib import Path

def discover_chroma_backends() -> Dict[str, Dict[str, str]]:
    """Discover available ChromaDB backends in the project directory"""
    backends = {}
    current_dir = Path(".")
    
    # Look for ChromaDB directories
    # TODO: Create list of directories that match specific criteria (directory type and name pattern)
    chroma_dirs = [
        directory
        for directory in current_dir.iterdir()
        if directory.is_dir() and "chroma" in directory.name.lower()
    ]

    # TODO: Loop through each discovered directory
    for chroma_dir in chroma_dirs:
        # TODO: Wrap connection attempt in try-except block for error handling
        try:
            # TODO: Initialize database client with directory path and configuration settings
            client = chromadb.PersistentClient(
                path=str(chroma_dir),
                settings=Settings(anonymized_telemetry=False)
            )
            # TODO: Retrieve list of available collections from the database
            collections = client.list_collections()
            # TODO: Loop through each collection found
            for collection_info in collections:
                if isinstance(collection_info, str):
                    collection_name = collection_info
                    collection = client.get_collection(
                        name=collection_name
                    )
                else:
                    collection_name = collection_info.name
                    collection = collection_info
                # TODO: Create unique identifier key combining directory and collection names
                backend_key = f"{chroma_dir.name}::{collection_name}"
                # TODO: Build information dictionary containing:
                    # TODO: Store directory path as string
                    # TODO: Store collection name
                    # TODO: Create user-friendly display name
                    # TODO: Get document count with fallback for unsupported operations
                try:
                      document_count = collection.count()
                except Exception:
                        document_count = "Unknown"

                collection_info_dict = {
                       "path": str(chroma_dir),
                       "collection_name": collection_name,
                       "display_name": (
                          f"{chroma_dir.name} / {collection_name} "
                          f"({document_count} documents)"
                        ),
                        "document_count": str(document_count)
                }
                # TODO: Add collection information to backends dictionary
                backends[backend_key] = collection_info_dict
        # TODO: Handle connection or access errors gracefully
        except Exception as error:
            # TODO: Create fallback entry for inaccessible directories
            backend_key = f"{chroma_dir.name}::error"
            # TODO: Include error information in display name with truncation
            error_message = str(error)

            if len(error_message) > 80:
                error_message = error_message[:77] + "..."

            # TODO: Set appropriate fallback values for missing information
            backends[backend_key] = {
                "path": str(chroma_dir),
                "collection_name": "",
                "display_name": (
                    f"{chroma_dir.name} "
                    f"(Unavailable: {error_message})"
                ),
                "document_count": "Unknown"
            }
    # TODO: Return complete backends dictionary with all discovered collections
    return backends
def initialize_rag_system(chroma_dir: str, collection_name: str):
    """Initialize the RAG system with specified backend (cached for performance)"""

    # TODO: Create a chomadb persistentclient
    client = chromadb.PersistentClient(
        path=chroma_dir,
        settings=Settings(anonymized_telemetry=False)
    )

    # TODO: Return the collection with the collection_name
    return client.get_collection(
        name=collection_name
    )
def retrieve_documents(collection, query: str, n_results: int = 3, 
                      mission_filter: Optional[str] = None) -> Optional[Dict]:
    """Retrieve relevant documents from ChromaDB with optional filtering"""

    # TODO: Initialize filter variable to None (represents no filtering)
    query_filter = None
    # TODO: Check if filter parameter exists and is not set to "all" or equivalent
    # TODO: If filter conditions are met, create filter dictionary with appropriate field-value pairs
    if (
        mission_filter
        and mission_filter.strip().lower()
        not in {"all", "all missions", "none"}
    ):
        query_filter = {
            "mission": mission_filter
        }
    # TODO: Execute database query with the following parameters:
        # TODO: Pass search query in the required format
        # TODO: Set maximum number of results to return
        # TODO: Apply conditional filter (None for no filtering, dictionary for specific filtering)
    if query_filter is None:
        results = collection.query(
            query_texts=[query],
            n_results=n_results
        )
    else:
        results = collection.query(
            query_texts=[query],
            n_results=n_results,
            where=query_filter
        )
    # TODO: Return query results to caller
    return results
def format_context(documents: List[str], metadatas: List[Dict]) -> str:
    """Format retrieved documents into context"""
    if not documents:
        return ""
    
    # TODO: Initialize list with header text for context section
    context_parts = [
        "Retrieved NASA Mission Context:",
        ""
    ]
    # TODO: Loop through paired documents and their metadata using enumeration
    for index, (document, metadata) in enumerate(
        zip(documents, metadatas),
        start=1
    ):
        # TODO: Extract mission information from metadata with fallback value
        mission = metadata.get("mission", "Unknown mission")
        # TODO: Clean up mission name formatting (replace underscores, capitalize)
        mission = str(mission).replace("_", " ").title()
        # TODO: Extract source information from metadata with fallback value 
        source = metadata.get("source", "Unknown source")
        # TODO: Extract category information from metadata with fallback value
        category = metadata.get("category", "Unknown category")
        # TODO: Clean up category name formatting (replace underscores, capitalize)
        category = str(category).replace("_", " ").title()
        
        # TODO: Create formatted source header with index number and extracted information
        source_header = (
            f"[Source {index}]\n"
            f"Mission: {mission}\n"
            f"Source: {source}\n"
            f"Category: {category}"
        )
        # TODO: Add source header to context parts list
        context_parts.append(source_header)
        
        # TODO: Check document length and truncate if necessary
        max_length = 2000

        if len(document) > max_length:
            document = document[:max_length].rstrip() + "..."
        # TODO: Add truncated or full document content to context parts list
        context_parts.append(document)
        context_parts.append("")

    # TODO: Join all context parts with newlines and return formatted string
    return "\n".join(context_parts).strip()