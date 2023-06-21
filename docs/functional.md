# Functional tests for cp command

All testing should be performed in the temporal directory. `cp` command
is expected to be installed system-wide.

Default testing structure should be the following:
```
    .
    ├── DstDir
    ├── srcA
    ├── srcB
    ├── SrcDir
    │   ├── srcC
    │   └── SrcSubDir
    │       └── srcD
    └── srcLnk -> srcA
```


[X] Exit code:
  [X] 0 - on success
  [X] non 0 - on failure

[X] Syntax:
  [X] cp with no arguments
  [X] cp with source argument only

[ ] No flags:

    [X] Copy single file to destination file
      |Done | Src File | Destination | Result                               |
      |-----|----------|-------------|--------------------------------------|
      | [X] | exists   | missing     | source as destination file           |
      | [X] | exists, not readable   | missing      | cp reports error      |
      | [X] | exists   | exists      | source replaces destination          |
      | [X] | exists   | exists, not writeable      | cp reports error      |
      | [X] | missing  | missing     | cp reports error (covered in syntax) |
      | [X] | missing  | exists      | cp reports error (covered in syntax) |

    [X] Copy single file by src relative path:
        [X] this directory
        [X] above directory
        [X] below directory
    [X] Copy single file by src absolute path
    [X] Copy single file by dst relative path
        [X] this directory
        [X] above directory
        [X] below directory
    [X] Copy single file by dst absolute path

    [X] Copy single file to destination directory
      |Done | Src File | DST Dir | DST file  | Result               |
      |-----|----------|---------|-----------|----------------------|
      | [X] | exists   | exists  | skipped   | src appears in dst   |
      | [X] | exists   | exists  | indicated | src appears in dst   |
      | [X] | exists   | missing | N/A       | cp reports error     |

    [X] Copy multiple files by explicit names to destination dir
      | Done| SrcA    | SrcB    | DstDir  |  Result               |
      |-----|---------|---------|---------|-----------------------|
      | [X] | exists  | exists  | exists  |  Srcs appears as Dsts |
      | [X] | exists  | exists  | missing |  cp reports an error  |
      | [X] | exists  | missing | missing |  cp reports an error  |
      | [X] | missing | exists  | missing |  cp reports an error  |

    [X] Copy multiple files by mask to destination dir:
      [X] Mask applies -> files under the mask are copied
      [X] Mask doesn't apply -> no files are copied

    [X] Copy directory to directory
      [X] Copy directory to existing directory with -r -> success
      [X] Copy directory to existing directory skipping -r -> failure
      [X] Copy directory to non-existing directory with -r-> success
      [X] Copy directory to non-existing directory skipping -r-> failure

[ ] Single-flag cases

  [ ] -a, --archive -> copies all src structure (use *rc* mask) to DST dir;
  [ ] --attributes-only -> no effect for new and existing files;
  [ ] --backup:
    [ ] none, off:
        [ ] No destination file -> Destination file appears, no backups;
        [ ] Destination file exists -> Destination file updates, no backups;
    [ ] numbered, t:
        [ ] No destination file -> Destination file appears, no backups;
        [ ] Destination file exists -> Destination file updates, backup appears;
        [ ] Destination file + backup exist -> Destination file updates, new backup appears;
    [ ] existing, nil:
        [ ] No destination file -> Destination file will be created, no backups;
        [ ] Destination file exists -> Destination file + simple backup will be created;
        [ ] Destination + numbered backup exist -> Destination + another numbered backup will be created;
        [ ] Destination + simple backup exist -> Destination + simple backup exist.
    [ ] simple, never:
        [ ] No destination files -> One destination file is created;
        [ ] One destination file -> One destination and one backup file will be created;
        [ ] One destination and one backup -> One destination and one backup will be created.
  [ ] -n:
     [ ] DST missing -> DST is created
     [ ] DST exists -> DST remains
