"""
Web search service using DuckDuckGo.
Provides internet access capability for Shayla.
"""
from utils.logger import logger

SEARCH_AVAILABLE = False

try:
    from duckduckgo_search import DDGS
    SEARCH_AVAILABLE = True
except ImportError:
    logger.warning("duckduckgo-search not installed. Web search will be disabled.")

async def search_web(query: str, max_results: int = 5) -> list:
    if not SEARCH_AVAILABLE:
        return [{"error": "Búsqueda web no disponible. duckduckgo-search no está instalado."}]

    try:
        import asyncio
        loop = asyncio.get_event_loop()

        results = await loop.run_in_executor(
            None,
            lambda: list(DDGS().text(query, max_results=max_results))
        )

        logger.info(f"Web search for '{query[:50]}...' returned {len(results)} results")

        formatted = []
        for r in results:
            formatted.append({
                "title": r.get("title", ""),
                "body": r.get("body", ""),
                "href": r.get("href", ""),
            })
        return formatted
    except Exception as e:
        logger.error(f"Web search error: {e}")
        return [{"error": f"Error en la búsqueda: {str(e)}"}]

def format_search_results(results: list) -> str:
    if not results:
        return "No encontré resultados para esa búsqueda."

    if "error" in results[0]:
        return f"⚠️ {results[0]['error']}"

    lines = ["**Resultados de la búsqueda:**\n"]
    for i, r in enumerate(results, 1):
        title = r.get("title", "Sin título")
        body = r.get("body", "")
        href = r.get("href", "")
        lines.append(f"{i}. **{title}**")
        if body:
            body_trimmed = body[:300] + "..." if len(body) > 300 else body
            lines.append(f"   {body_trimmed}")
        if href:
            lines.append(f"   [{href}]({href})")
        lines.append("")

    return "\n".join(lines)
