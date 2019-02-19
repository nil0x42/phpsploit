# Change Log

## [v3.0](https://github.com/nil0x42/phpsploit/tree/v3.0) (2019-01-06)

[Full Changelog](https://github.com/nil0x42/phpsploit/compare/2.2.0b...v3.0)

**Implemented enhancements:**

-   Add verbosity on tunnel handler [#18](https://github.com/nil0x42/phpsploit/issues/18)
-   Add retrocompatibility for phpsploit v1 sessions (legacy version) [#13](https://github.com/nil0x42/phpsploit/issues/13)
-   Improve session changes mechanism. [#12](https://github.com/nil0x42/phpsploit/issues/12)
-   `lrun cd \<DIRECTORY\>` does not changes $PWD. [#10](https://github.com/nil0x42/phpsploit/issues/10)
-   Add a '--browser' option to `phpinfo` plugin for html display. [#5](https://github.com/nil0x42/phpsploit/issues/5)
-   Create a `stat` plugin (which replaces old fileinfo) [#4](https://github.com/nil0x42/phpsploit/issues/4)
-   Proposal: Add workaround for custom php `error\_reporting` level [#3](https://github.com/nil0x42/phpsploit/issues/3)

**Fixed bugs:**

-   command: `phpinfo --browse`: BUG [#34](https://github.com/nil0x42/phpsploit/issues/34)
-   Regression on Phpcode() datatype after Code() wrapper implementation [#16](https://github.com/nil0x42/phpsploit/issues/16)
-   `set \<SETTING\> +` dont checks new added value, resulting to unexpected bugs. [#15](https://github.com/nil0x42/phpsploit/issues/15)
-   Dynamic HTTP\_\* header settings cannot be unset. [#11](https://github.com/nil0x42/phpsploit/issues/11)
-   `lrun cd \\<DIRECTORY\\>` does not changes $PWD. [#10](https://github.com/nil0x42/phpsploit/issues/10)
-   Unlike unix's `ls` command, the `ls` plugin leaves at first invalid path [#1](https://github.com/nil0x42/phpsploit/issues/1)

**Closed issues:**

-   Unknown Command [#52](https://github.com/nil0x42/phpsploit/issues/52)
-   Changes in data/config/config not loaded [#49](https://github.com/nil0x42/phpsploit/issues/49)
-   Upload error [#48](https://github.com/nil0x42/phpsploit/issues/48)
-   post parameter for target [#47](https://github.com/nil0x42/phpsploit/issues/47)
-   Key Error: ADDR [#36](https://github.com/nil0x42/phpsploit/issues/36)
-   Bad return value for `exploit --get-backdoor` [#35](https://github.com/nil0x42/phpsploit/issues/35)
-   'corectl reload-plugins' [#30](https://github.com/nil0x42/phpsploit/issues/30)
-   interface: autocompletion bug with commands containing '-' char [#28](https://github.com/nil0x42/phpsploit/issues/28)
-   setting an https url auto sets port to 80 instead of 443 as normally wanted [#26](https://github.com/nil0x42/phpsploit/issues/26)
-   `exploit` command alters ENV without asking [#24](https://github.com/nil0x42/phpsploit/issues/24)
-   \[PHP 5.2.17 / Microsoft-IIS 8.0] HTTP headers with '\_' not converted into $\_SERVER vars [#23](https://github.com/nil0x42/phpsploit/issues/23)
-   Python help [#22](https://github.com/nil0x42/phpsploit/issues/22)
-   Architecture issue: Organising decorators. [#20](https://github.com/nil0x42/phpsploit/issues/20)
-   No deterministic component display order on `session` command. [#17](https://github.com/nil0x42/phpsploit/issues/17)
-   History size issue (very slow loop) [#14](https://github.com/nil0x42/phpsploit/issues/14)
-   Add support for http_proxy like env vars on unix platforms [#6](https://github.com/nil0x42/phpsploit/issues/6)

**Merged pull requests:**

-   spelling fixes [#51](https://github.com/nil0x42/phpsploit/pull/51) ([paralax](https://github.com/paralax))
-   fix a bunch of spelling and grammar errors [#50](https://github.com/nil0x42/phpsploit/pull/50) ([paralax](https://github.com/paralax))
-   fix machinery import [#46](https://github.com/nil0x42/phpsploit/pull/46) ([paralax](https://github.com/paralax))
-   Plugin ldap [#40](https://github.com/nil0x42/phpsploit/pull/40) ([shiney-wh](https://github.com/shiney-wh))
-   new plugin: scan [#38](https://github.com/nil0x42/phpsploit/pull/38) ([shiney-wh](https://github.com/shiney-wh))
-   Fix some issues  [#33](https://github.com/nil0x42/phpsploit/pull/33) ([yurilaaziz](https://github.com/yurilaaziz))
-   Deps cleanout [#25](https://github.com/nil0x42/phpsploit/pull/25) ([nil0x42](https://github.com/nil0x42))

## [2.2.0b](https://github.com/nil0x42/phpsploit/tree/2.2.0b) (2014-08-09)

[Full Changelog](https://github.com/nil0x42/phpsploit/compare/2.1.4...2.2.0b)

## [2.1.4](https://github.com/nil0x42/phpsploit/tree/2.1.4) (2013-04-07)

[Full Changelog](https://github.com/nil0x42/phpsploit/compare/2.1.3...2.1.4)

## [2.1.3](https://github.com/nil0x42/phpsploit/tree/2.1.3) (2013-02-20)

[Full Changelog](https://github.com/nil0x42/phpsploit/compare/2.1.2...2.1.3)

## [2.1.2](https://github.com/nil0x42/phpsploit/tree/2.1.2) (2012-08-12)

[Full Changelog](https://github.com/nil0x42/phpsploit/compare/2.1.1...2.1.2)

## [2.1.1](https://github.com/nil0x42/phpsploit/tree/2.1.1) (2012-08-11)

[Full Changelog](https://github.com/nil0x42/phpsploit/compare/2.1.0...2.1.1)

## [2.1.0](https://github.com/nil0x42/phpsploit/tree/2.1.0) (2012-08-11)

[Full Changelog](https://github.com/nil0x42/phpsploit/compare/2.0.2...2.1.0)

## [2.0.2](https://github.com/nil0x42/phpsploit/tree/2.0.2) (2012-07-27)

\* _This Change Log was automatically generated by [github_changelog_generator](https://github.com/skywinder/Github-Changelog-Generator)_
