---
title: "Two GitHub accounts, one machine, zero switching"
description: "I split my GitHub life in two and refused to switch accounts by hand ever again. Nix made it easy, git and gh made it interesting."
date: 2026-10-02
topic: nix
tags: [nixos, home-manager, git, github, gh-cli, sops, identity, developer-experience]
image: /assets/blog/nix-snowflake-cover.svg
imageAlt: "The Nix snowflake logo on a dark blue background"
imageCredit: "Nix snowflake by the NixOS project, CC BY 4.0"
imageCreditUrl: "https://github.com/NixOS/nixos-artwork/tree/master/logo"
draft: false
---

Okay, I have to show you this, because it made me unreasonably happy:

```shell-session
~/hub/private/site $ gh api user --jq .login
Patrick-Kappen

~/hub/work/platform $ gh api user --jq .login
work-account
```

Same machine. Same command. Two different people. 🎉

I didn't run `gh auth switch`. I didn't set up SSH aliases. My remotes are just
normal `https://github.com/…` URLs. I `cd` into a folder, and my machine simply
*knows* who I am in there.

Let me tell you how I got here, and about the two moments where I stared at my
terminal thinking "but… why?!"

## How I ended up with two accounts

For years I had one GitHub account. Over time it quietly became my work
account too. Admin in the company organisation, enterprise owner, a Copilot
seat, my work email address attached. Super convenient!

Until this week, when I wanted a public profile that is actually *mine*. My
own projects, my own blog, my own story. Not something that half belongs to my
employer.

So I split it: one personal account, one work account. Clean. Very satisfying.

And then I immediately created a new problem. Two accounts on one machine
means one question before every commit, every push and every pull request:
*wait, who am I right now?*

I know myself. If I have to remember that by hand, I *will* get it wrong one
day. And those mistakes are public: a commit with the wrong email address, or
a pull request from the wrong account in someone else's repository. No thanks.

So I made a rule: **the folder decides who I am.** Everything under
`~/hub/work` is work. Everything else is me.

## Nix makes the boring part boring (in a good way)

This is the bit where I love Nix a little bit more every time.

I have one tiny list of work folders, and everything else reads from it:

```nix
workPaths = [ "~/hub/work" ];
```

Git has a lovely feature called `includeIf`: "if this repository lives here,
load this extra config too". Home Manager turns that into a one-liner per
folder:

```nix
programs.git.includes = map (workPath: {
  condition = "gitdir:${workPath}/**";
  path = "${config.xdg.configHome}/git/work.inc";
}) identity.workPaths;
```

That extra file holds my work email address. And I really didn't want that
address sitting in a Git repository or in the Nix store, where anyone on the
machine can read it. So sops writes the file for me when the system activates:

```nix
sops.templates."git-work.inc" = {
  path = "${config.xdg.configHome}/git/work.inc";
  content = ''
    [user]
      email = ${config.sops.placeholder.WORK_EMAIL}
    [credential "https://github.com"]
      helper =
      helper = ${ghCredential identity.workGithubUser}
  '';
};
```

Commits: sorted! ✅

Now see that empty `helper =` line? Looks like a typo, right? Hold that
thought. We'll get there. 😄

## Surprise #1: gh doesn't listen

To push, git needs a token. And `gh` already has tokens for both of my
accounts. Even better: `gh` can act as git's credential helper. Perfect! Plug
it in, done!

…except it wasn't.

Git politely tells the helper *which* user it wants. And `gh` just… ignores
that. It always hands over the token of the account you used **last**. With two
accounts, that's basically a coin toss. 🪙

The good news: `gh auth token -u <user>` *does* listen. So I wrote my own
helper. It's five lines:

```nix
ghCredential =
  user:
  pkgs.writeShellScript "gh-credential-${user}" ''
    cat >/dev/null
    [ "$1" = get ] || exit 0
    token=$(${lib.getExe pkgs.gh} auth token -u ${user}) || exit 0
    echo "username=${user}"
    echo "password=$token"
  '';
```

Personal helper in the main config, work helper in the work file. Done!

Right? …right?

## Surprise #2: git keeps a queue

Nope. A work push still went out as my personal account. 🙃

Here's the thing I didn't know: when you set a credential helper in an extra
config file, git doesn't *replace* the one you already had. It **adds** it to a
queue, and asks them one by one. My personal helper was first in line,
cheerfully handed over a personal token, and that was that.

The fix is that "typo" from earlier. An empty `helper =` tells git: *forget
everything before this line*. You can actually watch it happen:

```shell-session
$ git config --get-all credential.https://github.com.helper
/nix/store/…-gh-credential-Patrick-Kappen

/nix/store/…-gh-credential-work-account
```

Personal. *Reset.* Work. Git starts over after the empty line, so only my work
helper counts. One empty line! I love it and I hate it. 😅

## Bonus: making gh follow along too

Git was happy now, but `gh` itself still used whatever account was active. Luckily
`gh` listens to a `GH_TOKEN` environment variable. So I put a tiny wrapper in
front of it that looks at where I am and hands over the right token:

```nix
ghAccountWrapper = pkgs.writeShellScript "gh" ''
  real=${lib.getExe pkgs.gh}
  if [[ -z ''${GH_TOKEN:-}''${GITHUB_TOKEN:-} && ''${1:-} != auth ]]; then
    user=${identity.githubUser}
    for dir in "$PWD/" "$(pwd -P)/"; do
      for work in ${workPaths}; do
        [[ $dir == "$work"* ]] && user=${identity.workGithubUser}
      done
    done
    if token=$("$real" auth token -u "$user" 2>/dev/null); then
      export GH_TOKEN=$token
    fi
  fi
  exec "$real" "$@"
'';
```

A few little things I'm quite proud of:

- It also checks `pwd -P`, so it still works when I reach a work folder through
  a symlink.
- If a token is already set, that one wins. My scripts and CI stay in charge.
- `gh auth` is left alone, so logging in works like it always did.

And with `symlinkJoin` I only swap out the `gh` binary itself, so tab
completion and man pages keep working:

```nix
ghPerDirectory = pkgs.symlinkJoin {
  name = "gh-per-directory";
  paths = [ pkgs.gh ];
  meta.mainProgram = "gh";
  postBuild = ''
    rm "$out/bin/gh"
    install -m 755 ${ghAccountWrapper} "$out/bin/gh"
  '';
};
```

## It's not perfect (and that's fine)

Being honest here:

- Git looks at where the **repository** is; my `gh` wrapper looks at where
  **I** am. Usually that's the same place. If I run `gh -R work-org/repo` from
  a personal folder, I'm still me.
- You could do all of this with SSH aliases (`git@github-work:org/repo`). That
  works too! But then every remote needs a special URL, and copy-pasting a
  clone URL from GitHub no longer just works. Not for me.
- You still need to log in to both accounts with `gh auth login` once. After
  that the tokens live in the system keyring, not in a dotfile.

## What I took away from this

The happy path was easy. It always is. The fun was in the two surprises: a
tool that quietly answered for the wrong person, and a config line that
*added* when I thought it *replaced*.

That's identity in a nutshell, really. It's not about the login screen. It's
about all the quiet places where software decides who you are on your behalf.

And now every one of my machines gets it right every single time, without me thinking about
it. That's the best kind of automation. 🚀

Got a setup like this, or a smarter trick? I'd love to hear it. Send me a
message on [LinkedIn](https://www.linkedin.com/in/patrick-kappen/) or drop me
an email at [patrick@kappen.io](mailto:patrick@kappen.io).
