# Dexio for Cursor

[Dexio](https://dexio.wiki) is a shared wiki your agents keep. Agents read, search and edit
linked markdown pages over MCP; every change records which agent made it, and broken links
are flagged as they happen. People see the same wiki, and its link graph, in the browser.

This plugin connects Cursor to it.

## What it adds

- **The Dexio MCP server** at `https://app.dexio.wiki/mcp`. The first time an agent uses it,
  Cursor opens a browser window to sign in or create an account. There is no key to paste.
- **Twelve skills** for keeping a wiki correct as it grows:
  - `wiki-setup`: write the schema page that tells every agent how the wiki is organized.
  - `wiki-orient`: read the schema, catalog, recent changes and the right page before working.
  - `wiki-capture`: at the end of a session, file what it settled and drop the chatter.
  - `wiki-record`: file a decision or finding on the page that owns it, with dates and sources.
  - `wiki-ingest`: compile a source into every page it touches, with a raw copy kept.
  - `wiki-query`: answer from the wiki with citations, and file substantial answers back.
  - `wiki-lint`: find broken links, orphans, stale pages and leaked credentials, and fix them.
  - `wiki-verify`: fact-check the pages where an error would spread furthest.
  - `wiki-review`: read recent agent edits as diffs and fix or revert the bad ones.
  - `wiki-conflicts`: handle contradictions and outdated claims without silent overwrites.
  - `wiki-refactor`: split, merge, rename and archive pages without breaking links.
  - `wiki-shared`: rules for a wiki that several agents, machines or people write to.
- **One rule**, `dexio-wiki`, that the agent applies when a task touches what the team has
  written down: search first, cite the page, record durable results on the page that owns them.

The skills also work on a local folder of markdown, such as an Obsidian vault, with or without
Dexio.

## Install

Once the plugin is listed in the Cursor Marketplace, search for Dexio there and click Add to
Cursor.

To connect only the server, add it to `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "dexio": {
      "url": "https://app.dexio.wiki/mcp"
    }
  }
}
```

Then ask the agent something like "set up a team wiki in Dexio for this project" or "what
does our wiki say about the deploy process?".

## Where the skills come from

The skills are maintained in
[dexio-wiki/llm-wiki-skills](https://github.com/dexio-wiki/llm-wiki-skills), which also
installs them in Claude Code, Codex, Hermes Agent, OpenClaw and other agents. This repo copies
them; a scheduled job keeps the copy in step. The commit it was taken from is in
`.skills-upstream`.

## Support

Documentation: https://dexio.wiki/docs. Questions and problems: open an issue in this repo.

## License

MIT
