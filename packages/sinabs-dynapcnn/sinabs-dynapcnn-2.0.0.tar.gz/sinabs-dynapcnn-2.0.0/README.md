# :warning: Warning: The 'sinabs-dynapcnn' package is deprecated! :warning:
The functionality of the sinabs-dynapcnn package has been fully merged into sinabs.
Installing sinabs-dynapcnn in addition to sinabs is not required anymore.

It is recommended to follow these steps:

- Use `pip install sinabs --upgrade` to make sure that the most  recent version of sinabs (2.0 or higher) is installed.
- Replace `sinabs-dynapcnn` with `sinabs>=2.0` in your pip requirement files.

Even if your projects use sinabs-dynapcnn, there should be no need to change any code.
Import statements containing the term `sinabs.backend.dynapcnn` are still the same.

If for some reason you require a specific, older, version of sinabs-dynapcnn, make sure to install it along with a version of sinabs that is smaller than 2.0.

To get the newest code, reoport bugs, or push changes, please go to [the github repository of sinabs](https://github.com/synsense/sinabs/).

Documentation
-------------

You can find the latest documentation for sinabs at [https://sinabs.ai/](https://sinabs.ai/)
