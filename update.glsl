// Uniforms
uniform vec2 worldSize;
uniform float sensorAngle;
uniform float speed;
uniform float radius;
uniform float pheromoneValue;

// Function to reflect at boundary
vec3 reflectAtBoundary(vec3 position, vec3 agentPosition) {
    if (abs(position.x) > 1.0) {
        position.x = 2.0 * (position.x > 0.0) - position.x;
    }

    if (abs(position.y) > 1.0) {
        position.y = 2.0 * (position.y > 0.0) - position.y;
    }

    vec3 delta = position - agentPosition;
    float angle = atan(delta.y, delta.x);

    return vec3(position.xy, angle);
}

// Function to map float to int
ivec2 mapFloatToInt(vec2 coordinates) {
    vec2 floatToWorldSize = vec2(2.0, 2.0);
    ivec2 newCoordinates;

    for (int i = 0; i < 2; ++i) {
        int coordinate = int((coordinates[i] + 1.0) * 0.5 * worldSize[i]);
        coordinate = max(0, min(int(worldSize[i]) - 1, coordinate));
        newCoordinates[i] = coordinate;
    }

    return newCoordinates;
}

// Function to map int to float
vec2 mapIntToFloat(ivec2 coordinates) {
    vec2 floatToWorldSize = vec2(2.0, 2.0);
    vec2 newCoordinates;

    for (int i = 0; i < 2; ++i) {
        float coordinate = -1.0 + (2.0 * float(coordinates[i]) / worldSize[i]);
        newCoordinates[i] = coordinate;
    }

    return newCoordinates;
}

// Function to update agent's position
void makeMove(inout vec2 floatXPos, inout vec2 floatYPos, inout float movementAngle, float[] world) {
    vec2 currentPosition = vec2(floatXPos, floatYPos);

    // Update pheromone concentration at current position
    ivec2 indices = mapFloatToInt(currentPosition);
    world[indices.x * int(worldSize.y) + indices.y] += pheromoneValue;

    // Get the best move
    vec3 nextMove = getBestMove(currentPosition, movementAngle, world);

    // Move the agent to the next position
    floatXPos = nextMove.x;
    floatYPos = nextMove.y;

    // Update the direction the agent is looking at after the move
    movementAngle = nextMove.z + radians(float(rand() % 11 - 5));
}

// Function to get the best move
vec3 getBestMove(vec2 currentPosition, float movementAngle, float[] world) {
    vec3 possibleMoves[3];

    // Iterate over sensor angles
    for (int i = 0; i < 3; ++i) {
        float sensorAngle = radians(float(i - 1) * sensorAngle);
        float angle = movementAngle + sensorAngle;

        vec2 newPosition = currentPosition + speed * radius * vec2(cos(angle), sin(angle));

        // Reflect at the boundary if the new position is outside the world
        if (!(newPosition.x >= 0.0 && newPosition.x <= 1.0 && newPosition.y >= 0.0 && newPosition.y <= 1.0)) {
            newPosition = reflectAtBoundary(newPosition, vec3(currentPosition, 0.0)).xy;
        }

        // Append the move to the list of possible moves
        possibleMoves[i] = vec3(newPosition, angle);
    }

    // Find the move with the maximum pheromone concentration
    int maxIdx = 0;
    float maxPheromone = world[mapFloatToInt(possibleMoves[0].xy).x * int(worldSize.y) + mapFloatToInt(possibleMoves[0].xy).y];
    
    for (int i = 1; i < 3; ++i) {
        float pheromone = world[mapFloatToInt(possibleMoves[i].xy).x * int(worldSize.y) + mapFloatToInt(possibleMoves[i].xy).y];
        if (pheromone > maxPheromone) {
            maxPheromone = pheromone;
            maxIdx = i;
        }
    }

    return possibleMoves[maxIdx];
}
