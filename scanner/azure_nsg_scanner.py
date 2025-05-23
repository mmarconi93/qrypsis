from azure.mgmt.network import NetworkManagementClient
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import SubscriptionClient

def scan_nsg(credential, subscription_id):
    network_client = NetworkManagementClient(credential, subscription_id)
    findings = []

    for nsg in network_client.network_security_groups.list_all():
        for rule in nsg.security_rules:
            # Check if rule is Allow and applies to 0.0.0.0/0
            if rule.access.lower() == "allow" and rule.direction.lower() == "inbound":
                if rule.source_address_prefix in ["*", "0.0.0.0/0", "Internet"]:
                    findings.append({
                        "type": "NSG",
                        "nsg_name": nsg.name,
                        "resource_group": nsg.id.split("/")[4],
                        "rule_name": rule.name,
                        "priority": rule.priority,
                        "port_range": rule.destination_port_range,
                        "issue": f"Insecure NSG rule allows inbound from {rule.source_address_prefix}",
                        "severity": "HIGH" if rule.destination_port_range in ["22", "3389"] else "MEDIUM"
                    })
    return {"azure_nsg": findings}