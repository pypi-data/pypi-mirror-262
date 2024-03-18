# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.2] - 2023-03-18

### Added

- `pyCFS.data` package
  - code, tests and doc
- Sensor array result support 
  - Because CFS currently does not write SA results into the `hdf` file

### Changed

- Extended dependencies to accommodate `pyCFS.data` package

## [0.0.1] - 2023-03-12

### Added 

- Old `pycfs` package code (refactored)
- CI pipeline for automated testing 
- GitLab pages for documentation
  
### Fixed 

- Parallelization when meshing
- Type hints

### Removed 

- History results are no longer supported 
  - These are now to be written into the `hdf` file
- Sensor array results are the only exception 
  - When CFS can directly write these to the `hdf` file this package will change accordingly 
  - Users should not see much difference in behavior