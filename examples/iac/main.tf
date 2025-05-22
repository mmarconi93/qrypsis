provider "azurerm" {
  features = {}
}

resource "azurerm_key_vault" "bad_example" {
  name                = "badkv"
  location            = "East US"
  resource_group_name = "example-rg"
  tenant_id           = "00000000-0000-0000-0000-000000000000"
  sku_name            = "standard"

  # 🚨 No public_network_access defined — will trigger Checkov
}