"""Contains class to calculate best vertical seam to remove in a picture."""
import numpy as np
import imagematrix

class ResizeableImage(imagematrix.ImageMatrix):
    """Calculates best vertical seam to remove given a picture."""
    def best_seam(self):
        """Returns a list of tuples of coordinates of best steam to remove."""
        weight_table = np.empty((self.height, self.width), dtype=float)
        parent = np.empty((self.height, self.width), dtype=int)
        for i in range(self.width):
            weight_table[0, i] = self.energy(i, 0)
            parent[0, i] = -1

        for i in range(1, self.height):
            for j in range(self.width):
                left_weight = (weight_table[i - 1, j - 1] if j > 0 else
                    float('inf'))
                centre_weight = weight_table[i - 1, j]
                right_weight = (weight_table[i - 1, j + 1] if j < self.width - 1
                    else float('inf'))
                if (centre_weight <= right_weight and centre_weight <=
                    left_weight):
                    weight_table[i, j] = self.energy(j, i) + centre_weight
                    parent[i, j] = j
                elif (left_weight <= centre_weight and left_weight <=
                    right_weight):
                    weight_table[i, j] = self.energy(j, i) + left_weight
                    parent[i, j] = j - 1
                else:
                    weight_table[i, j] = self.energy(j, i) + right_weight
                    parent[i, j] = j + 1

        # Construct list of coordinates for the best seam.
        best_in_top_row = weight_table[self.height - 1].argmin()
        ret = [(best_in_top_row, self.height - 1)]
        for i in reversed(range(1, self.height)):
            ret.append((parent[i, ret[-1][0]], i - 1))
        return ret

    def remove_best_seam(self):
        """Wrapper function."""
        self.remove_seam(self.best_seam())
