from kubernetes import client, config

def scan_rbac():
    try:
        config.load_kube_config()
        rbac_api = client.RbacAuthorizationV1Api()

        findings = []

        # ClusterRoleBindings
        crbs = rbac_api.list_cluster_role_binding()
        for crb in crbs.items:
            role_ref = crb.role_ref
            for subject in crb.subjects or []:
                if role_ref.name == "cluster-admin":
                    findings.append({
                        "type": "ClusterRoleBinding",
                        "subject": subject.name,
                        "namespace": subject.namespace if subject.namespace else "N/A",
                        "issue": "cluster-admin assigned",
                        "severity": "HIGH"
                    })

        # RoleBindings (namespaced)
        all_namespaces = client.CoreV1Api().list_namespace().items
        for ns in all_namespaces:
            rbs = rbac_api.list_namespaced_role_binding(ns.metadata.name)
            for rb in rbs.items:
                role_ref = rb.role_ref
                for subject in rb.subjects or []:
                    if role_ref.name == "admin" or "*" in role_ref.name:
                        findings.append({
                            "type": "RoleBinding",
                            "subject": subject.name,
                            "namespace": subject.namespace if subject.namespace else ns.metadata.name,
                            "issue": f"Over-permissioned role: {role_ref.name}",
                            "severity": "MEDIUM"
                        })

        return {"rbac": findings}

    except Exception as e:
        return {"rbac": [{"issue": str(e), "severity": "LOW"}]}
