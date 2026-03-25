---
layout: blog-post
title: "Why My SSH Key Wasn't Being Used for Git Despite Multi-Key Setup"
excerpt: "How the SSH agent silently overrides an explicitly specified key, and why adding IdentitiesOnly=yes to git sshCommand fixed it."
disqus_id: /2027/06/01/ssh-multi-account-github-identitiesonly/
tags:
    - SSH
    - Git
    - GitHub
    - Linux
---

*This article was written with the assistance of AI.*

---

I manage two GitHub accounts — personal and work — on the same machine. I had set up folder-based SSH key switching using git's `includeIf` directive. The setup looked correct, but git kept authenticating with the wrong key and I kept getting:

```
ERROR: Repository not found.
fatal: Could not read from remote repository.
```

This is what was going wrong and how I fixed it.

## My Setup

I use `includeIf` in `~/.gitconfig` to apply different configs based on the working directory:

```ini
[includeIf "gitdir:/home/madhur/github/"]
    path = /home/madhur/.gitconfig-work

[includeIf "gitdir:/home/madhur/gitpersonal/"]
    path = /home/madhur/.gitconfig-personal
```

And in `~/.gitconfig-work`:

```ini
[core]
    sshCommand = ssh -i ~/.ssh/id_rsa_work

[user]
    email = user@company.com
    name = Madhur Ahuja
```

I verified the config was being applied correctly:

```bash
git config --show-origin core.sshCommand
# file:/home/madhur/.gitconfig-work   ssh -i ~/.ssh/id_rsa_work
```

The right config was being picked up. Yet git was still failing.

## The Problem: SSH Agent Takes Priority

The issue is how SSH handles the `-i` flag when an SSH agent is running.

When you specify `-i keyfile`, SSH does **not** exclusively use that key. It adds the specified key to the list of identities to try, but **the SSH agent's loaded keys are tried first**. SSH works through identities in this order:

1. Keys already loaded in the SSH agent
2. Keys specified via `-i` or `IdentityFile`

My agent had my personal key loaded (which happens automatically after login), and GitHub recognized it — so SSH authenticated with my personal account before ever trying the work key.

I confirmed this with verbose SSH output:

```bash
ssh -i ~/.ssh/id_rsa_work -vT git@github.com 2>&1 | grep -E "Offering|accepts"
```

Output:
```
debug1: Offering public key: /home/madhur/.ssh/id_rsa RSA SHA256:xxxxx agent
debug1: Server accepts key: /home/madhur/.ssh/id_rsa RSA SHA256:xxxxx agent
```

The agent key (`id_rsa`, personal) was offered and accepted. SSH never got to trying `id_rsa_work`.

## The Fix: IdentitiesOnly=yes

The `IdentitiesOnly` option tells SSH to use **only** the explicitly configured keys, ignoring everything the agent offers.

I updated `~/.gitconfig-work`:

```ini
[core]
    sshCommand = ssh -i ~/.ssh/id_rsa_work -o IdentitiesOnly=yes
```

Now SSH skips the agent entirely and only uses `id_rsa_work`. Verifying:

```bash
ssh -i ~/.ssh/id_rsa_work -o IdentitiesOnly=yes -vT git@github.com 2>&1 | grep -E "Offering|accepts"
```

```
debug1: Offering public key: /home/madhur/.ssh/id_rsa_work RSA SHA256:yyyyy explicit
debug1: Server accepts key: /home/madhur/.ssh/id_rsa_work RSA SHA256:yyyyy explicit
```

And `git pull` worked.

## The Same Applies to ~/.ssh/config

The same issue affects SSH host aliases in `~/.ssh/config`. The `IdentityFile` directive alone doesn't prevent agent keys from being offered. It should always be paired with `IdentitiesOnly yes`:

```
Host github-work
    HostName github.com
    IdentityFile ~/.ssh/id_rsa_work
    IdentitiesOnly yes
```

Without `IdentitiesOnly yes`, the host alias merely adds the specified key to the list — it doesn't remove agent keys from contention.

## A Bonus Gotcha: Missing .pub File

While debugging, I also discovered my `id_rsa_work.pub` file was missing — only the private key existed. SSH needs the public key file to pre-screen identities. Without it, SSH skips the key entirely without any warning.

If the `.pub` file is missing, regenerate it from the private key:

```bash
ssh-keygen -y -f ~/.ssh/id_rsa_work > ~/.ssh/id_rsa_work.pub
```

## The Documentation

From `man ssh_config`:

> **IdentitiesOnly**
> Specifies that ssh(1) should only use the configured authentication identity and certificate files (either the default files, or those explicitly configured in the ssh_config files or passed on the ssh(1) command-line), even if ssh-agent(1) or a PKCS11Provider or SecurityKeyProvider offers more identities.

It's documented, but easy to miss. Most SSH multi-account guides show the `IdentityFile` setup but leave out `IdentitiesOnly yes`.

## Conclusion

Whenever you configure SSH to use a specific key — whether via `~/.ssh/config` or git's `sshCommand` — always add `IdentitiesOnly yes` (or `-o IdentitiesOnly=yes`). Without it, the SSH agent silently overrides the intended key with no obvious error explaining why.
