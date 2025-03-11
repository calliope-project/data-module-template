# Data module template

A template for modular data workflows using [`snakemake`](https://snakemake.readthedocs.io/en/stable/), part of the [`clio`](https://clio.readthedocs.io/) toolset.

## Resources

To familiarise yourself with `clio` data modules:

- This template auto-generates a minimal example. You can find more about it in `tests/integration/Snakefile`.
- Read about the `clio` approach in [our documentation](https://clio.readthedocs.io/).
- Read about `snakemake` modularisation in [their documentation](https://snakemake.readthedocs.io/en/stable/snakefiles/modularization.html#modules).

## How to use this template

We recommend using [`pixi`](https://pixi.sh/) as your package manager. Once installed, do the following:

1. Install the templater tool [`copier`](https://copier.readthedocs.io/en/stable/).

    ```shell
    pixi global install copier
    ```

2. Use `copier` to build a project with this template. A new module will be created in a subdirectory corresponding to the module name you chose inside the given `destination_path`.

    ```shell
    copier copy https://github.com/calliope-project/data-module-template.git ./destination_path/
    ```

    If your terminal does not have access to `copier` then you may need to update your `PATH` variable to include `~/.pixi/bin`.

3. Answer some questions so can we pre-fill licensing, citation files, etc...
4. Initialise the `pixi` project environment of your new module.

    ```shell
    cd ./destination_path/module_name/  # navigate to the new project
    pixi install --all  # install the project environment
    ```

5. Extra: run the auto-generated example module!

    ```shell
    cd tests/integration  # go to the integration test...
    pixi run snakemake --use-conda  # run it!
    ```

## Features

- Standardised layout compliant with the [snakemake workflow catalogue's](https://snakemake.github.io/snakemake-workflow-catalog/#) listing requirements.
    - `resources/`: files external to the module.
        - `user/`: files that should be provided by users. Document them well!
        - `automatic/`: files that the module downloads before processing.
    - `results/`: files generated by the module's algorithms (both intermediate and final).
- Pre-made integration test setup for your module.
    - Continuous Integration (CI) settings, ready for [pre-commit.ci](https://pre-commit.ci/).
    - Premade `pytest` setup.
- Auto-generated documentation, ready for [Read the Docs](https://about.readthedocs.com/).

> [!IMPORTANT]
>
> A few things to be aware of.
>
> - **Modules do not work like regular snakemake workflows**
>     - The primary way to test them should be external (calling `module:`, passing resources, and requesting results). Check the pre-made example in `tests/integration` for more info.
>     - Internal access (calling the `all:` rule) will not work, as the module will not have the necessary `resources/` to execute properly.
> - **Please respect the 'specification' section of the documentation**
>     - `docs/hooks/clio_standard.py` will auto-generate documentation for you as long as certain files (e.g., `INTERFACE.yaml`, `CITATION.yaml`) are filled correctly.
>     - Please **do not modify this file** to ensure all data modules have a similar 'specification' section.
>     - If you wish to extend the documentation, feel free to add other sections.
>
