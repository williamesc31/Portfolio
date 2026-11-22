# GitHub Pages Maintenance

The portfolio is published at https://williamesc31.github.io/Portfolio/ from the `main` branch and `/docs` folder.

To maintain the portfolio:

1. Update a project's code and inputs under `projects/<name>/`.
2. Run `python scripts/run_all.py` to reproduce all outputs and write VERIFICATION.json.
3. Run `python scripts/build_portfolio.py` to refresh project documentation, downloadable READMEs, and the website catalog.
4. Commit the intended source and generated output changes to `main`.
5. Check the repository's Pages build and deployment run, then review the public site.

To preview the website locally, run `python -m http.server 8000 --directory docs` and open http://localhost:8000/ .

Submit the published website URL in Blackboard. Repository files and the website source are retained together; no ChatGPT hosting is required to open the public portfolio.
