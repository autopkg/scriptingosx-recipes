# Scripting OS X - Shared Processors

## Processors for Recipes

### FileTemplate

This processor can be used to read a file with placeholder variables and write the result to a new file (presumably in the package being built). I use the `FileTemplate` processor in the [`FirefoxPrefs.pkg`](https://github.com/autopkg/scriptingosx-recipes/blob/master/FirefoxPrefs/FirefoxPrefs.pkg.recipe) recipe to insert a javascript settings file with the proper values.

Required Input Variables:

- `destination_path`: (required) path to write the resulting file to
- `template_path`: (required) path to the template file.

String sequences in the template file which are enclosed with `%` symbols such as `%version%` or `%homepage_url` will be replaced with the value from the `autopkg` variable. You can use variables defined or obtained in previous recipe steps (e.g. `%version%` or `%NAME%`) or add additional values as input variables for the `FileTemplate` processor (see `homepage_url` in [`FirefoxPrefs.pkg`](https://github.com/autopkg/scriptingosx-recipes/blob/master/FirefoxPrefs/FirefoxPrefs.pkg.recipe))

Use `com.scriptingosx.processors/FileTemplate` to add this processor to your recipes.

See the [`firefox_AA.cfg.template`](https://github.com/autopkg/scriptingosx-recipes/blob/master/FirefoxPrefs/firefox_AA.cfg.template) file for an example.

## Post Processors

These processors are designed to run as post-processors. You can add them to your autopkg workflow like this:

```
$ autopkg run Recipe1.pkg Recipe2.pkg --post com.scriptingosx.processors/Notification
```

Or with [a plist format recipe list](https://github.com/autopkg/autopkg/wiki/Running-Multiple-Recipes).


### Notification

This will show a user notification when the processor detects a new download or that a new package was built. May act strangely when run with no user logged in.

Use `com.scriptingosx.processors/Notification` to add this processor as a post processor.

### RevealInFinder

This processor will open a new Finder window and select the new file. It will either use a newly archived file, a newly built package or a new download (in that order). May not work when no user is logged in.

Use `com.scriptingosx.processors/RevealInFinder` to add this processor as a post processor.


### Archive

When this processor detects a new download or that a new package was built it will copy it to a the directory given in `archive_path`. `archive_path` can be on a file server, but it is your responsibility that the share is mounted and available at that path.

Even when you don't copy to a server this can be useful to create an archive of packages outside of the ~/Library/AutoPkg/Caches folder so you can delete cache folders to remove problems with downloads or package building without losing your 'history' of packages.

Input Variables:

- `archive_path`: (required) path for the package/download item archive
- `archive_subdir`: (optional) subdirectory in the `archive_path` folder (e.g. `%NAME%`)

Output Variables:

- `archived_file_path`: Path to the archived file.
- `archive_summary_result`: Used to display summary at the end of an `autopkg run`

Use `com.scriptingosx.processors/Archive` to add this processor as a post processor.

To provide the required `archive_path` variable you can use the `-k/--key` argument or [a plist format recipe list](https://github.com/autopkg/autopkg/wiki/Running-Multiple-Recipes).

```
$ autopkg run Recipe1.pkg Recipe2.pkg --post com.scriptingosx.processors/Archive -k archive_path=~/Library/AutoPkg/Archive/ -k archive_subdir=%NAME%
```

