---
# 🎉 Bug Free Fiesta

A demonstration repository showcasing automated documentation publishing with Ansible Automation Platform (AAP) templates.

## 📁 Repository Structure

```bash
bug-free-fiesta/
├── docs/                           # Documentation templates and content
│   ├── macros/                     # Jinja2 macros for template processing
│   ├── images/                     # Documentation images and diagrams
│   ├── *.j2                        # Jinja2 documentation templates
│   ├── vars.yaml                   # Template variables and configuration
│   └── *.md                        # Markdown documentation files
├── .github/
│   └── workflows/
│       └── ci-cd.yml               # CI/CD pipeline with external publishing
└── requirements.txt                # Python and Ansible dependencies
```

## 🚀 Features

- **📝 Template-based Documentation**: Uses Jinja2 templates for dynamic content generation
- **🔄 Automated Publishing**: Integrates with `redesigned-guacamole` for Confluence publishing
- **🛡️ Quality Assurance**: Automated linting and security scanning
- **📊 Cross-Repository Workflow**: Demonstrates external workflow calling patterns

## 🔧 Usage

### Manual Workflow Trigger

1. Navigate to **Actions** tab in GitHub
2. Select **"🚀 CI/CD Pipeline"**
3. Click **"Run workflow"**
4. Configure options:
   - **Full scan**: Enable complete codebase analysis
   - **Target environment**: Choose deployment target
   - **Dry run**: Test without actual publishing

### Automatic Triggers

The workflow automatically runs on:
- Push to `main`, `develop`, `feature/*`, `release/*`, `hotfix/*` branches
- Pull requests to `main` or `develop` branches

## 📚 Documentation Templates

The repository includes several AAP-focused documentation templates:

- **`aap_platform_admin_guide.j2`**: Platform administration guide
- **`aap_operations_manual.j2`**: Operational procedures and runbooks
- **`aap_policy_governance.j2`**: Governance and compliance documentation
- **`BRANCH_NAMING_GUIDE.j2`**: Development workflow guidelines

## ⚙️ Configuration

Template variables are configured in `docs/vars.yaml`:

```yaml
project_name: "Project Phoenix"
ORGANIZATION_NAME: "My Big Company"
SUB_ORGANIZATION_NAME: "Server Engineering and Operations"
# ... additional configuration
```

## 🔐 Required Secrets

For Confluence publishing, configure these repository secrets:

- `CONFLUENCE_URL`: Your Confluence instance URL
- `CONFLUENCE_USER`: Confluence username/email
- `CONFLUENCE_API_TOKEN`: Confluence API token

## 🤝 Integration

This repository demonstrates integration with [`redesigned-guacamole`](https://github.com/KhalilGibrotha/redesigned-guacamole) for:

- External workflow execution
- Centralized publishing automation
- Cross-repository secret management
- Template processing and rendering

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
