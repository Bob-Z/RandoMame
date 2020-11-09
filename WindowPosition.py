class WindowPosition:
    position = []

    def get(self, quantity, pos_x, pos_y, width, height):
        if quantity == 1:
            self.position.append({'pos_x': pos_x, 'pos_y': pos_y, 'width': width, 'height': height})

        else:
            height_ratio = height * 4 / 3  # TODO hard coded 4:3 ratio
            if width > height_ratio:
                new_width = width / 2
                new_height = height
                new_pos_x = pos_x + new_width
                new_pos_y = pos_y
            else:
                new_width = width
                new_height = height / 2
                new_pos_x = pos_x
                new_pos_y = pos_y + new_height

            quantity1 = quantity / 2
            quantity2 = quantity - quantity1

            self.get(quantity1, pos_x, pos_y, new_width, new_height)
            self.get(quantity2, new_pos_x, new_pos_y, new_width, new_height)

        return self.position
