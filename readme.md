# UMassCTF '24 Challenges & Infra Repo

## Challenges

Each challenge should follow the following hierarchy: `/category/challenge_name/`

Each challenge should also include the following:

- `README.md` - This file should include the following:
  - Challenge name as displayed to the user
  - Challenge description as displayed to the user
  - Challenge flag in format `UMASS{...}`
  - A description of the challenge (not given to the users)
  - A description of how to solve the challenge
- `/challenge` - The directory containing the challenge source and build/run information
  - This should include a `Dockerfile`
- `/static` - This directory contains the file(s) that will be given to the user
- `/solve` - This directory should contain any file(s) and scripts used to solve the challenge
- `/challenge.yaml` - The kctf config for deploying the challenge

### Contributing

Each challenge should have its own branch before being merged. The branch naming convention should be `category-challenge_name`