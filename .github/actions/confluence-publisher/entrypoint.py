import os
import sys
import requests
import yaml
import frontmatter
from jinja2 import Environment, FileSystemLoader
from markdown_it import MarkdownIt
from mdit_py_plugins.front_matter import front_matter_plugin
from mdit_py_plugins.admon import admon_plugin

# --- Configuration ---
# Get Confluence credentials and URL from environment variables (set by the GitHub workflow)
CONFLUENCE_URL = os.environ.get("CONFLUENCE_URL")
CONFLUENCE_USER = os.environ.get("CONFLUENCE_USER")
CONFLUENCE_API_TOKEN = os.environ.get("CONFLUENCE_API_TOKEN")
GITHUB_WORKSPACE = os.environ.get("GITHUB_WORKSPACE", ".")

# Set up authentication for Confluence API
confluence_auth = (CONFLUENCE_USER, CONFLUENCE_API_TOKEN)
confluence_headers = {"Content-Type": "application/json", "Accept": "application/json"}

# --- Helper Functions ---

def find_markdown_files(start_path):
    """Finds all Markdown files in the repository."""
    print("🔍 Scanning for Markdown files...")
    markdown_files = []
    for root, _, files in os.walk(start_path):
        for file in files:
            if file.endswith(".md"):
                markdown_files.append(os.path.join(root, file))
    print(f"✅ Found {len(markdown_files)} Markdown files.")
    return markdown_files

def render_jinja_template(content, vars_file_path):
    """Renders the markdown content with Jinja2 if a vars file is specified."""
    if not vars_file_path:
        return content

    full_vars_path = os.path.join(GITHUB_WORKSPACE, vars_file_path)
    if not os.path.exists(full_vars_path):
        print(f"⚠️ Vars file not found at {full_vars_path}. Skipping templating.")
        return content

    with open(full_vars_path, 'r') as f:
        variables = yaml.safe_load(f)

    # Use a string-based loader for Jinja
    env = Environment(loader=FileSystemLoader(searchpath=GITHUB_WORKSPACE))
    template = env.from_string(content)
    return template.render(variables)


def convert_md_to_confluence_xhtml(md_content, image_folder_path):
    """Converts rendered Markdown to Confluence XHTML and finds images."""
    print("🔄 Converting Markdown to Confluence XHTML...")
    
    # Configure the markdown parser
    md = MarkdownIt("commonmark", {"breaks": True, "html": True}).use(admon_plugin)
    
    # This is a simplified conversion. Real-world might need more robust HTML parsing.
    html_output = md.render(md_content)

    # --- Image Handling ---
    # Convert local image paths to Confluence attachment tags
    image_files_to_upload = []
    # A more robust solution would parse the HTML tree (e.g., with BeautifulSoup)
    # For simplicity, we're doing a string replacement here.
    if image_folder_path and os.path.exists(os.path.join(GITHUB_WORKSPACE, image_folder_path)):
        for img_file in os.listdir(os.path.join(GITHUB_WORKSPACE, image_folder_path)):
            if html_output.find(img_file) != -1:
                html_output = html_output.replace(f'src="{img_file}"', f'src="/download/attachments/PAGE_ID/{img_file}"') # Placeholder
                html_output = html_output.replace(f'src="./{img_file}"', f'src="/download/attachments/PAGE_ID/{img_file}"')
                html_output = html_output.replace(f'<img src="{img_file}"', f'<ac:image><ri:attachment ri:filename="{img_file}" /></ac:image>')

                image_files_to_upload.append(os.path.join(GITHUB_WORKSPACE, image_folder_path, img_file))

    print(f"🖼️ Found {len(image_files_to_upload)} images to upload.")
    return html_output, image_files_to_upload


def find_confluence_page(space, title):
    """Finds a Confluence page by title in a given space."""
    print(f"🔎 Searching for page with title '{title}' in space '{space}'...")
    
    # Let's add this for better debugging!
    endpoint_url = f"{CONFLUENCE_URL}/rest/api/content"
    print(f"  -> Calling API endpoint: {endpoint_url}")

    params = {"spaceKey": space, "title": title, "expand": "version"}
    try:
        response = requests.get(endpoint_url, headers=confluence_headers, auth=confluence_auth, params=params)
        response.raise_for_status() # This will raise an error on 4xx or 5xx responses
        results = response.json().get("results", [])
        if results:
            page_id = results[0]['id']
            version = results[0]['version']['number']
            print(f"✅ Found existing page. ID: {page_id}, Version: {version}")
            return page_id, version
        print("📄 Page not found. Will create a new one.")
        return None, None
    except requests.exceptions.HTTPError as err:
        print(f"❌ HTTP Error received: {err}")
        # Add more context for 403 errors
        if err.response.status_code == 403:
            print("  -> A 403 Forbidden error suggests an issue with permissions, the API token, or IP allowlisting.")
        sys.exit(1) # Exit with an error code


def publish_to_confluence(metadata, content, images):
    """Publishes the content to Confluence, creating or updating a page."""
    space = metadata['confluenceSpace']
    title = metadata['title']
    parent_page_id = metadata['parentPageId']

    page_id, version = find_confluence_page(space, title)

    page_data = {
        "type": "page",
        "title": title,
        "space": {"key": space},
        "body": {
            "storage": {
                "value": content,
                "representation": "storage"
            }
        }
    }

    if page_id: # Update existing page
        print(f"⬆️ Updating page ID: {page_id}")
        page_data["id"] = page_id
        page_data["version"] = {"number": version + 1}
        url = f"{CONFLUENCE_URL}/rest/api/content/{page_id}"
        response = requests.put(url, json=page_data, headers=confluence_headers, auth=confluence_auth)
    else: # Create new page
        print(f"✨ Creating new page under parent ID: {parent_page_id}")
        page_data["ancestors"] = [{"id": parent_page_id}]
        url = f"{CONFLUENCE_URL}/rest/api/content"
        response = requests.post(url, json=page_data, headers=confluence_headers, auth=confluence_auth)

    response.raise_for_status()
    new_page_info = response.json()
    new_page_id = new_page_info['id']
    print(f"✅ Successfully published page: {new_page_info['_links']['webui']}")
    
    # --- Upload Images ---
    if images:
        upload_images(new_page_id, images)


def upload_images(page_id, images):
    """Uploads a list of image files to a Confluence page."""
    print(f"🚀 Uploading {len(images)} images to page ID {page_id}...")
    url = f"{CONFLUENCE_URL}/rest/api/content/{page_id}/child/attachment"
    headers = {"X-Atlassian-Token": "no-check"} # Required for attachment uploads

    for image_path in images:
        file_name = os.path.basename(image_path)
        print(f"  -> Uploading {file_name}")
        with open(image_path, 'rb') as f:
            files = {'file': (file_name, f, 'image/png', {'Expires': '0'})}
            response = requests.post(url, headers=headers, auth=confluence_auth, files=files)
            response.raise_for_status()
    print("✅ All images uploaded.")


# --- Main Execution ---
def main():
    if not all([CONFLUENCE_URL, CONFLUENCE_USER, CONFLUENCE_API_TOKEN]):
        sys.exit("🛑 Missing required Confluence credentials. Set CONFLUENCE_URL, CONFLUENCE_USER, and CONFLUENCE_API_TOKEN secrets.")

    files_to_process = find_markdown_files(GITHUB_WORKSPACE)

    for file_path in files_to_process:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                post = frontmatter.load(f)

            # Check for required metadata
            required_keys = ['confluenceSpace', 'parentPageId', 'title']
            if not all(key in post.metadata for key in required_keys):
                print(f"⏭️ Skipping {os.path.basename(file_path)}: missing required front matter.")
                continue
            
            print(f"\n--- Processing: {os.path.basename(file_path)} ---")

            # 1. Render Jinja templates
            rendered_content = render_jinja_template(post.content, post.metadata.get('varsFile'))

            # 2. Convert to Confluence format and find images
            image_folder = post.metadata.get('imageFolder')
            confluence_xhtml, images_to_upload = convert_md_to_confluence_xhtml(rendered_content, image_folder)

            # 3. Publish to Confluence
            publish_to_confluence(post.metadata, confluence_xhtml, images_to_upload)

        except Exception as e:
            print(f"❌ Error processing {file_path}: {e}")
            continue

if __name__ == "__main__":
    main()