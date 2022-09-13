The API is composed of a middleware service that randomly queries one of several maze generator microservices (MGs) available.

## Endpoints

### Maze Generator

Each MG has the following endpoints:

- `generateSegment`:
  - `type`: `POST`
  - `payload`: `JSON`
    ```json
    {
      limits: {
        'L': left limiting exit location,
        'R': right limiting exit location,
        'U': up limiting exit location,
        'D': down limiting exit location
      }
    }
    ```
    Location are objects with an x and a y coordinate attribute.
  - `response`: `JSON`
    ```json
    {
      geom: hex-encoded geometry of a 7x7 maze,
      exits: {
        'L': left exit location,
        'R': right exit location,
        'U': up exit location,
        'D': down exit location
      }
    }
    ```
    Exits in response are relative to the top left cell of the segment as (0,0).

### Middleware

The middleware has the following endpoints:

- `/`: `GET`, responds with the front-end page.
- `/generateSegment`:
  - `type`: `POST`
  - `payload`: `JSON`
    ```json
    {
      limits: {
        'L': left limiting exit location,
        'R': right limiting exit location,
        'U': up limiting exit location,
        'D': down limiting exit location
      }
    }
    ```
    Location are objects with an x and a y coordinate attribute.
  - `response`: `JSON`
    ```json
    {
      geom: hex-encoded geometry of a 7x7 maze,
      exits: {
        'L': left exit location,
        'R': right exit location,
        'U': up exit location,
        'D': down exit location
      }
    }
    ```
    Exits in response are relative to the top left cell of the segment as (0,0).

- `/login`:
  - `type`: `POST`
  - `payload`: `FORM`
    'username': Username

    Username is now registered

- `/login`:
  - `type`: `GET`
    Logged in as "username"

    Username is displayed

- `/logout`:
  - `type`: `GET`

    Logs user out if in session

- `/register`:
  - `type`: `PUT`
  - `payload`: `JSON`

    Registers username by author

- `/visit`:
  - `type`: `POST`
  - `payload`: `FORM`
    
    Posts locations visited in x,y format

- `/history/<username>`:
  - `type`: `GET`

    Shows last 50 points visited by user

- `/render`
  - `type`: `GET`
  - `response`: `JSON`
    ```json
    {
      "segments": List of segments (as in /generateSegment),
      "locations": [
        {
          "username": username,
          "x": x coordinate,
          "y": y coordinate
        },
        ...
      ]

    }
    ```

    Returns a list of all segments in maze and last location of all users


## Adding and Removing MGs

MGs are added by means of a PUT request by making sure there is a valid 'name', 'author', and 'url' in the given MG. After confirming the validity of the MG, the information is stored.

## Dependencies

Dependencies required are:

- `flask`, `python-dotenv` for all microservices
- `requests` for middleware-backend communication

## Flexibility

The front-end is meant to handle identifying the limiting exits for each generated segment, allowing the MGs to focus simply on generating mazes that meet or fall short of these exit locations and the middleware to select and forward from a maze generator. As a result, non-square block sizes can be supported.

## Implemented Advanced Features

The advanced feature implemented is adding a history to the maze. This is done by implementing a login/logout feature to be able to track a specific user every time said user logs in. 

To actually track the path the user makes in the maze, a POST request is sent for each spot the user has been through, given through x and y coordinates. In order to retrieve the history, a GET request was implemented to find the coordinated that were posted. 