sequenceDiagram
    actor Developer
    participant GitHub
    actor AppSupport as Application Support (via Ansible)
    participant Shares as Filesystem Shares

    Note over Developer, Shares: Phase 1: Development & Local Testing

    Developer->>Shares: Works in isolated 'Dev' share
    Developer->>Developer: Edits Launcher code (VB.NET) in IDE
    Developer->>GitHub: Commits code changes to a feature branch

    Note over Developer, GitHub: Phase 2: Code Review & Integration

    Developer->>GitHub: Creates Pull Request to 'develop' branch
    GitHub-->>Developer: (Automated Build / Peer Review)
    Developer->>GitHub: Merges approved PR

    Note over Developer, AppSupport: Phase 3: Release Request & Packaging

    Developer->>AppSupport: Requests a new release promotion
    AppSupport->>Shares: 1. Copies artifacts from 'UAT' or 'Staging'
    AppSupport->>GitHub: 2. Fetches tagged Launcher version
    AppSupport->>AppSupport: 3. Creates the release manifest.json
    AppSupport->>Shares: 4. Creates new folder in 'Archive'<br/>(e.g., /2025-08-04_Release-1.2.1)
    AppSupport->>Shares: 5. Places all components into the Archive folder

    Note over AppSupport, Shares: Phase 4: Deployment to Environments

    AppSupport->>Shares: Deploys package from 'Archive' to 'UAT' for testing
    Note right of AppSupport: (Business User Validation occurs here)
    AppSupport->>Shares: Upon approval, deploys same package<br/>from 'Archive' to 'Prod'

    Note over Developer, Shares: Result: Production is updated atomically with a complete, versioned release.
