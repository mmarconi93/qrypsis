from azure.mgmt.containerregistry import ContainerRegistryManagementClient

def scan_acr(credential, subscription_id):
    acr_client = ContainerRegistryManagementClient(credential, subscription_id)
    findings = []

    for registry in acr_client.registries.list():
        if registry.admin_user_enabled:
            findings.append({
                "type": "ACR",
                "name": registry.name,
                "issue": "Admin user enabled",
                "severity": "HIGH"
            })
        if registry.public_network_access == "Enabled":
            findings.append({
                "type": "ACR",
                "name": registry.name,
                "issue": "Public access enabled",
                "severity": "HIGH"
            })

    return {"azure_acr": findings}
