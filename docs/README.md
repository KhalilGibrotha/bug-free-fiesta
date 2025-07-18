# 📚 Documentation Template Guide

This directory contains Jinja2 templates for generating dynamic documentation using variables and macros. This guide explains how to create properly formatted template files that integrate with the Confluence publishing system.

## � Table of Contents

- [Template Structure](#-template-structure)
- [YAML Front Matter](#-yaml-front-matter)
- [Variable Usage](#-variable-usage)
- [Macro Integration](#-macro-integration)
- [Template Examples](#-template-examples)
- [Best Practices](#-best-practices)
- [Directory Structure](#-directory-structure)

## 🏗️ Template Structure

All documentation templates follow this standardized structure:

```jinja2
---
# Required YAML Front Matter
varsFile: "vars/aap.yml"
project_status: "Active"

# Confluence Publishing Configuration
confluence:
  title: "Document Title"
  space: "SPACE_KEY"
  category: "operations"           # Uses hierarchy from vars/aap.yml
  imageFolder: "docs/images"
---

{% import 'docs/macros/macros.j2' as macros %}

# {{ organization_name }} Document Title

## Content using variables and macros...
```

## 📝 YAML Front Matter

### Required Fields

Every template must include these required fields:

```yaml
---
varsFile: "vars/aap.yml"           # Path to variables file
project_status: "Active"           # Status: Active, Draft, Deprecated, In Review
```

### Confluence Configuration

For Confluence publishing, include the `confluence` section:

```yaml
confluence:
  title: "Your Document Title"      # Title in Confluence
  space: "AH"                      # Confluence space key (e.g., AH, DOC, PROJ)
  category: "operations"           # Category from hierarchy (operations, administration, governance, etc.)
  imageFolder: "docs/images"       # Relative path to images
```

**Available Categories:**
- `operations` - Operations & Maintenance
- `administration` - Platform Administration  
- `governance` - Policies & Governance
- `automation_hub` - Automation Hub
- `guides` - User Guides & Training
- `testing` - Testing & Validation

**Legacy Support:**
You can still use `parentPageId` directly if needed:
```yaml
confluence:
  title: "Your Document Title"
  space: "AH"
  parentPageId: "123456"           # Direct parent page ID
  imageFolder: "docs/images"
```

### Optional Fields

Additional metadata fields you can include:

```yaml
author: "Your Name"                # Document author
version: "1.0"                     # Document version
tags: ["automation", "platform"]   # Document tags
lastUpdated: "2025-07-17"         # Last update date
```

## 🔧 Variable Usage

### Importing Variables

Variables are defined in `vars/aap.yml` and referenced in templates using Jinja2 syntax:

```jinja2
# Basic variable usage
{{ organization_name }}
{{ aap_version }}

# Array/list variables with join filter
{{ rhel_versions | join(', ') }}
{{ main_objectives | join(', ') }}

# Complex variable usage
{{ aap_security_and_compliance | join(', ') }}
```

### Available Variables

Key variables available from `vars/aap.yml`:

**Organization Variables:**
- `organization_name` - Primary organization name
- `sub_organization_name` - Sub-organization name
- `environment_type` - Environment type (Production, Development, etc.)

**Platform Variables:**
- `aap_version` - Ansible Automation Platform version
- `aap_registry_url` - Container registry URL
- `aap_rbac_provider` - RBAC provider system

**Technical Stack Variables:**
- `aap_network_tech` - Network technologies (array)
- `aap_security_tech` - Security technologies (array)
- `aap_compute_tech` - Compute technologies (array)

**Configuration Variables:**
- `aap_inventory_management` - Inventory management system
- `aap_credential_storage` - Credential storage system
- `aap_compliance_audit_frequency` - Audit frequency

### Variable Naming Convention

All variables follow Ansible naming conventions:
- Use lowercase letters and underscores only
- Start with a letter or underscore
- Pattern: `^[a-z_][a-z0-9_]*$`

## 🧩 Macro Integration

### Importing Macros

Always import macros at the top of your template:

```jinja2
{% import 'docs/macros/macros.j2' as macros %}
```

### Available Macros

**`oxford_comma_list(items)`**
Creates grammatically correct lists with Oxford commas:

```jinja2
# Usage
{{ macros.oxford_comma_list(main_objectives) }}

# Output: "Objective A, Objective B, and Objective C"
```

**Usage Examples:**
```jinja2
# For technology lists
Our network technologies include {{ macros.oxford_comma_list(aap_network_tech) }}.

# For objectives
{{ organization_name }} focuses on {{ macros.oxford_comma_list(main_objectives) }}.

# For compliance standards
We adhere to {{ macros.oxford_comma_list(aap_security_and_compliance) }} standards.
```

## 📚 Template Examples

### Basic Template Structure

```jinja2
---
varsFile: "vars/aap.yml"
project_status: "Active"

confluence:
  title: "{{ organization_name }} Operations Guide"
  space: "AH"
  category: "operations"
  imageFolder: "docs/images"
---

{% import 'docs/macros/macros.j2' as macros %}

# {{ organization_name }} Operations Guide

## Overview
This guide covers operations for {{ sub_organization_name }}'s automation platform.

## Environment Details
- **Organization**: {{ organization_name }}
- **Platform Version**: {{ aap_version }}
- **Environment Type**: {{ environment_type }}

## Supported Technologies
### Network Technologies
{{ macros.oxford_comma_list(aap_network_tech) }}

### Security Technologies  
{{ macros.oxford_comma_list(aap_security_tech) }}

## Compliance
We maintain compliance with {{ macros.oxford_comma_list(aap_security_and_compliance) }}.
```

### Advanced Template with Conditional Logic

```jinja2
---
varsFile: "vars/aap.yml"
project_status: "Active"

confluence:
  title: "Platform Configuration Guide"
  space: "AH"
  category: "administration"
  imageFolder: "docs/images"
---

{% import 'docs/macros/macros.j2' as macros %}

# {{ organization_name }} Platform Configuration

## Infrastructure Overview
- **Load Balancer**: {{ aap_load_balancer }}
- **Registry**: {{ aap_registry_url }}
- **RBAC Provider**: {{ aap_rbac_provider }}

## Operating System Support
### RHEL Versions
Supported RHEL versions: {{ macros.oxford_comma_list(rhel_versions) }}

### Windows Versions
Supported Windows versions: {{ macros.oxford_comma_list(windows_versions) }}

## Technology Stack
{% if aap_network_tech %}
### Network Technologies
{{ macros.oxford_comma_list(aap_network_tech) }}
{% endif %}

{% if aap_security_tech %}
### Security Technologies
{{ macros.oxford_comma_list(aap_security_tech) }}
{% endif %}
```

## ✅ Best Practices

### 1. **Consistent Variable Usage**
```jinja2
# Good - Use variables for reusability
{{ organization_name }}'s platform runs on {{ aap_version }}.

# Bad - Hard-coded values
My Company's platform runs on version 2.4.
```

### 2. **Proper Macro Usage**
```jinja2
# Good - Use macros for lists
{{ macros.oxford_comma_list(main_objectives) }}

# Bad - Manual list formatting
{{ main_objectives[0] }}, {{ main_objectives[1] }}, and {{ main_objectives[2] }}
```

### 3. **YAML Front Matter Validation**
```yaml
# Good - Complete configuration
---
varsFile: "vars/aap.yml"
project_status: "Active"

confluence:
  title: "Complete Title"
  space: "AH"
  category: "operations"
  imageFolder: "docs/images"
---

# Bad - Missing required fields
---
confluence:
  title: "Incomplete"
---
```

### 4. **Template Organization**
```jinja2
# Good - Organized structure
{% import 'docs/macros/macros.j2' as macros %}

# {{ organization_name }} Title

## Section 1
Content with {{ variables }}

## Section 2
More content with {{ macros.oxford_comma_list(array_variable) }}
```

### 5. **Variable Validation**
```jinja2
# Good - Check if variables exist
{% if aap_metrics %}
## Performance Metrics
{{ macros.oxford_comma_list(aap_metrics) }}
{% endif %}

# Bad - Assuming variables exist
## Performance Metrics
{{ macros.oxford_comma_list(aap_metrics) }}
```

## 📁 Directory Structure

```
docs/
├── README.md                          # This guide
├── vars.yaml                          # Variable definitions
├── macros/
│   └── macros.j2                      # Jinja2 macros
├── templates/
│   ├── main.j2                        # Main template
│   ├── child.j2                       # Child template
│   └── macros.j2                      # Template-specific macros
├── automation_hub/
│   ├── automation_hub.j2              # Hub documentation
│   ├── automation_hub_simple.j2       # Simplified hub docs
│   └── *.j2                           # Other hub templates
├── aap_operations_manual.j2           # Operations manual
├── aap_platform_admin_guide.j2        # Admin guide
├── aap_policy_governance.j2           # Policy documentation
└── images/                            # Image assets
    └── *.png, *.jpg, *.webp
```

## 🔍 Template Validation

### Syntax Checking
```bash
# Check Jinja2 syntax
python -c "
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('docs'))
template = env.get_template('your_template.j2')
"
```

### Variable Validation
```bash
# Check for undefined variables
grep -r "{{ [a-zA-Z_]" docs/ --include="*.j2" | grep -v "macros"
```

### YAML Front Matter Validation
```bash
# Validate YAML headers
python -c "
import yaml
with open('docs/your_template.j2', 'r') as f:
    content = f.read()
    if content.startswith('---'):
        yaml_end = content.find('---', 3)
        yaml_content = content[3:yaml_end]
        yaml.safe_load(yaml_content)
"
```

## 🚀 Getting Started

1. **Copy Template Structure**:
   ```bash
   cp docs/templates/main.j2 docs/your_new_doc.j2
   ```

2. **Update YAML Front Matter**:
   - Set appropriate `title`, `space`, and `parentPageId`
   - Ensure `varsFile` points to correct variables file

3. **Import Macros**:
   ```jinja2
   {% import 'docs/macros/macros.j2' as macros %}
   ```

4. **Use Variables**:
   - Reference variables from `vars/aap.yml`
   - Use macros for consistent formatting

5. **Test Template**:
   - Validate YAML syntax
   - Check variable references
   - Test macro usage

## 📞 Support

For questions about template creation or variable usage:
- Check `vars/aap.yml` for available variables
- Review `docs/macros/macros.j2` for macro definitions
- Examine existing templates for examples
- Consult the main repository documentation

---

**📝 Note**: This documentation is actively maintained. Always use the latest variable names and macro definitions from the repository.
