# Firefox Prefs recipes

These recipes will insert a Firefox configuration file into the Firefox bundle [as described here](https://managingosx.wordpress.com/2008/08/18/firefox-default-settings/).

Note: this is a very basic way of setting Firefox preferences. It worked great for my use case (supressing update dialogs and setting home page url in student labs). If you need more control over Firefox behavior in your packaging process, look at [CCK](https://github.com/mkaply/cck2wizard/releases/tag/2.2.3) and use [Greg's FirefoxAutoconfig recipes](https://github.com/autopkg/gregneagle-recipes/blob/master/Mozilla/FirefoxAutoconfig.pkg.recipe).

The `FirefoxPrefs.pkg` recipe uses the [`FileTemplate`](https://github.com/autopkg/scriptingosx-recipes/tree/master/SharedProcessors) shared processor to load the `firefox_AA.cfg.template` and fill in the proper values. You can modify the template file to add your own settings. The recipe will also put the `local-settings.js` and `override.ini` in the proper locations and build installer package file with everything.

If you put your copies of any of the three resource files (`firefox_AA.cfg.template`, `local-settings.js` or `override.ini`) in the same folder as your recipe override, those copies will be used instead.