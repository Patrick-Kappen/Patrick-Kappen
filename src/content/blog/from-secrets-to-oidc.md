---
title: "From secrets to OIDC: GitHub, Azure and Entra"
description: "Why every stored pipeline secret is a liability, and how workload identity federation replaces them."
date: 2026-10-01
topic: identity
tags: [azure, github-actions, entra-id, security]
draft: true
---

## Why stored secrets are a problem

<!-- What goes wrong with client secrets in pipelines: rotation, leaks, who has them. -->

## How workload identity federation works

<!-- GitHub's OIDC token, the federated credential in Entra, and what the subject claim pins. -->

## Setting it up

<!-- The app registration or managed identity, the federated credential, and the workflow. -->

```yaml
permissions:
  id-token: write
  contents: read
```

## Scoping the trust

<!-- Branches, environments and pull requests: which subject to trust, and why environments matter. -->

## What changed in practice

<!-- Rotation gone, secrets gone, approvals through environments. -->
