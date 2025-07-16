import os
import sys
import requests
import yaml
import frontmatter
from jinja2 import Environment, FileSystemLoader
from markdown_it import MarkdownIt
from mdit_py_plugins.admon import admon_plugin

# --- Start of Script ---
print("--- Python script starting now. ---")

# --- Configuration & Pre-flight Checks ---
try:
    CONFLUENCE_URL = os.environ["CONFLUENCE_URL"]
    CONFLUENCE_USER = os.environ["CONFLUENCE_USER"]
    CONFLUENCE_API_TOKEN = os.environ["CONFLUENCE_API_TOKEN"]
    GITHUB_WORKSPACE = os.environ.get("GITHUB_WORKSPACE", ".")
    print("✅ Successfully loaded Confluence credentials and workspace.")
    print(f"   -> GITHUB_WORKSPACE is: {GITHUB_WORKSPACE}")
except KeyError as e:
    sys.exit(f"🛑 FATAL: Missing required environment variable: {e}. Please check your workflow 'env' block.")

# --- Function Definitions ---

def find_all_source_files(start_path):
    print("\n🔍 Scanning for all source files...")
    source_files = []
    
    # Let's see what's in the workspace directory
    print(f"   -> Listing contents of start_path ('{start_path}'):")
    try:
        for item in os.listdir(start_path):
            print(f"     - {item}")
    except Exception as e:
        print(f"     -> Could not list directory: {e}")

    # The action's own path, to be excluded
    action_dir = os.path.join(start_path, '.github', 'actions')
    print(f"   -> Will exclude files found in: {action_dir}")

    for root, dirs, files in os.walk(start_path):
        # Exclude the action's own directory to avoid loops
        if root.startswith(action_dir):
            continue
        
        print(f"   -> Traversing directory: {root}")
        for file in files:
            if file.endswith(('.md', '.j2', '.jinja')):
                full_path = os.path.join(root, file)
                print(f"     -> Found potential source file: {file}")
                source_files.append(full_path)

    print(f"\n✅ Scan complete. Found {len(source_files)} total files.")
    return source_files

def render_jinja_template(content, metadata, file_path):
    """Renders a markdown content string with Jinja2, supporting variables and macros."""
    # This function remains the same as before, no changes needed here.
    print("✨ Rendering Jinja2 template...")
    env = Environment(loader=FileSystemLoader(searchpath=GITHUB_WORKSPACE), autoescape=True)
    variables = {}
    vars_file_path = metadata.get('varsFile')
    if vars_file_path:
        full_vars_path = os.path.join(GITHUB_WORKSPACE, vars_file_path)
        if os.path.exists(full_vars_path):
            print(f"  -> Loading variables from: {vars_file_path}")
            with open(full_vars_path, 'r') as f:
                variables = yaml.safe_load(f)
        else:
            print(f"⚠️ Vars file not found at {full_vars_path}. Skipping.")
    try:
        template = env.from_string(content)
        return template.render(variables)
    except Exception as e:
        print(f"❌ Error rendering Jinja template for {file_path}: {e}")
        return None

def convert_md_to_confluence_xhtml(md_content, image_folder_path):
    """Converts rendered Markdown to Confluence XHTML and finds images."""
    # This function remains the same as before.
    print("🔄 Converting Markdown to Confluence XHTML...")
    md = MarkdownIt("commonmark", {"breaks": True, "html": True}).use(admon_plugin)
    html_output = md.render(md_content)
    image_files_to_upload = []
    if image_folder_path and os.path.exists(os.path.join(GITHUB_WORKSPACE, image_folder_path)):
        for img_file in os.listdir(os.path.join(GITHUB_WORKSPACE, image_folder_path)):
            if img_file in html_output:
                html_output = html_output.replace(f'src="{img_file}"', f'src="/download/attachments/PAGE_ID/{img_file}"')
                html_output = html_output.replace(f'<img src="{img_file}"', f'<ac:image><ri:attachment ri:filename="{img_file}" /></ac:image>')
                image_files_to_upload.append(os.path.join(GITHUB_WORKSPACE, image_folder_path, img_file))
    print(f"🖼️ Found {len(image_files_to_upload)} images to upload.")
    return html_output, image_files_to_upload

def publish_to_confluence(metadata, content, images):
    """Publishes the content to Confluence, creating or updating a page."""
    # This function remains the same as before.
    space = metadata['space']
    title = metadata['title']
    parent_page_id = metadata.get('parentPageId')
    page_id, version = find_confluence_page(space, title)
    page_data = {"type": "page", "title": title, "space": {"key": space}, "body": {"storage": {"value": content, "representation": "storage"}}}
    if page_id:
        print(f"⬆️ Updating page ID: {page_id}")
        page_data["id"] = page_id
        page_data["version"] = {"number": version + 1}
        url = f"{CONFLUENCE_URL}/rest/api/content/{page_id}"
        response = requests.put(url, json=page_data, headers={"Content-Type": "application/json"}, auth=(CONFLUENCE_USER, CONFLUENCE_API_TOKEN))
    else:
        print(f"✨ Creating new page under parent ID: {parent_page_id}")
        if parent_page_id:
            page_data["ancestors"] = [{"id": parent_page_id}]
        url = f"{CONFLUENCE_URL}/rest/api/content"
        response = requests.post(url, json=page_data, headers={"Content-Type": "application/json"}, auth=(CONFLUENCE_USER, CONFLUENCE_API_TOKEN))
    response.raise_for_status()
    new_page_info = response.json()
    print(f"✅ Successfully published page: {new_page_info['_links']['webui']}")
    if images:
        upload_images(new_page_info['id'], images)

def find_confluence_page(space, title):
    """Finds a Confluence page by title in a given space."""
    print(f"  -> Searching for page with title '{title}' in space '{space}'...")
    url = f"{CONFLUENCE_URL}/rest/api/content"
    params = {"spaceKey": space, "title": title, "expand": "version"}
    
    # The typo was here:
    response = requests.get(url, headers={"Accept": "application/json"}, auth=(CONFLUENCE_USER, CONFLUENCE_API_TOKEN), params=params)
    
    response.raise_for_status()
    results = response.json().get("results", [])
    if results:
        page_id = results[0]['id']
        version = results[0]['version']['number']
        print(f"  -> Found existing page. ID: {page_id}, Version: {version}")
        return page_id, version
    
    print("  -> Page not found. A new page will be created.")
    return None, None

def upload_images(page_id, images):
    """Uploads a list of image files to a Confluence page."""
    print(f"  -> Uploading {len(images)} image(s) to page ID: {page_id}")
    url = f"{CONFLUENCE_URL}/rest/api/content/{page_id}/child/attachment"
    headers = {"X-Atlassian-Token": "no-check"} # Required for attachment uploads

    for image_path in images:
        file_name = os.path.basename(image_path)
        print(f"    -> Preparing to upload: {file_name}")

        try:
            # Explicitly set the content type for the image
            content_type = 'image/png' # Defaulting to PNG, can be improved later if needed
            with open(image_path, 'rb') as f:
                # The 'files' dictionary needs three parts: name, file object, and content type
                files = {'file': (file_name, f, content_type)}

                # Using the correct auth variables
                response = requests.post(url, headers=headers, auth=(CONFLUENCE_USER, CONFLUENCE_API_TOKEN), files=files)
                response.raise_for_status()

            print(f"    ✅ Successfully uploaded {file_name}")

        except Exception as e:
            print(f"    ❌ Failed to upload {file_name}: {e}")
            # Continue to the next image even if one fails
            continue


# --- Main Execution ---

def main():
    print("\n--- UNIFIED PUBLISH PROCESS ---")
    source_files = find_all_source_files(GITHUB_WORKSPACE)

    if not source_files:
        print("\n🛑 STOPPING: No source files were found to process. Check the scan log above to see why.")
        return

    for file_path in source_files:
        try:
            print(f"\n--- Analyzing file: {os.path.basename(file_path)} ---")
            with open(file_path, 'r', encoding='utf-8') as f:
                post = frontmatter.load(f)

            if 'confluence' not in post.metadata or 'title' not in post.metadata.get('confluence', {}):
                print(f"⏭️ Skipping: Not a publishable page (missing 'confluence.title' front matter).")
                continue

            print("   -> Found valid 'confluence.title' key. Proceeding to publish.")
            confluence_meta = post.metadata['confluence']
            
            rendered_content = render_jinja_template(post.content, post.metadata, file_path)
            if rendered_content is None:
                continue

            image_folder = confluence_meta.get('imageFolder')
            confluence_xhtml, images_to_upload = convert_md_to_confluence_xhtml(rendered_content, image_folder)
            publish_to_confluence(confluence_meta, confluence_xhtml, images_to_upload)

        except Exception as e:
            print(f"❌ An error occurred while processing {os.path.basename(file_path)}: {e}")
            print("    Moving to the next file...")
            continue

    print("\n✅ All files processed.")

if __name__ == "__main__":
    main()