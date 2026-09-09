# Claude Development Guidelines

## Rules
1. **Do not use pip/npm/uv/docker unless explicitly told to !**
2. You can only use git to revert bad changes, no commit, no push !

## Coding philosophy
* Keep changes to a minimum
* Rendering can be unoptimized

## Project Structure
* `.run/` - Ignore
* `.data/`
  * `applets/` - Definitions for applets that can be included anywhere
  * `articles/` - Ignore
  * `brands/` - Ignore
  * `code/` - Ignore 
  * `downloads/` - Definitions for the releases rendered on some pages; avoid unless required
  * `pages/` - Definitions for pages to render 
  * `projects/` - Definitions for projects' pages to render [project.jinja](templates/pages/project.jinja)
  * `strings/` - Ignore
  * `tools/` - Definitions for tools' pages to render [tool.jinja](templates/pages/tool.jinja)
* `docker/` - Ignore
* `nibblepoker/` - Python code for pre-rendering the website
* `scripts/` - Ignore, those are build scripts
* `static/` - Ignore, it's the output
* `templates/` - Jinja templates
* `prerender.py` - Script used to pre-render the website
