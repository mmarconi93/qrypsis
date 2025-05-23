from azure.identity import DefaultAzureCredential
from azure.mgmt.keyvault import KeyVaultManagementClient
from azure.keyvault.secrets import SecretClient
from azure.mgmt.resource import SubscriptionClient
from azure_acr_scanner import scan_acr
from datetime import datetime, timedelta
from azure_nsg_scanner import scan_nsg

def scan_azure(redact=True):
    credential = DefaultAzureCredential(exclude_interactive_browser_credential=False)

    # Get default subscription
    sub_client = SubscriptionClient(credential)
    subscription = next(sub_client.subscriptions.list())
    subscription_id = subscription.subscription_id

    kv_client = KeyVaultManagementClient(credential, subscription_id)
    findings = []

    for vault in kv_client.vaults.list():
        vault_name = vault.name
        resource_group = vault.id.split("/")[4]
        location = vault.location
        public_access = vault.properties.public_network_access

        if public_access == "Enabled":
            findings.append({
                "type": "KeyVault",
                "vault": vault_name,
                "issue": "Public network access is ENABLED",
                "resource_group": resource_group,
                "location": location,
                "severity": "HIGH"
            })

        # Scan secrets for expiration
        try:
            vault_uri = vault.properties.vault_uri
            secret_client = SecretClient(vault_url=vault_uri, credential=credential)
            secrets = secret_client.list_properties_of_secrets()

            for s in secrets:
                secret_name = s.name if not redact else "[REDACTED]"
                if s.expires_on and s.expires_on < datetime.utcnow() + timedelta(days=30):
                    findings.append({
                        "type": "Secret",
                        "vault": vault_name,
                        "secret": secret_name,
                        "issue": f"Secret expires on {s.expires_on.date()}",
                        "resource_group": resource_group,
                        "location": location,
                        "severity": "MEDIUM"
                    })
        except Exception as e:
            findings.append({
                "type": "KeyVault",
                "vault": vault_name,
                "issue": f"Failed to scan secrets: {str(e)}",
                "severity": "LOW"
            })

    acr_results = scan_acr(credential, subscription_id)
    findings.extend(acr_results.get("azure_acr", []))

    nsg_results = scan_nsg(credential, subscription_id)
    findings.extend(nsg_results.get("azure_nsg", []))

    return {"azure": findings}
