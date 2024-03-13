# Self Documenting Data Management Plan

## Usage

`python create_html_files.py --input "example_project" --output "docs"`

`--output`  is optional. By default, it will create a directory called "docs" in the current working directory.

## Setup

We expect a directory that contains one or more sub-directories, and one or more files. In the root directory, place a file called "README.yaml" that contains any common metadata that should apply to all files in the directory in yaml format.

Example:

```yaml
visibility: public
project-name: <title>
principal-investigator:
  - name: <name>
    email: <email>
  - name: <name2>
    email: <email2>
grand-ids:
  EU-Horizon: <number1>
  DFG: <number2>
description: "Root folder for Example Project"
```

In any subfolder, we can place another file that contains any subset of this information. 

Example:

in example_project/20-29 Communication/20 Internal we place a README.yaml that looks like this:
```yaml
ignore-section: true
description: "Internal Project Communications - not intended for publication"
```

When determining metadata for files in this folder, it inherits all of the metadata from the root file above, adds a new one ("ignore-section") and replaces the content of another ("description").

## Output

The included script will scan the indicated input directory and create a collection of simple html pages in the output directory. The root page will be an index that links to every other page that was created. Each page contains a table with metadata for that directory and all directories that are children of that one.
