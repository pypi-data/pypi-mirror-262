A command and utility functions for making listings of file content hashcodes
and manipulating directory trees based on such a hash index.

*Latest release 20240316*:
Fixed release upload artifacts.

## Function `dir_filepaths(dirpath: str, *, fstags: cs.fstags.FSTags)`

Generator yielding the filesystem paths of the files in `dirpath`.

## Function `dir_remap(srcdirpath: str, fspaths_by_hashcode: Mapping[cs.hashutils.BaseHashCode, List[str]], *, hashname: str)`

Generator yielding `(srcpath,[remapped_paths])` 2-tuples
based on the hashcodes keying `rfspaths_by_hashcode`.

## Function `file_checksum(fspath: str, hashname: str = 'sha256', *, fstags: cs.fstags.FSTags) -> Optional[cs.hashutils.BaseHashCode]`

Return the hashcode for the contents of the file at `fspath`.
Warn and return `None` on `OSError`.

## Function `get_fstags_hashcode(fspath: str, hashname: str, fstags: cs.fstags.FSTags) -> Tuple[Optional[cs.hashutils.BaseHashCode], Optional[os.stat_result]]`

Obtain the hashcode cached in the fstags if still valid.
Return a 2-tuple of `(hashcode,stat_result)`
where `hashcode` is a `BaseHashCode` subclass instance is valid
or `None` if missing or no longer valid
and `stat_result` is the current `os.stat` result for `fspath`.

## Function `hashindex(fspath: Union[str, io.TextIOBase, Tuple[Optional[str], str]], *, hashname: str, **kw) -> Iterable[Tuple[Optional[cs.hashutils.BaseHashCode], Optional[str]]]`

Generator yielding `(hashcode,filepath)` 2-tuples
for the files in `fspath`, which may be a file or directory path.
Note that it yields `(None,filepath)` for files which cannot be accessed.

## Class `HashIndexCommand(cs.cmdutils.BaseCommand)`

A tool to generate indices of file content hashcodes
and to link or otherwise rearrange files to destinations based
on their hashcode.

Command line usage:

    Usage: hashindex subcommand...
        Generate or process file content hash listings.
      Subcommands:
        comm {-1|-2|-3} {path1|-} {path2|-}
          Compare the filepaths in path1 and path2 by content.
          -1            List hashes and paths only present in path1.
          -2            List hashes and paths only present in path2.
          -3            List hashes and paths present in path1 and path2.
          -e ssh_exe    Specify the ssh executable.
          -h hashname   Specify the file content hash algorithm name.
          -H hashindex_exe
                        Specify the remote hashindex executable.
        help [-l] [subcommand-names...]
          Print help for subcommands.
          This outputs the full help for the named subcommands,
          or the short help for all subcommands if no names are specified.
          -l  Long help even if no subcommand-names provided.
        ls [options...] [host:]path...
          Walk filesystem paths and emit a listing.
          Options:
          -e ssh_exe    Specify the ssh executable.
          -h hashname   Specify the file content hash algorithm name.
          -H hashindex_exe
                        Specify the remote hashindex executable.
          -r            Emit relative paths in the listing.
                        This requires each path to be a directory.
        rearrange [options...] {[[user@]host:]refdir|-} [[user@]rhost:]targetdir [dstdir]
          Rearrange files from targetdir into dstdir based on their positions in refdir.
          Options:
            -e ssh_exe  Specify the ssh executable.
            -h hashname Specify the file content hash algorithm name.
            -H hashindex_exe
                        Specify the remote hashindex executable.
            --mv        Move mode.
            -n          No action, dry run.
            -s          Symlink mode.
          Other arguments:
            refdir      The reference directory, which may be local or remote
                        or "-" indicating that a hash index will be read from
                        standard input.
            targetdir   The directory containing the files to be rearranged,
                        which may be local or remote.
            dstdir      Optional destination directory for the rearranged files.
                        Default is the targetdir.
                        It is taken to be on the same host as targetdir.
        shell
          Run a command prompt via cmd.Cmd using this command's subcommands.

*`HashIndexCommand.Options`*

*Method `HashIndexCommand.cmd_comm(self, argv)`*:
Usage: {cmd} {{-1|-2|-3}} {{path1|-}} {{path2|-}}
Compare the filepaths in path1 and path2 by content.
-1            List hashes and paths only present in path1.
-2            List hashes and paths only present in path2.
-3            List hashes and paths present in path1 and path2.
-e ssh_exe    Specify the ssh executable.
-h hashname   Specify the file content hash algorithm name.
-H hashindex_exe
              Specify the remote hashindex executable.

*Method `HashIndexCommand.cmd_ls(self, argv)`*:
Usage: {cmd} [options...] [host:]path...
Walk filesystem paths and emit a listing.
Options:
-e ssh_exe    Specify the ssh executable.
-h hashname   Specify the file content hash algorithm name.
-H hashindex_exe
              Specify the remote hashindex executable.
-r            Emit relative paths in the listing.
              This requires each path to be a directory.

*Method `HashIndexCommand.cmd_rearrange(self, argv)`*:
Usage: {cmd} [options...] {{[[user@]host:]refdir|-}} [[user@]rhost:]targetdir [dstdir]
Rearrange files from targetdir into dstdir based on their positions in refdir.
Options:
  -e ssh_exe  Specify the ssh executable.
  -h hashname Specify the file content hash algorithm name.
  -H hashindex_exe
              Specify the remote hashindex executable.
  --mv        Move mode.
  -n          No action, dry run.
  -s          Symlink mode.
Other arguments:
  refdir      The reference directory, which may be local or remote
              or "-" indicating that a hash index will be read from
              standard input.
  targetdir   The directory containing the files to be rearranged,
              which may be local or remote.
  dstdir      Optional destination directory for the rearranged files.
              Default is the targetdir.
              It is taken to be on the same host as targetdir.

## Function `localpath(fspath: str) -> str`

Return a filesystem path modified so that it connot be
misinterpreted as a remote path such as `user@host:path`.

If `fspath` contains no colon (`:`) or is an absolute path
or starts with `./` then it is returned unchanged.
Otherwise a leading `./` is prepended.

## Function `main(argv=None)`

Commandline implementation.

## Function `merge(srcpath: str, dstpath: str, *, opname=None, hashname: str, move_mode: bool = False, symlink_mode=False, doit=False, quiet=False, fstags: cs.fstags.FSTags)`

Merge `srcpath` to `dstpath`.

If `dstpath` does not exist, move/link/symlink `srcpath` to `dstpath`.
Otherwise checksum their contents and raise `FileExistsError` if they differ.

## Function `paths_remap(srcpaths: Iterable[str], fspaths_by_hashcode: Mapping[cs.hashutils.BaseHashCode, List[str]], *, hashname: str)`

Generator yielding `(srcpath,fspaths)` 2-tuples.

## Function `read_hashindex(f, start=1, *, hashname: str) -> Iterable[Tuple[Optional[cs.hashutils.BaseHashCode], Optional[str]]]`

A generator which reads line from the file `f`
and yields `(hashcode,fspath)` 2-tuples for each line.
If there are parse errors the `hashcode` or `fspath` may be `None`.

## Function `read_remote_hashindex(rhost: str, rdirpath: str, *, hashname: str, ssh_exe=None, hashindex_exe=None, check=True) -> Iterable[Tuple[Optional[cs.hashutils.BaseHashCode], Optional[str]]]`

A generator which reads a hashindex of a remote directory,
This runs: `hashindex ls -h hashname -r rdirpath` on the remote host.
It yields `(hashcode,fspath)` 2-tuples.

Parameters:
* `rhost`: the remote host, or `user@host`
* `rdirpath`: the remote directory path
* `hashname`: the file content hash algorithm name
* `ssh_exe`: the `ssh` executable,
  default `SSH_EXE_DEFAULT`: `'ssh'`
* `hashindex_exe`: the remote `hashindex` executable,
  default `HASHINDEX_EXE_DEFAULT`: `'hashindex'`
* `check`: whether to check that the remote command has a `0` return code,
  default `True`

## Function `rearrange(srcdirpath: str, rfspaths_by_hashcode, dstdirpath=None, *, hashname: str, move_mode: bool = False, symlink_mode=False, doit: bool, quiet: bool = False, fstags: cs.fstags.FSTags, runstate: cs.resources.RunState)`

Rearrange the files in `dirpath` according to the
hashcode->[relpaths] `fspaths_by_hashcode`.

Parameters:
* `srcdirpath`: the directory whose files are to be rearranged
* `rfspaths_by_hashcode`: a mapping of hashcode to relative
  pathname to which the original file is to be moved
* `dstdirpath`: optional target directory for the rearranged files;
  defaults to `srcdirpath`, rearranging the files in place
* `hashname`: the file content hash algorithm name
* `move_move`: move files instead of linking them
* `symlink_mode`: symlink files instead of linking them
* `doit`: if true do the link/move/symlink, otherwise just print
* `quiet`: default `False`; if true do not print

## Function `run_remote_hashindex(rhost: str, argv, *, ssh_exe=None, hashindex_exe=None, check: bool = True, doit: bool = None, options: cs.cmdutils.BaseCommandOptions, **subp_options)`

Run a remote `hashindex` command.
Return the `CompletedProcess` result or `None` if `doit` is false.
Note that as with `cs.psutils.run`, the arguments are resolved
via `cs.psutils.prep_argv`.

Parameters:
* `rhost`: the remote host, or `user@host`
* `argv`: the command line arguments to be passed to the
  remote `hashindex` command
* `ssh_exe`: the `ssh` executable,
  default `SSH_EXE_DEFAULT`: `'ssh'`
* `hashindex_exe`: the remote `hashindex` executable,
  default `HASHINDEX_EXE_DEFAULT`: `'hashindex'`
* `check`: whether to check that the remote command has a `0` return code,
  default `True`
* `doit`: whether to actually run the command, default `True`
Other keyword parameters are passed therough to `cs.psutils.run`.

## Function `set_fstags_hashcode(fspath: str, hashcode, S: os.stat_result, fstags: cs.fstags.FSTags)`

Record `hashcode` against `fspath`.

# Release Log



*Release 20240316*:
Fixed release upload artifacts.

*Release 20240305*:
* HashIndexCommand.cmd_ls: support rhost:rpath paths, honour intterupts in the remote mode.
* HashIndexCommand.cmd_rearrange: new optional dstdir command line argument, passed to rearrange.
* merge: symlink_mode: leave identical symlinks alone, just merge tags.
* rearrange: new optional dstdirpath parameter, default srcdirpath.

*Release 20240216*:
* HashIndexCommand.cmdlinkto,cmd_rearrange: run the link/mv stuff with sys.stdout in line buffered mode.
* DO not get hashcodes from symlinks.
* HashIndexCommand.cmd_ls: ignore None hashcodes, do not set xit=1.
* New run_remote_hashindex() and read_remote_hashindex() functions.
* dir_filepaths: skip dot files, the fstags .fstags file and nonregular files.

*Release 20240211.1*:
Better module docstring.

*Release 20240211*:
Initial PyPI release: "hashindex" command and utility functions for listing file hashcodes and rearranging trees based on a hash index.
