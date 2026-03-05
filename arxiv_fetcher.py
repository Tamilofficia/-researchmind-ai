import arxiv

def search_arxiv(query, max_results=3):
    """
    Search ArXiv for papers based on a query and return their abstracts.
    """
    try:
        # Construct the default API client.
        client = arxiv.Client()

        # Search for papers using the given query
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance
        )

        results = []
        for result in client.results(search):
            results.append({
                "title": result.title,
                "authors": [author.name for author in result.authors],
                "abstract": result.summary,
                "url": result.pdf_url
            })
            
        return results

    except Exception as e:
        print(f"Error searching ArXiv: {e}")
        return []
