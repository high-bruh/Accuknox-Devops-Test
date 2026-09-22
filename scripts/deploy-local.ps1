param(
    [string]$Image = "wisecow:local",
    [string]$Context = "docker-desktop"
)

$ErrorActionPreference = "Stop"
kubectl config use-context $Context
docker build -t $Image .
kubectl apply -f k8s/namespace.yaml
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout tls.key -out tls.crt -subj "/CN=wisecow.local"
kubectl -n wisecow create secret tls wisecow-tls --cert=tls.crt --key=tls.key --dry-run=client -o yaml | kubectl apply -f -
kubectl apply -f k8s/deployment.yaml -f k8s/service.yaml -f k8s/ingress.yaml -f k8s/network-policy.yaml
kubectl -n wisecow set image deployment/wisecow wisecow=$Image
kubectl -n wisecow rollout status deployment/wisecow