# Infinite Maze

## Deployment

### Maze Generators

Maze Generators can be deployed by running `project-maze/start.sh`, a script which deploys every mg in `project-maze/mg` in separate Docker containers named `mg_<name>` with an exposed port in the 5001-and-above range.

### Middleware and Front-end

Middleware and front-end are deployed by starting the Flask app in `project-maze`.
