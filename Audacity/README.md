# Note on `Audacity.pkg` recipe

The `Audacity.download` [was removed because of a TOS violation](https://github.com/autopkg/scriptingosx-recipes/issues/21). My `Audacity.pkg` recipe used that as a parent. There are actually several recipes which use `Audacity.pkg` as their parent.

I have changed `Audactiy.pkg` to use the `--pkg` option. When you download the Audacity disk image (dmg) file [from the official website](http://www.audacityteam.org/download/mac/) manually you can then run

```
autopkg run Audacity.pkg --pkg ~/Downloads/audacity-macosx-ub-2.1.2.dmg
```

Or any of the Audacity child recipes with the `--pkg` parameter.

## Note on the `Audacity.jss` recipe

Since my `Audacity.jss` is mostly redundant with the `Audacity.jss` in the [jss-recipes repository](https://github.com/autopkg/jss-recipes/blob/master/Audacity/Audacity.jss.recipe) I have turned it into a stub that uses [jss-recipes/Audacity/Audacity.jss](https://github.com/autopkg/jss-recipes/blob/master/Audacity/Audacity.jss.recipe) as a parent. You will have to add the `jss-recipes` repository for it to work. Going forward you want to directly use the jss-recipes `Audacity.jss` recipe. (change the `ParentRecipe` key in your Override to `com.github.jss-recipes.jss.Audacity`)
