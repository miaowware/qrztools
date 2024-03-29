# Changelog for qrztools
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [Unreleased]


## [1.2.0] - 2021-09-27
### Deprecated
- This library. Use `callsignlookuptools` instead.


## [1.1.1] - 2021-03-16
### Fixed
- Issue allowing for possible XSS in queries


## [1.1.0] - 2021-03-15
### Added
- Support for getting trustee info from `get_callsign()` queries
- Support for `all` as an argument for `get_dxcc()`
### Changed
- `QrzCallsignData.eqsl`, `QrzCallsignData.mail_qsl`, and `QrzCallsignData.lotw_qsl` now is `None` if the value is unknown
- The dependency `rich` to be be installed via the extra `cli`, instead of being installed by default
### Fixed
- An error when getting some callsigns because of invalid dates.
- An issue where the documentation would not render properly.


## [1.0.0] - 2021-03-15
### Added
- Synchronous and asynchronous interfaces to QRZ


[Unreleased]: https://github.com/miaowware/qrztools/compare/1.2.0...HEAD
[1.2.0]: https://github.com/miaowware/qrztools/releases/tag/1.2.0
[1.1.1]: https://github.com/miaowware/qrztools/releases/tag/1.1.1
[1.1.0]: https://github.com/miaowware/qrztools/releases/tag/1.1.0
[1.0.0]: https://github.com/miaowware/qrztools/releases/tag/1.0.0
