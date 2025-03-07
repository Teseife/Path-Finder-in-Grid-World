from grid import Point
from utils import Stack, Queue, PriorityQueue
import math


class GridPathFinder:
    def __init__(self, source, destination, enclosures,turfs):
        """
        :param source:  Source point
        :param destination: Goal point
        :param enclosures: List of black polygons on the grid
        :param turfs: List of green polygons on the gird
        """
        self.source = source
        self.destination = destination
        self.enclosures = enclosures
        self.turfs = turfs


    def onLineSegment(self,p,p1,p2,eps=1e-9):
        """
        :param p:
        :param p1:
        :param p2:
        :param eps:
        :return: True if point P lies on the line segment [p1,p2].
                 This is done by checking collinearity via cross-product
                 and bound-boxing constraints
        """

        crossProd = (p.y - p1.y) * (p2.x - p1.x) - (p.x - p1.x) * (p2.y - p1.y)
        if abs(crossProd) > eps:
            return False
        # Check if p is within bounding box of p1 and p2
        if (min(p1.x, p2.x) - eps <= p.x <= max(p1.x, p2.x) + eps and min(p1.y, p2.y) - eps <= p.y <= max(p1.y, p2.y) + eps):
            return True
        return False

    def insidePolygon(self, point, polygon):
        """

        :param point:
        :param polygon:
        :return: Bool: True if the point is inside a polygon
        """
        # 1) Boundary Check: if point is on any edge of the polygon consider it as if is inside the polygon as well
        totalVerts = len(polygon)
        for i in range(totalVerts):
            p1 = polygon[i]
            p2 = polygon[(i + 1) % totalVerts]
            if self.onLineSegment(point, p1, p2):
                return True

        # 2) Standard ray-casting for interior
        xval, yval = point.x, point.y
        isInside = False
        px, py = polygon[0].x, polygon[0].y
        for i in range(totalVerts + 1):
            qx, qy = polygon[i % totalVerts].x, polygon[i % totalVerts].y
            match True:
                case _ if yval > min(py, qy) and yval <= max(py, qy) and xval <= max(px, qx):
                    if py != qy:
                        x_cross = (yval - py) * (qx - px) / (qy - py) + px
                    else:
                        x_cross = px
                    if px == qx or xval <= x_cross:
                         isInside = not isInside
                case _:
                    pass

            px, py = qx, qy
        return isInside

    def inEnclosure(self, point):
        """

        :param point:
        :return: Returns True if point is inside or on boundary of any black polygon ( enclosure )
        """
        for poly in self.enclosures:
            if self.insidePolygon(point, poly):
                return True
        return False

    def inTurf(self, point):
        """

        :param point:
        :return: True if point is inside or on boundary of any green polygon (turf)
        """
        for poly in self.turfs:
            if self.insidePolygon(point, poly):
                return True
        return False

    def expand_(self, current):
        """
        :param current:
        :return: valid neighbors in the order up,right,down,left. While avoiding any neighbor that is
                outside the 50*50 grid, and any point that in the boundary of the black polygons (enclosure)
        """
        directions = [(0,1),(1,0),(0,-1),(-1,0)] # up, right, down, left
        neighbors = []
        for dx, dy in directions:
            nx, ny = current.x + dx, current.y + dy
            if 0 <= nx < 50 and 0 <= ny < 50:
                candidate = Point(nx, ny)
                # Skip if inside or on boundary of black polygon
                if not self.inEnclosure(candidate):
                    neighbors.append(candidate)
        return neighbors

    def actionCost(self,point):
        """

        :param point:
        :return: the cost of stepping onto point:
                    - 1.5 if inside or on green turf polygon
                    -1.0 otherwise
        """

        if self.inTurf(point):
            return 1.5
        else:
            return 1.0

        #        *** Action cost and heuristic functions***

    def heuristic(self, point):
        """

        :param point:
        :return: The Euclidean distance form point to the destination point.
        Used for GBFS and A*
        """
        dx = point.x - self.destination.x
        dy = point.y - self.destination.y
        return math.sqrt(dx*dx + dy*dy)

    def searchSummary(self,algorithm,pathCost, nodeExpansions):
        """

        :param self:
        :param algorithm: Name of the algorithm
        :param pathCost: Number of steps taken to reach destination
        :param nodeExpansions: Number of nodes expanded
        :return: writes the values passed in the summary.txt file
        """
        with open('summary.txt','a') as f:
            f.write(f'{algorithm}:\nPath Cost:{pathCost}\nNodes expanded: {nodeExpansions}\n')



    #             ***Search algorithms***

    def bfs(self):
        '''

        :return: A path based on BFS algorithm
        '''
        frontier = Queue()
        exploredValue = set()
        pathCost = 0.0
        nodeExpansions = 0

        frontier.push([self.source])
        exploredValue.add((self.source.x,self.source.y))
        while not frontier.isEmpty():
            pathSoFar = frontier.pop()
            nodeExpansions += 1
            current = pathSoFar[-1]
            if current == self.destination:
                for i in range(1,len(pathSoFar)):
                    pathCost += self.actionCost(pathSoFar[i])
                self.searchSummary('BFS',pathCost,nodeExpansions)
                return pathSoFar

            for neighbor in self.expand_(current):
                neighborTuple = (neighbor.x, neighbor.y)
                if neighborTuple not in exploredValue:
                    exploredValue.add(neighborTuple)
                    new_path = pathSoFar + [neighbor]
                    frontier.push(new_path)
        return None  # No pathSoFar found

    def dfs(self):
        """
        :return: DFS storing pathSoFar in the frontier stack.
        """
        frontier = Stack()
        exploredValue = set()
        pathCost = 0.0
        nodeExpansions = 0

        frontier.push([self.source])
        exploredValue.add((self.source.x,self.source.y))

        while not frontier.isEmpty():
            pathSoFar = frontier.pop()
            nodeExpansions += 1
            current = pathSoFar[-1]
            if current == self.destination:
                for i in range(1,len(pathSoFar)):
                    pathCost += self.actionCost(pathSoFar[i])
                self.searchSummary('DFS',pathCost,nodeExpansions)
                return pathSoFar
            neighbors = self.expand_(current)
            for next in neighbors:
                nextTuple = (next.x,next.y)
                if nextTuple not in exploredValue:
                    exploredValue.add(nextTuple)
                    new_path = pathSoFar + [next]
                    frontier.push(new_path)
        return None

    def aStar(self):
        """

        :return: A* with path plus with cost-so-far (f(n)) in the frontier.
        where f = cost_so_far + heuristic(last_node). ( f(n) + h(n) )
        """
        frontier = PriorityQueue()
        bestCosts = {}
        startCost = 0.0
        nodeExpansions = 0
        pathCost = 0.0

        frontier.push(([self.source], startCost), startCost + self.heuristic(self.source))
        bestCosts[(self.source.x, self.source.y)] = 0.0

        while not frontier.isEmpty():
            (pathSoFar, costSoFar) = frontier.pop()
            nodeExpansions += 1
            currentNode = pathSoFar[-1]
            if currentNode == self.destination:
                for i in range(1,len(pathSoFar)):
                    pathCost += self.actionCost(pathSoFar[i])
                self.searchSummary('A*',pathCost,nodeExpansions)
                return pathSoFar
            for neighbor in self.expand_(currentNode):
                nextCoord = (neighbor.x, neighbor.y)
                stepCost = self.actionCost(neighbor)
                newTotalCost = costSoFar + stepCost
                if nextCoord not in bestCosts or newTotalCost < bestCosts[nextCoord]:
                    bestCosts[nextCoord] = newTotalCost
                    newPath = pathSoFar + [neighbor]
                    fVal = newTotalCost + self.heuristic(neighbor)
                    frontier.push((newPath, newTotalCost), fVal)
        return None

    def GBFS(self):
        """

        :return: Greedy Best First Search. Similar to A* but without cost-so-far.
        """
        frontier = PriorityQueue()
        visited = set()
        nodeExpansions = 0
        pathCost = 0.0

        frontier.push([self.source], self.heuristic(self.source))
        visited.add((self.source.x,self.source.y))

        while not frontier.isEmpty():
            pathSoFar = frontier.pop()
            nodeExpansions += 1
            currentNode = pathSoFar[-1]
            if currentNode == self.destination:
                for i in range(1,len(pathSoFar)):
                    pathCost += self.actionCost(pathSoFar[i])
                self.searchSummary('GBFS',pathCost,nodeExpansions)
                return pathSoFar
            for neighbor in self.expand_(currentNode):
                neighborTuple = (neighbor.x, neighbor.y)
                if neighborTuple not  in visited:
                    visited.add(neighborTuple)
                    newPath = pathSoFar + [neighbor]
                    heuristicVal = self.heuristic(neighbor)
                    frontier.push(newPath, heuristicVal)
        return None
