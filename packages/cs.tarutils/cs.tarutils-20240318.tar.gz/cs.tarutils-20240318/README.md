Assorted tar related things, including a fast tar-based copy.

*Latest release 20240318*:
Initial PyPI release with nice traced_cpdir() function.

My most heavily used use for this is my `cpdir` script which
does a high performance directory copy by piping 2 `tar`s
together.
It runs this:

    from cs.tarutils import traced_cpdir
    sys.exit(traced_cpdir(*sys.argv[1:]))

## Function `tar(*srcpaths: List[str], chdirpath='.', output, tar_exe='tar', bcount=2048)`

Tar up the contents of `srcpaths` to `output`.
Return the `Popen` object for the `tar` command.

Parameters:
* `srcpaths`: source filesystem paths
* `chdirpath`: optional directory to which to `chdir` before accessing `srcpaths`
* `tar_exe`: optional `tar` executable, default from `TAR_EXE`: `tar`
* `bcount`: blocking factor in 512 byte unites,
  default from `DEFAULT_BCOUNT`: `2048`

## Function `traced_cpdir(srcdirpath, dstdirpath, *, label=None, tar_exe='tar', bcount=2048, upd)`

Copy a directory to a new place using piped tars with progress reporting.
Return `0` if both tars succeed, nonzero otherwise.

Parameters:
* `srcdirpath`: the source directory filesystem path
* `dstdirpath`: the destination directory filesystem path,
  which must not already exist
* `label`: optional label for the progress bar
* `tar_exe`: optional `tar` executable, default from `TAR_EXE`: `tar`
* `bcount`: blocking factor in 512 byte unites,
  default from `DEFAULT_BCOUNT`: `2048`

## Function `traced_untar(tarfd, *, chdirpath='.', label=None, tar_exe='tar', bcount=2048, total=None, _stat_fd=False, upd)`

Read tar data from `tarfd` and extract.
Return the `tar` exit code.

Parameters:
* `tarfd`: the source tar data,
  suitable for `subprocess.Popen`'s `stdin` parameter
* `chdirpath`: optional directory to which to `chdir` before accessing `srcpaths`
* `label`: optional label for the progress bar
* `tar_exe`: optional `tar` executable, default from `TAR_EXE`: `tar`
* `bcount`: blocking factor in 512 byte unites,
  default from `DEFAULT_BCOUNT`: `2048`

# Release Log



*Release 20240318*:
Initial PyPI release with nice traced_cpdir() function.
