from setuptools import setup
import sys


if __name__ == "__main__":
    # Allow python setup.py sdist to work, so that the sdist can be
    # generated and uploaded to PyPI.
    doing_sdist = len(sys.argv) >= 2 and sys.argv[1] == "sdist"

    if not doing_sdist:
        raise SystemExit(
            "The functionality of the 'sinabs-dynapcnn' package has been fully"
            " merged into sinabs.\nInstalling 'sinabs-dynapcnn' in addition"
            " to sinabs is not required anymore.\n"
            "\nIt is recommended to follow these steps:\n\n"
            "- Use 'pip install sinabs --upgrade' to make sure that the most "
            " recent version of sinabs (2.0 or higher) is installed.\n"
            "- Replace 'sinabs-dynapcnn' with 'sinabs>=2.0 in your pip"
            " requirement files.\n\n"
            "Even if your projects use sinabs-dynapcnn, there should be no need"
            " to change any code.\nImport statements containing the term"
            " `sinabs.backend.dynapcnn` are still the same.\n\n"
            "If for some reason you require a specific, older, version of"
            " 'sinabs-dynapcnn', make sure to install it along with a version"
            " of sinabs that is smaller than 2.0."
        )

    setup()
