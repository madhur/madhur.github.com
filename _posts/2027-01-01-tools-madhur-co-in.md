---
layout: blog-post
title: "tools.madhur.co.in - Developer Utilities for Data Transformation"
excerpt: "A collection of client-side tools for YAML/JSON conversion, JSON minification, and JOLT transformations"
disqus_id: /2027/01/01/tools-madhur-co-in/
tags:
    - Web Development
    - Tools
    - JSON
    - YAML
---

I've published a set of developer utilities at [tools.madhur.co.in](https://tools.madhur.co.in) that handle common data transformation tasks entirely in the browser. The site provides three main tools: YAML/JSON conversion, JSON minification, and JOLT transformations.

## Available Tools

### 1. YAML ↔ JSON Escaped Converter

Converts between YAML format and JSON-escaped strings. This is particularly useful when working with configuration management systems or APIs that require JSON-escaped YAML content.

**Use cases:**
- Converting Kubernetes ConfigMaps or Secrets between YAML and JSON-escaped format
- Working with infrastructure-as-code tools that store YAML as JSON strings
- Preparing YAML content for JSON payloads in API requests

The conversion uses `js-yaml` library for parsing and `JSON.stringify()` for proper escaping, ensuring all special characters, newlines, and Unicode sequences are correctly handled.

### 2. JSON Minify/Unminify

Minifies JSON to a single line or pretty-prints it with proper indentation. Useful for reducing payload sizes or improving readability.

**Use cases:**
- Reducing JSON payload size for API requests
- Formatting minified JSON responses for debugging
- Preparing JSON for embedding in HTML/JavaScript

### 3. JOLT Transform

Performs JSON-to-JSON transformations using JOLT (JSON Object Language Transform) specifications. JOLT is commonly used in data pipeline transformations, especially in Apache NiFi and similar ETL tools.

**Use cases:**
- Testing JOLT transformation specs before deploying to production
- Converting between different JSON schema formats
- Data mapping and restructuring for API integrations

The tool connects to a Lambda-based JOLT transformation service, allowing you to test transformations in real-time.

## Technical Implementation

The site is built as a single-page application with:

- **Client-side only**: All processing happens in the browser using JavaScript. No data is sent to a server except for JOLT transformations (which require server-side processing).
- **CodeMirror integration**: Syntax-highlighted editors for better code readability with support for YAML and JavaScript modes.
- **Dark mode**: Toggle between light and dark themes with preference stored in localStorage.
- **Responsive design**: Works on desktop and mobile devices.

### Architecture

```
tools.madhur.co.in
├── Single HTML file (yaml_json_converter.html)
├── CDN dependencies:
│   ├── js-yaml (YAML parsing)
│   ├── CodeMirror (code editor)
│   └── Material theme (dark mode)
└── JOLT API endpoint (AWS Lambda)
```

The site is hosted on GitHub Pages with a custom domain. The HTML file is served directly without any build process, making updates straightforward.

## Who Is This For?

**DevOps Engineers**: Converting between YAML and JSON formats is common when working with Kubernetes, Ansible, Terraform, or similar tools. The JSON-escaped format is often required when storing YAML in JSON-based configuration systems.

**API Developers**: When working with APIs that accept JSON-escaped strings or need to minify JSON payloads, these tools provide quick conversion without leaving the browser.

**Data Engineers**: JOLT transformations are essential for data pipeline work. Being able to test JOLT specs interactively speeds up development and debugging.

**Frontend Developers**: JSON minification and formatting are daily tasks when working with API responses or preparing data for client-side consumption.

## Privacy and Security

Since all processing (except JOLT) happens client-side:
- No data is logged or stored on servers
- YAML/JSON conversion and minification work entirely offline
- JOLT transformations are sent to the API but not persisted

The site uses HTTPS with a GitHub Pages SSL certificate, ensuring secure connections.

## Future Enhancements

Potential additions could include:
- JSON Schema validation
- Additional transformation formats (XML, CSV)
- Batch processing for multiple files
- Export/import functionality

The codebase is straightforward to extend given the single-file architecture.

## Access

The tools are available at [tools.madhur.co.in](https://tools.madhur.co.in). No registration or installation required—just open the site and start using the tools.

