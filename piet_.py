import numpy

from PIL import Image, ImageDraw

mind = [3, 2, 2]
maxd = [7, 4, 2]

minspacing = [0.05, 0.1, 0.2]

prob_nest = 0.15
prob_color = 0.15

resolution = 256

def transform(x, l, r):
    return l+x*(r-l)

class Table(object):
    
    def __init__(self, depth, left, right, bottom, top):
        
        self.depth = depth
        
        self.left = left
        self.right = right
        
        self.top = top
        self.bottom = bottom
        
        self.num_cols  = numpy.random.randint(mind[depth], maxd[depth]+1)
        self.num_rows  = numpy.random.randint(mind[depth], maxd[depth]+1)

        vs = self.create_divides(self.num_cols-1)
        hs = self.create_divides(self.num_rows-1)

        self.verticals = [ transform(v, left, right) for v in vs ]
        self.horizontals = [ transform(h, bottom, top) for h in hs ]
        
        self.table = [None] * (self.num_rows * self.num_cols)

        for r in range(self.num_rows):
            for c in range(self.num_cols):
                if depth < 2 and numpy.random.random() < prob_nest:
                    #self.table[r*self.num_cols + c] = 'Black'
                    self.table[r*self.num_cols + c] = Table(depth+1, self.verticals[c], self.verticals[c+1], self.horizontals[r], self.horizontals[r+1])
                elif numpy.random.random() < prob_color:
                    self.table[r*self.num_cols + c] = numpy.random.choice(['Red', 'Yellow', 'Blue', 'Red', 'Yellow', 'Blue', 'Black'])
                else:
                    self.table[r*self.num_cols + c] = 'White'

    def create_divides(self, num):
        divs = [0.0]
        for n in range(num):
            while True:
                x = numpy.random.random()
                div = transform(x, minspacing[self.depth], 1-minspacing[self.depth])
                overlap = False
                for d in divs:
                    if abs(div-d) < minspacing[self.depth]:
                        overlap = True
                        break
                if not overlap:
                    divs.append(div)
                    break
        divs.sort()
        divs.append(1.0)
        return divs

    def draw_table(self, image, dtable):
        for r in range(dtable.num_rows):
            for c in range(dtable.num_cols):
                if isinstance(dtable.table[r*dtable.num_cols + c], str):
                    image.rectangle([dtable.verticals[c], dtable.horizontals[r], dtable.verticals[c+1], dtable.horizontals[r+1]], fill=dtable.table[r*dtable.num_cols + c])
                else:
                    dtable.draw_table(image, dtable.table[r*dtable.num_cols + c])
        for v in range(dtable.num_cols+1):
            image.line([(dtable.verticals[v], dtable.bottom), (dtable.verticals[v], dtable.top)], fill='Black')
        for h in range(dtable.num_rows+1):
            image.line([(dtable.left, dtable.horizontals[h]), (dtable.right, dtable.horizontals[h])], fill='Black')
    
    def create_image(self, filename):
        ifile = Image.new('RGB', (resolution, resolution), 'White')
        image = ImageDraw.Draw(ifile, mode='RGB')
        self.draw_table(image, self)
        ifile.save(filename)
    
if __name__ == '__main__':
    
    piet = Table(0, 0.0, resolution, 0.0, resolution)
    piet.create_image('piet.bmp')
    
    
    
    
    
    
    
    