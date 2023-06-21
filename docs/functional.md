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
    [ ] Copy single file by src absolute path
    [ ] Copy single file by dst relative path
        [ ] this directory
        [ ] above directory
        [ ] below directory
    [ ] Copy single file by dst absolute path

    [ ] Copy single file to destination directory
      |Done | Src File | DST Dir | DST file | Result               |
      |-----|----------|---------|----------|----------------------|
      | [ ] | exists   | exists  | missing  | src appears in dst   |
      | [ ] | exists   | exists  | exists   | src replaces dst     |
      | [ ] | exists   | missing | N/A      | cp reports error     |
      | [ ] | missing  | missing | N/A      | cp reports error     |

    [ ] Copy multiple files by explicit names to destination dir
      | Done| SrcA    | SrcB    | DstA    | DstB    | Result               |
      |-----|---------|---------|---------|---------|----------------------|
      | [ ] | exists  | exists  | missing | missing | Srcs appears as Dsts |
      | [ ] | exists  | exists  | exists  | missing | Srcs appears as Dsts |
      | [ ] | exists  | exists  | exists  | exists  | Srcs appears as Dsts |
      | [ ] | exists  | missing | missing | missing | cp reports an error  |
      | [ ] | missing | exists  | missing | missing | cp reports an error  |

    [ ] Copy multiple files by mask to destination dir:
      [ ] Mask applies -> files under the mask are copied
      [ ] Mask doesn't apply -> no files are copied

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
