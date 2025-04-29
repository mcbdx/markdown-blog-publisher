import markdown

def get_frontmatter_metadata(content):
    """
        Extracts the front matter from the content.
    """
    if content.startswith("---"):
        
        # this returns where the string begins
        end = content.find("---",3) # this helps me tell find to start looking after index 3 else starts looking at index 0 which will be the start 

        metadata = {}

        for line in content[4:end].splitlines():
            d = line.strip().split(":")
            if d[0] == "tags":
                metadata[d[0]] = []
            if d[0].startswith('-'):
                metadata['tags'].append(d[0].replace("- ", ""))
            if d[0] != "tags" and not d[0].startswith("-"):
                metadata[d[0]] = d[1].strip()
            if d[0] == "published":
                metadata[d[0]] = d[1].strip().lower() == "true"

        return metadata

def extract_main_content(content):
    main_start = content.find("---", 3)
    return content[main_start+5:]

def md_transform_content(content):
    transformed_content = markdown.markdown(content, extensions=['fenced_code','tables','toc'])
    return transformed_content


def generate_html(file):
    with open(file, 'r') as f:
        content = f.read()
        metadata = get_frontmatter_metadata(content)
        main_content = extract_main_content(content)
        html = md_transform_content(main_content)

    return metadata, html




    