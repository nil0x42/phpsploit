# Change Log

## [v3.2](https://github.com/nil0x42/phpsploit/tree/v3.2) (2020-10-16)

[Full Changelog](https://github.com/nil0x42/phpsploit/compare/v3.1...v3.2)

**Implemented enhancements:**

-   integrate `bannergrab`, `cloudcredgrab` & `proclist` plugins by @paralax [#151](https://github.com/nil0x42/phpsploit/issues/151)
-   unused session attribute: `session.Cache` [#102](https://github.com/nil0x42/phpsploit/issues/102)
-   session.Env.PORT is useless [#71](https://github.com/nil0x42/phpsploit/issues/71)

**Merged pull requests:**

-   Wip [#156](https://github.com/nil0x42/phpsploit/pull/156) ([nil0x42](https://github.com/nil0x42))
-   Wip [#155](https://github.com/nil0x42/phpsploit/pull/155) ([nil0x42](https://github.com/nil0x42))
-   Wip [#153](https://github.com/nil0x42/phpsploit/pull/153) ([nil0x42](https://github.com/nil0x42))
-   add three new plugins - proclist, cloud creds, and banner grabs [#152](https://github.com/nil0x42/phpsploit/pull/152) ([paralax](https://github.com/paralax))
-   Wip [#150](https://github.com/nil0x42/phpsploit/pull/150) ([nil0x42](https://github.com/nil0x42))
-   Create Dependabot config file [#149](https://github.com/nil0x42/phpsploit/pull/149) ([dependabot-preview\[bot\]](https://github.com/apps/dependabot-preview))
-   \[requires.io] dependency update on master branch [#148](https://github.com/nil0x42/phpsploit/pull/148) ([nil0x42](https://github.com/nil0x42))
-   \[requires.io] dependency update on master branch [#147](https://github.com/nil0x42/phpsploit/pull/147) ([nil0x42](https://github.com/nil0x42))

## [v3.1](https://github.com/nil0x42/phpsploit/tree/v3.1) (2020-09-10)

[Full Changelog](https://github.com/nil0x42/phpsploit/compare/v3.0...v3.1)

**Implemented enhancements:**

-   Make warning message explicit when running plugin in non-connected mode  [#74](https://github.com/nil0x42/phpsploit/issues/74)
-   Show stack trace when VERBOSITY is True [#73](https://github.com/nil0x42/phpsploit/issues/73)
-   get help for `CMD` when calling `help CMD ARG` [#70](https://github.com/nil0x42/phpsploit/issues/70)
-   unexpected infinite autocompletion [#68](https://github.com/nil0x42/phpsploit/issues/68)
-   `help set \<VAR\>`: display buffer type description [#67](https://github.com/nil0x42/phpsploit/issues/67)
-   `set` should inform user that `help set \<VAR\>` is available [#62](https://github.com/nil0x42/phpsploit/issues/62)
-   `alias \<VAR\> None` misses verbosity [#59](https://github.com/nil0x42/phpsploit/issues/59)
-   Missing `help set \<SETTING\>` autocompletion [#56](https://github.com/nil0x42/phpsploit/issues/56)
-   env: Confusing error message before `exploited` context [#53](https://github.com/nil0x42/phpsploit/issues/53)
-   `./deps/` folder is archaic [#41](https://github.com/nil0x42/phpsploit/issues/41)

**Fixed bugs:**

-   phpsploit is not working properly [#128](https://github.com/nil0x42/phpsploit/issues/128)
-   `suidroot` plugin makes invalid assumptions [#105](https://github.com/nil0x42/phpsploit/issues/105)
-   crash: IndexError: list index out of range [#101](https://github.com/nil0x42/phpsploit/issues/101)
-   `lrun` command always returns 0 [#83](https://github.com/nil0x42/phpsploit/issues/83)
-   core.tunnel.exceptions.ResponseError: Php runtime error [#81](https://github.com/nil0x42/phpsploit/issues/81)
-   core: read non-tty STDIN line-by-line [#75](https://github.com/nil0x42/phpsploit/issues/75)
-   term colors: buggy message display [#72](https://github.com/nil0x42/phpsploit/issues/72)
-   `corectl display-http-requests`: invalid log on POST method [#65](https://github.com/nil0x42/phpsploit/issues/65)
-   `alias` can override existing command [#60](https://github.com/nil0x42/phpsploit/issues/60)
-   `isolate\_readline\_context\(\)` don't isolates readline history [#54](https://github.com/nil0x42/phpsploit/issues/54)

**Closed issues:**

-   Scripting support [#138](https://github.com/nil0x42/phpsploit/issues/138)
-   add jonas lejon as contributor for his blog post [#137](https://github.com/nil0x42/phpsploit/issues/137)
-   `corectl display-http-requests` not working when PROXY is set [#135](https://github.com/nil0x42/phpsploit/issues/135)
-   I'm sure i set the  backdoor file,but i can't get windows shell again [#120](https://github.com/nil0x42/phpsploit/issues/120)
-   a window shell trate mysql data [#119](https://github.com/nil0x42/phpsploit/issues/119)
-   Doubt about the socks proxy5  [#114](https://github.com/nil0x42/phpsploit/issues/114)
-   INSTALL.md should have install instructions [#106](https://github.com/nil0x42/phpsploit/issues/106)
-   Add contributors list on README [#88](https://github.com/nil0x42/phpsploit/issues/88)
-   `help \<PLUGIN\>` lacks plugin informations [#85](https://github.com/nil0x42/phpsploit/issues/85)
-   ux: show `missing dependency` warnings at start [#80](https://github.com/nil0x42/phpsploit/issues/80)

**Merged pull requests:**

-   Wip [#146](https://github.com/nil0x42/phpsploit/pull/146) ([nil0x42](https://github.com/nil0x42))
-   docs/README: add `awesome` badge [#145](https://github.com/nil0x42/phpsploit/pull/145) ([nil0x42](https://github.com/nil0x42))
-   WIP [#144](https://github.com/nil0x42/phpsploit/pull/144) ([nil0x42](https://github.com/nil0x42))
-   Wip [#143](https://github.com/nil0x42/phpsploit/pull/143) ([nil0x42](https://github.com/nil0x42))
-   \[ImgBot] Optimize images [#142](https://github.com/nil0x42/phpsploit/pull/142) ([imgbot\[bot\]](https://github.com/apps/imgbot))
-   Wip [#141](https://github.com/nil0x42/phpsploit/pull/141) ([nil0x42](https://github.com/nil0x42))
-   docs: add jonaslejon as a contributor [#139](https://github.com/nil0x42/phpsploit/pull/139) ([allcontributors\[bot\]](https://github.com/apps/allcontributors))
-   Wip [#136](https://github.com/nil0x42/phpsploit/pull/136) ([nil0x42](https://github.com/nil0x42))
-   \[requires.io] dependency update on master branch [#134](https://github.com/nil0x42/phpsploit/pull/134) ([nil0x42](https://github.com/nil0x42))
-   \[requires.io] dependency update on master branch [#133](https://github.com/nil0x42/phpsploit/pull/133) ([nil0x42](https://github.com/nil0x42))
-   \[requires.io] dependency update on master branch [#131](https://github.com/nil0x42/phpsploit/pull/131) ([nil0x42](https://github.com/nil0x42))
-   \[requires.io] dependency update on master branch [#130](https://github.com/nil0x42/phpsploit/pull/130) ([nil0x42](https://github.com/nil0x42))
-   set/BROWSER: fix issue #128 [#129](https://github.com/nil0x42/phpsploit/pull/129) ([nil0x42](https://github.com/nil0x42))
-   \[ImgBot] Optimize images [#127](https://github.com/nil0x42/phpsploit/pull/127) ([imgbot\[bot\]](https://github.com/apps/imgbot))
-   \[requires.io] dependency update on master branch [#126](https://github.com/nil0x42/phpsploit/pull/126) ([nil0x42](https://github.com/nil0x42))
-   \[requires.io] dependency update on master branch [#125](https://github.com/nil0x42/phpsploit/pull/125) ([nil0x42](https://github.com/nil0x42))
-   \[requires.io] dependency update on master branch [#124](https://github.com/nil0x42/phpsploit/pull/124) ([nil0x42](https://github.com/nil0x42))
-   plugin/mysql: add PHP 7 compatibility [#123](https://github.com/nil0x42/phpsploit/pull/123) ([nil0x42](https://github.com/nil0x42))
-   \[requires.io] dependency update on master branch [#122](https://github.com/nil0x42/phpsploit/pull/122) ([nil0x42](https://github.com/nil0x42))
-   \[requires.io] dependency update on master branch [#121](https://github.com/nil0x42/phpsploit/pull/121) ([nil0x42](https://github.com/nil0x42))
-   \[requires.io] dependency update on master branch [#118](https://github.com/nil0x42/phpsploit/pull/118) ([nil0x42](https://github.com/nil0x42))
-   \[requires.io] dependency update on master branch [#117](https://github.com/nil0x42/phpsploit/pull/117) ([nil0x42](https://github.com/nil0x42))
-   \[requires.io] dependency update on master branch [#116](https://github.com/nil0x42/phpsploit/pull/116) ([nil0x42](https://github.com/nil0x42))
-   \[requires.io] dependency update on master branch [#115](https://github.com/nil0x42/phpsploit/pull/115) ([nil0x42](https://github.com/nil0x42))
-   ci: fix bug on `alias` test [#113](https://github.com/nil0x42/phpsploit/pull/113) ([nil0x42](https://github.com/nil0x42))
-   docs: update README [#112](https://github.com/nil0x42/phpsploit/pull/112) ([nil0x42](https://github.com/nil0x42))
-   Wip [#111](https://github.com/nil0x42/phpsploit/pull/111) ([nil0x42](https://github.com/nil0x42))
-   docs: Add 'Quick Start' instructions in INSTALL.md [#110](https://github.com/nil0x42/phpsploit/pull/110) ([nil0x42](https://github.com/nil0x42))
-   \[requires.io] dependency update on master branch [#108](https://github.com/nil0x42/phpsploit/pull/108) ([nil0x42](https://github.com/nil0x42))
-   core: add '.' to WORD_TOKEN accepted chars [#104](https://github.com/nil0x42/phpsploit/pull/104) ([nil0x42](https://github.com/nil0x42))
-   Wip [#103](https://github.com/nil0x42/phpsploit/pull/103) ([nil0x42](https://github.com/nil0x42))
-   CI: critical bugfix: coverage reports were ignored [#100](https://github.com/nil0x42/phpsploit/pull/100) ([nil0x42](https://github.com/nil0x42))
-   Wip [#99](https://github.com/nil0x42/phpsploit/pull/99) ([nil0x42](https://github.com/nil0x42))
-   docs: add rohantarai as a contributor [#98](https://github.com/nil0x42/phpsploit/pull/98) ([allcontributors\[bot\]](https://github.com/apps/allcontributors))
-   docs: add tristandostaler as a contributor [#97](https://github.com/nil0x42/phpsploit/pull/97) ([allcontributors\[bot\]](https://github.com/apps/allcontributors))
-   docs: add sohelzerdoumi as a contributor [#96](https://github.com/nil0x42/phpsploit/pull/96) ([allcontributors\[bot\]](https://github.com/apps/allcontributors))
-   docs: add sujit as a contributor [#94](https://github.com/nil0x42/phpsploit/pull/94) ([allcontributors\[bot\]](https://github.com/apps/allcontributors))
-   docs: add paralax as a contributor [#93](https://github.com/nil0x42/phpsploit/pull/93) ([allcontributors\[bot\]](https://github.com/apps/allcontributors))
-   docs: add yurilaaziz as a contributor [#92](https://github.com/nil0x42/phpsploit/pull/92) ([allcontributors\[bot\]](https://github.com/apps/allcontributors))
-   docs: add wapiflapi as a contributor [#91](https://github.com/nil0x42/phpsploit/pull/91) ([allcontributors\[bot\]](https://github.com/apps/allcontributors))
-   docs: add shiney-wh as a contributor [#90](https://github.com/nil0x42/phpsploit/pull/90) ([allcontributors\[bot\]](https://github.com/apps/allcontributors))
-   docs: add nil0x42 as a contributor [#89](https://github.com/nil0x42/phpsploit/pull/89) ([allcontributors\[bot\]](https://github.com/apps/allcontributors))
-   Wip [#87](https://github.com/nil0x42/phpsploit/pull/87) ([nil0x42](https://github.com/nil0x42))
-   Initial Update [#86](https://github.com/nil0x42/phpsploit/pull/86) ([pyup-bot](https://github.com/pyup-bot))
-   Wip [#84](https://github.com/nil0x42/phpsploit/pull/84) ([nil0x42](https://github.com/nil0x42))
-   Wip [#82](https://github.com/nil0x42/phpsploit/pull/82) ([nil0x42](https://github.com/nil0x42))
-   WIP: improve CI workflow & add test for command-line options [#79](https://github.com/nil0x42/phpsploit/pull/79) ([nil0x42](https://github.com/nil0x42))
-   CI Workflow [#77](https://github.com/nil0x42/phpsploit/pull/77) ([nil0x42](https://github.com/nil0x42))

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

-   Changes in data/config/config not loaded [#49](https://github.com/nil0x42/phpsploit/issues/49)
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
