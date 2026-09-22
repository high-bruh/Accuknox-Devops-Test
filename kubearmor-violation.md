# KubeArmor Violation Evidence (Simulation)

> **SIMULATION - NOT A REAL CLUSTER ALERT**
>
> This file documents the expected KubeArmor output. It must not be presented
> as a captured enforcement screenshot.

## Workload

```text
Namespace: wisecow
Policy:   wisecow-zero-trust
Action:   Block
Rule:     /usr/bin/cat
Target:   /etc/hostname
```

## KubeArmor test

```console
$ kubectl -n wisecow exec deploy/wisecow -- /usr/bin/cat /etc/hostname
Error from server: command terminated with exit code 1
```

## KubeArmor alert

```text
Operation: Blocked
Namespace: wisecow
Pod: wisecow-<generated-name>
Process: /usr/bin/cat
Resource: /etc/hostname
Policy: wisecow-zero-trust
Action: Block
```

## Local limitation

The local Windows Docker Desktop / WSL2 Kind environment does not expose BPF
LSM to the Kubernetes node. The actual test returned exit code 0 and emitted
no enforcement alert. Genuine screenshot evidence requires a Linux node with
BPF LSM support.