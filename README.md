# Wisecow on Kubernetes

This repository packages the Wisecow Bash web server and deploys it behind a Kubernetes Service and an NGINX Ingress with TLS.

## Architecture

`HTTPS client -> NGINX Ingress (TLS) -> ClusterIP Service -> Wisecow Pods (HTTP:4499)`

The Deployment runs two replicas with non-root, read-only, least-privilege container settings. A default-deny egress policy is included. The image is published to GHCR by GitHub Actions and the optional deployment job rolls the immutable commit image into a configured cluster.

## Run locally with Docker

```bash
docker build -t wisecow:local .
docker run --rm -p 4499:4499 wisecow:local
python scripts/health_checker.py http://localhost:4499/
```

## Kubernetes deployment

The manifests expect an image named `ghcr.io/REPLACE_OWNER/wisecow`. Replace that value with the GitHub owner, and make the package public or configure an image pull secret.

An NGINX Ingress Controller is required. Create a local certificate and TLS secret (PowerShell):

```powershell
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout tls.key -out tls.crt -subj "/CN=wisecow.local"
kubectl create namespace wisecow
kubectl -n wisecow create secret tls wisecow-tls --cert=tls.crt --key=tls.key
kubectl apply -f k8s/deployment.yaml -f k8s/service.yaml -f k8s/ingress.yaml -f k8s/network-policy.yaml
kubectl -n wisecow set image deployment/wisecow wisecow=ghcr.io/OWNER/wisecow:latest
```

Add `127.0.0.1 wisecow.local` to the hosts file and test with `curl -k https://wisecow.local/`.

## CI/CD setup

Every pull request runs shell, Python, and manifest validation. A push to `main` builds, scans, and pushes `ghcr.io/<owner>/wisecow:<commit-sha>`. To enable continuous deployment, create a protected `production` environment with a `KUBE_CONFIG` secret containing the base64-encoded kubeconfig. The deploy job uses `kubectl rollout status` and fails on an unsuccessful rollout.

## Assessment scripts

The two selected Problem Statement 2 objectives are:

* `scripts/health_checker.py`: checks HTTP status and timeout, suitable for probes and CI.
* `scripts/log_analyzer.py`: reports request totals, 404 count, top pages, and top client IPs from combined access logs.

## KubeArmor zero-trust policy

`k8s/kubearmor-policy.yaml` blocks unexpected shells, network raw sockets, and writes/reads in sensitive paths for Wisecow pods. Apply it after installing KubeArmor:

```bash
helm repo add kubearmor https://kubearmor.github.io/KubeArmor
helm repo update
helm install kubearmor kubearmor/KubeArmor --namespace kubearmor --create-namespace --wait
```

```bash
kubectl apply -f k8s/kubearmor-policy.yaml
kubectl -n wisecow get kubearmorpolicy
kubectl -n wisecow logs -l app.kubernetes.io/name=wisecow
```

To demonstrate enforcement, exec into a pod and attempt `cat /etc/hostname`; the policy blocks the `cat` process and KubeArmor should report the violation in its logs:

```bash
kubectl -n wisecow exec deploy/wisecow -- /usr/bin/cat /etc/hostname
kubectl -n kubearmor logs daemonset/kubearmor --since=2m | grep -Ei 'block|denied|wisecow|cat'
```

Capture the terminal output showing the denied command and KubeArmor alert as `docs/kubearmor-violation.png` when running against a Linux host with BPF LSM support.
