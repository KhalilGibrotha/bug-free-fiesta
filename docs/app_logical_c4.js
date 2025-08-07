C4Container
    title Ansible Automation Platform Ecosystem (Full View)

    %% --- External / SaaS Services ---
    System_Ext(scm, "GitHub", "SaaS: Source Code", $sprite="github")
    System_Ext(teams, "Microsoft Teams", "SaaS: Notifications", $sprite="msteams")
    System_Ext(cloud, "Cloud Resources", "IaaS: VMs & Services", $sprite="aws/Compute/EC2")
    System_Ext(helix, "BMC Helix", "ITSM SaaS", $sprite="archimate/application-collaboration")
    System_Ext(infoblox, "Infoblox", "DDI SaaS", $sprite="archimate/application-collaboration")
    System_Ext(cyb_ccp, "CyberArk CCP", "Privileged Acct Mgmt", $sprite="archimate/application-component")
    System_Ext(cyb_secrets, "CyberArk Secrets", "Secrets Management", $sprite="archimate/application-component")
    %% New External Services
    System_Ext(rh_ah, "Red Hat Automation Hub", "SaaS: Certified Collections", $sprite="redhat")
    System_Ext(quay, "Quay.io", "SaaS: Container Registry", $sprite="docker")
    System_Ext(redhat_com, "redhat.com", "SaaS: Subscriptions", $sprite="redhat")


    %% --- On-Premise Core Network ---
    Enterprise_Boundary(core_network, "NCSECU Core Network") {
        Person(sre, "SRE / Automation Engineer", "Develops and manages automation.", $sprite="user")

        System_Ext(rhel, "RHEL Servers", "On-prem Linux servers.", $sprite="redhat")
        System_Ext(win, "Windows Servers", "On-prem Windows servers.", $sprite="windows")
        System_Ext(vcenter, "VMware vCenter", "Virtualization Mgmt", $sprite="vmware")
        System_Ext(openshift, "OpenShift", "Container Platform", $sprite="redhat")
        System_Ext(bigiq, "F5 BIG-IQ", "Network Mgmt", $sprite="archimate/node")
        SystemDb_Ext(isilon, "Isilon Fileshare", "NFS/SMB Storage", $sprite="archimate/database-server")

        %% Satellite Infrastructure
        System_Boundary(satellite_infra, "Satellite Infrastructure") {
            System(satellite_server, "Satellite Server", "Content & Lifecycle Mgmt", $sprite="redhat")
            System(capsule, "Capsule Server", "Content Proxy", $sprite="archimate/node")
        }

        %% Control Plane
        System_Boundary(aap, "Control Plane (AAP)") {
            System(hub, "Private Automation Hub", "Registry", $sprite="archimate/artifact")
            System(controller, "Automation Controller", "Engine", $sprite="archimate/application-component")
            SystemDb(db, "PostgreSQL DB", "Database", $sprite="postgres")
        }
        
        %% Execution Plane
        Container_Boundary(execution_plane, "Execution Plane") {
            Container(ee_mesh, "Execution Node Mesh", "4-node mesh of execution containers.", $sprite="aws/General/Groups/AutoScalingGroup", $tags="container")
        }
    }

    %% --- Relationships (with Protocols) ---
    Rel(sre, scm, "Pushes playbooks", "Git")
    Rel(sre, controller, "Pushes playbooks", "Git")
    Rel(scm, controller, "Syncs projects", "HTTPS")
    Rel(controller, db, "Reads/Writes job data", "JDBC")
    Rel(controller, hub, "Pulls EE image", "HTTPS/API")
    Rel(controller, ee_mesh, "Orchestrates Jobs", "Internal")
    Rel(controller, cyb_secrets, "Retrieves credentials from", "HTTPS/API")
    Rel(cyb_ccp, rhel, "Manages privileged accounts on", "Agent")
    Rel(cyb_ccp, controller, "Manages privileged accounts on", "Agent")
    Rel(ee_mesh, rhel, "Runs on", "SSH")
    Rel(ee_mesh, win, "Runs on", "WinRM")
    Rel(ee_mesh, vcenter, "Automates VMs", "HTTPS/API")
    Rel(ee_mesh, openshift, "Manages Pods", "HTTPS/API")
    Rel(ee_mesh, bigiq, "Configures LTMs", "HTTPS/API")
    Rel(ee_mesh, isilon, "Reads/Writes files", "NFS/SMB")
    Rel(ee_mesh, cloud, "Runs on", "API/SSH")
    Rel(ee_mesh, helix, "Creates Incidents", "HTTPS/API")
    Rel(ee_mesh, infoblox, "Manages DNS/IPs", "HTTPS/API")
    Rel(controller, teams, "Sends notifications", "Webhook")

    %% --- New Relationships ---
    Rel(hub, rh_ah, "Syncs collections from", "HTTPS/API")
    Rel(hub, quay, "Syncs EEs from", "HTTPS/API")
    Rel(controller, redhat_com, "Reports Insights data", "HTTPS/API")
    Rel(satellite_server, redhat_com, "Syncs content from", "HTTPS")
    Rel(satellite_server, capsule, "Pushes content to")
    Rel(rhel, capsule, "Pulls content from", "HTTPS")

    %% --- Arrow Styling & Positioning ---
    UpdateRelStyle(sre, scm, $lineColor="black", $textColor="black", $offsetX="0", $offsetY="0")
    UpdateRelStyle(sre, controller, $lineColor="black", $textColor="black", $offsetX="0", $offsetY="0")
    UpdateRelStyle(scm, controller, $lineColor="#797D7F", $textColor="#797D7F", $lineStyle="dotted", $offsetX="0", $offsetY="0")
    UpdateRelStyle(controller, db, $lineColor="#154360", $textColor="#154360", $offsetX="0", $offsetY="0")
    UpdateRelStyle(controller, hub, $lineColor="#154360", $textColor="#154360", $offsetX="0", $offsetY="0")
    UpdateRelStyle(controller, ee_mesh, $lineColor="#27AE60", $textColor="#27AE60", $offsetX="0", $offsetY="0")
    UpdateRelStyle(controller, cyb_secrets, $lineColor="#797D7F", $textColor="#797D7F", $lineStyle="dotted", $offsetX="0", $offsetY="0")
    UpdateRelStyle(cyb_ccp, rhel, $lineColor="#E74C3C", $textColor="#E74C3C", $lineStyle="dotted", $offsetX="0", $offsetY="0")
    UpdateRelStyle(cyb_ccp, controller, $lineColor="#E74C3C", $textColor="#E74C3C", $lineStyle="dotted", $offsetX="0", $offsetY="0")
    UpdateRelStyle(ee_mesh, rhel, $lineColor="#154360", $textColor="#154360", $offsetX="0", $offsetY="0")
    UpdateRelStyle(ee_mesh, win, $lineColor="#154360", $textColor="#154360", $offsetX="0", $offsetY="0")
    UpdateRelStyle(ee_mesh, vcenter, $lineColor="#154360", $textColor="#154360", $offsetX="0", $offsetY="0")
    UpdateRelStyle(ee_mesh, openshift, $lineColor="#154360", $textColor="#154360", $offsetX="0", $offsetY="0")
    UpdateRelStyle(ee_mesh, bigiq, $lineColor="#154360", $textColor="#154360", $offsetX="0", $offsetY="0")
    UpdateRelStyle(ee_mesh, isilon, $lineColor="#154360", $textColor="#154360", $offsetX="0", $offsetY="0")
    UpdateRelStyle(ee_mesh, cloud, $lineColor="#797D7F", $textColor="#797D7F", $lineStyle="dotted", $offsetX="0", $offsetY="0")
    UpdateRelStyle(ee_mesh, helix, $lineColor="#797D7F", $textColor="#797D7F", $lineStyle="dotted", $offsetX="0", $offsetY="0")
    UpdateRelStyle(ee_mesh, infoblox, $lineColor="#797D7F", $textColor="#797D7F", $lineStyle="dotted", $offsetX="0", $offsetY="0")
    UpdateRelStyle(controller, teams, $lineColor="#797D7F", $textColor="#797D7F", $lineStyle="dotted", $offsetX="0", $offsetY="0")

    %% -- Styles for New  --
    UpdateRelStyle(hub, rh_ah, $lineColor="#797D7F", $textColor="#797D7F", $lineStyle="dotted", $offsetX="0", $offsetY="0")
    UpdateRelStyle(hub, quay, $lineColor="#797D7F", $textColor="#797D7F", $lineStyle="dotted", $offsetX="0", $offsetY="0")
    UpdateRelStyle(controller, redhat_com, $lineColor="#797D7F", $textColor="#797D7F", $lineStyle="dotted", $offsetX="0", $offsetY="0")
    UpdateRelStyle(satellite_server, redhat_com, $lineColor="#797D7F", $textColor="#797D7F", $lineStyle="dotted", $offsetX="0", $offsetY="0")
    UpdateRelStyle(satellite_server, capsule, $lineColor="#154360", $textColor="#154360", $offsetX="0", $offsetY="0")
    UpdateRelStyle(rhel, capsule, $lineColor="#154360", $textColor="#154360", $offsetX="0", $offsetY="0")

    UpdateLayoutConfig($c4ShapeInRow="5", $c4BoundaryInRow="4")
