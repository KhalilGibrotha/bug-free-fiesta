---
# You can have other metadata here, like variables for Jinja
varsFile: "docs/vars.yaml"
project_status: "In Review"

# All Confluence settings are now nested under this block
confluence:
  title: "My Awesome New Feature"
  space: "AH" # Renamed from confluenceSpace
  parentPageId: "123456789" # Optional: for creating pages under a parent
  imageFolder: "docs/images" # Optional: for finding images
------

# {{ project_name }} Documentation

This document describes the architecture for our awesome new feature.

Now I am updating the document to make sure that it updates correctly!

## Architecture Diagram

Here is the main diagram:
![The overall architecture of the new feature.](architecture_diagram.webp)
![The overall architecture of the new feature.](architecture_diagram.png)
## Status
The current status of the project is **{{ project_status }}**.# Test Change Fri Jul 18 14:02:53 EDT 2025
