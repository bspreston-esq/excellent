# triumphant

Whoa! This is the most excellent little program in the whole Western
Civilization. Fire up `triumphant` and it doles out a righteous quote from
the dudes themselves — Bill and Ted, no less!

## Party on, man: usage

Grab a bodacious quote, dude:

    triumphant

Strange things are afoot at the Circle-K? Play it safe, dudes:

    triumphant --careful

Things went totally heinous? Express yourself:

    triumphant --bogus

Which collections are available, dude?

    triumphant --list-collections

Want a quote from another batch of dudes, like Austin Powers (yeah, baby!)?

    triumphant --collection austin-powers

Need a hand, man? The program's got your back:

    triumphant --help

And if you toss it some bogus, non-triumphant argument, it'll school you with
a usage message. Most impressive.

## Excellent quality, dude

Be excellent to each other:

- Random quote from the righteous set when you run it plain.
- `--careful` picks from the cautious set.
- `--bogus` picks from the most non-triumphant set.
- `--collection NAME` / `-C NAME` picks which collection to quote from
  (`default` is Bill and Ted; `austin-powers` ships too, baby).
- `--list-collections` / `-L` lists the available collections.
- `--help` shows the usage, and invalid flags get the boot (exit code and
  all, man).

## Collections, dude

Each collection is a directory with three files — `standard`, `careful` and
`bogus` — plus an optional `description` file. The quote files are plain
text, easy to read and easy to modify: each quote is separated by a line of
two or more dashes (`--`), `#` lines and blank lines are ignored, and quotes
can span multiple lines. For example:

    Be excellent to each other.
    --
    Party on, dudes!

Want your own collection, dude? Just drop a directory like
`/var/lib/triumphant/my-dudes/` (with those three files) and it shows up in
`--list-collections` right away. On RPM installs the data files live in
`/var/lib/triumphant/<collection>/` and are marked as config files, so
package upgrades will leave your edits alone (new versions arrive as
`.rpmnew` files). On pip installs the collections ship inside the package
itself, and `/var/lib/triumphant/<collection>` still takes the lead if you
create one there.

## Party on from PyPI, dude

Whoa, the whole quote machine is on PyPI now as **`triumphant`** — most
triumphant, dudes:

    pip install triumphant

Then call up a righteous quote from anywhere, dude:

    triumphant             # a righteous quote
    triumphant --careful   # strange things are afoot at the Circle-K
    triumphant --bogus     # things are most heinously failing

## RPM party, dudes

The same righteous quotes ride as an RPM, built for Fedora by COPR. Enable
the repo and install, man:

    dnf copr enable bspreston-esq/triumphant
    dnf install triumphant

Then `triumphant` is a bodacious command right in `/usr/bin` — most
triumphant, no pip required. Party on! Extra collections (like the righteous
Austin Powers set) ride in a separate package:

    dnf install triumphant-collections

## Development, dudes

The main branch is a most protected zone — no direct commits, no way, man.
All changes roll in via pull requests, and CI (see `.github/workflows/ci.yml`)
has got to come up most triumphant before anything merges into main.

Want to contribute? Party on, but be excellent to each other — and write any
README updates in this same Bill and Ted style. Most outstanding!

## License

See [LICENSE](LICENSE).
