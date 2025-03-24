# Data module template

A template for modular data workflows using [`snakemake`](https://snakemake.readthedocs.io/en/stable/), part of the [`clio`](https://clio.readthedocs.io/) toolset.

## Resources

To familiarise yourself with `clio` data modules:

- Check the auto-generated minimal example. You can find it in `tests/integration/Snakefile`.
- Read about the `clio` approach in [our documentation](https://clio.readthedocs.io/).
- Read about `snakemake` modularisation in [their documentation](https://snakemake.readthedocs.io/en/stable/snakefiles/modularization.html#modules).

## How to use this template

We recommend using [`pixi`](https://pixi.sh/) as your package manager. Once installed, do the following:

1. Install the templater tool [`copier`](https://copier.readthedocs.io/en/stable/).

    ```shell
    pixi global install copier
    ```

2. Use `copier` to build a project with this template.
    A new module will be created in the directory you chose.
    We recommend you use the module name as the directory name.

    ```shell
    copier copy https://github.com/calliope-project/data-module-template.git ./path/to/<module_name>
    ```

    If your terminal does not have access to `copier` then you may need to update your `PATH` variable to include `~/.pixi/bin`.

3. Answer some questions so can we pre-fill licensing, citation files, etc...
4. Initialise the `pixi` project environment of your new module.

    ```shell
    cd ./path/to/<module_name> # navigate to the new project
    pixi install --all  # install the project environment
    ```

5. Extra: run the auto-generated example module!

    ```shell
    cd tests/integration  # go to the integration test...
    pixi run snakemake --use-conda  # run it!
    ```

## Features

- Standardised layout compliant with the [snakemake workflow catalogue's](https://snakemake.github.io/snakemake-workflow-catalog/#) listing requirements.
    - `resources/`: files needed for the module's processes.
        - `user/`: files that should be provided by users. Document them well!
        - `automatic/`: files that the module downloads or prepares in intermediate steps.
    - `results/`: files generated by the module's algorithms that are relevant to the user.
- Pre-made integration test setup for your module.
    - Continuous Integration (CI) settings, ready for [pre-commit.ci](https://pre-commit.ci/).
    - Premade `pytest` setup.
- Optional auto-generated documentation, ready for [Read the Docs](https://about.readthedocs.com/) or [Github Pages](https://pages.github.com/).

> [!IMPORTANT]
>
> A few things to be aware of.
>
> - **Modules do not work like regular snakemake workflows**
>     - The primary way to test them should be external (calling `module:`, passing resources, and requesting results). Check the pre-made example in `tests/integration` for more info.
>     - Internal access (e.g., calling the `all:` rule) may not work, as the module may not have the necessary `resources/` to execute properly.
> - **Please be sure to maintain the following files to ensure `clio` compatibility**
>     - These are:
>         - `INTERFACE.yaml`: a simple description of the module's input/output structure.
>         - `config/example.yaml`: a basic functioning example of how to configure this module.
>         - `workflow/internal/config.schema.yaml`: the module's configuration schema, used by `snakemake` for [validation](https://snakemake.readthedocs.io/en/stable/snakefiles/configuration.html).
>         - `AUTHORS` / `CITATION.cff` / `LICENSE`: licensing and attribution of this module's code and methods.
>     - If the optional auto-generated documentation was selected, `docs/hooks/clio_standard.py` will use these files to automatically generate a basic Read the Docs website.
