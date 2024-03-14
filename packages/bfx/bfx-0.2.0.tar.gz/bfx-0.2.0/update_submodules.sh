#!/bin/bash

repos=(
    "https://github.com/not-a-feature/blosum.git"
    "https://github.com/not-a-feature/miniFasta.git"
    "https://github.com/not-a-feature/fastq.git"
    "https://github.com/not-a-feature/tajimas_d.git"
    # Add more repositories here
)

# Iterate through each repository
for repo in "${repos[@]}"; do
    # Extract the repository name from the URL
    repo_name=$(basename "$repo" .git)

    # Remove existing src/bfx/MODULE_NAME directory if it exists
    if [[ -d "src/bfx/$repo_name" ]]; then
        rm -rf "src/bfx/$repo_name"
    fi

    # Clone the latest version of the repository
    git clone "$repo"

    # Change working directory to the cloned repo
    cd "$repo_name"

    # Delete everything within the repository except "src"
    find . -maxdepth 1 ! -name 'src' -exec rm -rf {} \;

    # Move back to the parent directory
    cd ..

    mv "$repo_name" "src/bfx/$repo_name"
done

pre-commit run --all-files
