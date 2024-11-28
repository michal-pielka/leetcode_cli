from ..data_fetching.graphql_data_fetchers.fetch_code_snippet import fetch_code_snippet

def create_solution_file(title_slug, lang_slug):
    file_name = f"{title_slug}.{lang_slug}"
    code_snippet = fetch_code_snippet(title_slug, lang_slug)
    
    with open(file_name, 'w') as file:
        file.write(code_snippet)

