from matplotlib import pyplot as plt


class Vector:
    def __init__(self, x, y, u, v, root=True, color="black"):
        self.x = x
        self.y = y
        self.u = u
        self.v = v
        self.root = root
        self.color = color

    def get_vector(self):
        return self.x, self.y, self.u, self.v

    def get_line_segment(self):
        return [self.x, self.x + self.u], [self.y, self.y + self.v]

    def set_cross(self):
        self.root = False
        self.color = "red"


class Fractal:
    def __init__(self):
        self.vectors = list()
        self.vectors.append(Vector(0, 0, 0, 1))
        self.offset = max(map(lambda v: v.x, self.vectors)) - min(map(lambda v: v.x, self.vectors))
        self.num_layers = 1

    def add_layer(self):
        self.num_layers += 1
        this_layer = list()

        # Finding crosses and removing them from consideration
        for i in range(0, len(self.vectors)):
            for j in range(i + 1, len(self.vectors)):
                first_index = i if self.vectors[i].x > self.vectors[j].x else j
                second_index = i + j - first_index
                first_vec = self.vectors[i].get_vector() \
                    if self.vectors[i].x > self.vectors[j].x else self.vectors[j].get_vector()
                second_vec = self.vectors[j].get_vector() \
                    if self.vectors[i].x > self.vectors[j].x else self.vectors[i].get_vector()

                # Direct Cross
                if first_vec[1] == second_vec[1] and \
                        first_vec[0] - second_vec[0] == 1 and \
                        first_vec[2] == -1 and second_vec[2] == 1:
                    self.vectors[i].set_cross()
                    self.vectors[j].set_cross()

                # Right Vec (first) Higher
                if first_vec[1] - second_vec[1] == 1 and \
                        first_vec[0] - second_vec[0] == 2 and \
                        first_vec[2] == -1 and second_vec[2] == 1 and \
                        self.vectors[second_index].root:
                    self.vectors[j].set_cross()

                if first_vec[1] - second_vec[1] == -1 and \
                        first_vec[0] - second_vec[0] == 2 and \
                        first_vec[2] == -1 and second_vec[2] == 1 and \
                        self.vectors[first_index].root:
                    self.vectors[j].set_cross()

        # Finding convergence vectors
        convergences = list()
        for i in range(0, len(self.vectors)):
            for j in range(i + 1, len(self.vectors)):
                first_vec = self.vectors[i].get_vector() \
                    if self.vectors[i].x > self.vectors[j].x else self.vectors[j].get_vector()
                second_vec = self.vectors[j].get_vector() \
                    if self.vectors[i].x > self.vectors[j].x else self.vectors[i].get_vector()

                if self.vectors[i].root and self.vectors[j].root and \
                        first_vec[1] == second_vec[1] and \
                        first_vec[0] - second_vec[0] == 2 and first_vec[2] == -1 and second_vec[2] == 1:
                    x = (first_vec[0] + second_vec[0]) // 2
                    y = first_vec[1] + 1
                    convergences.append(Vector(x, y, 0, 1, color="lime"))
                    self.vectors[i].root = False
                    self.vectors[j].root = False

        # Adding convergence vectors to the layer
        this_layer.extend(convergences)

        # Adding diagonal vectors
        for vector in self.vectors:
            if vector.root:
                vector.root = False
                vector = vector.get_vector()
                x = vector[0] + vector[2]
                y = vector[1] + vector[3]
                this_layer.append(Vector(x, y, -1, 1))
                this_layer.append(Vector(x, y, 1, 1))

        self.vectors.extend(this_layer)

    def plot(self):
        for vector in self.vectors:
            plt.plot(*(vector.get_line_segment()), color=vector.color)
        plt.axis([-self.num_layers - fractal.offset, self.num_layers + fractal.offset, 0, 2 * self.num_layers])
        plt.gca().set_aspect("equal")
        plt.show()


fractal = Fractal()
for i in range(25):
    fractal.add_layer()
fractal.plot()
