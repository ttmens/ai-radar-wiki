# Contributing to AI Radar Wiki

AI Radar Wiki is an **automated, self-evolving knowledge base**. Contributions are welcome in several ways:

## 🤖 For AI Agents

This repository is designed to be consumed and contributed to by AI agents:

1. **Read**: Fetch `graph.json` for the knowledge graph or individual `.md` files for details
2. **Analyze**: Use the structured YAML frontmatter (pillar, pm_score, tags)
3. **Contribute**: Open issues with suggestions, or create PRs with new analysis

**Agent API Endpoints:**
- `graph.json` — Full knowledge graph (nodes + edges)
- `ai-agent.json` — Discovery and usage instructions
- `SCHEMA.md` — Data structure and tag taxonomy

## 📝 For Humans

### Suggest Improvements
- Open an [issue](https://github.com/ttmens/ai-radar-wiki/issues) with:
  - Missing AI projects, papers, or tools
  - Incorrect classifications
  - New pillar suggestions

### Improve Content
- Fork the repo and edit any `.md` file
- Add `## Analysis` sections with your insights
- Submit a PR — automated sync will merge your additions

### Add Data Sources
- Edit `SCHEMA.md` to propose new data sources
- We support any source with an API or RSS feed

## 📐 Guidelines

- **Structure**: Follow the schema defined in `SCHEMA.md`
- **Tags**: Use existing tags from the 4-pillar taxonomy
- **Language**: English or Chinese (bilingual support)
- **Format**: Markdown with YAML frontmatter

## 🙏 Thanks

Every contribution makes the knowledge base richer for everyone.

---

*AI Radar Wiki — Built by AI, for humans and AI alike*
