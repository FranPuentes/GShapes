#!/bin/env python3

from PIL import Image, ImageDraw;
import random;
import math;

#-------------------------------------------------------------------------------
def create_noise_on_image(image, draw, points=300, lines=60):
    width, height = image.size;
    for _ in range(points):
        x = random.randint(0, width)
        y = random.randint(0, height)
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        draw.point((x, y), fill=color)
    
    for _ in range(lines):
        start_point = (random.randint(0, width), random.randint(0, height))
        end_point = (random.randint(0, width), random.randint(0, height))
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        draw.line([start_point, end_point], fill=color, width=1)

#-------------------------------------------------------------------------------
def create_rotated_hexagon(draw, center, size, angle, fill_color):
    # Número de lados
    num_sides = 6
    # Calcular el radio del círculo circunscrito alrededor del pentágono
    radius = size / (2 * math.sin(math.pi / num_sides))
    # Ángulo interno para calcular la posición de los vértices
    internal_angle = 360 / num_sides
    # Coordenadas del pentágono antes de la rotación, centradas en el origen
    coords = [(math.cos(math.radians(internal_angle * i + angle)) * radius + center[0], math.sin(math.radians(internal_angle * i + angle)) * radius + center[1]) for i in range(num_sides)]
    draw.polygon(coords, outline="black", fill=fill_color)

#-------------------------------------------------------------------------------
def create_rotated_pentagon(draw, center, size, angle, fill_color):
    # Número de lados
    num_sides = 5
    # Calcular el radio del círculo circunscrito alrededor del pentágono
    radius = size / (2 * math.sin(math.pi / num_sides))
    # Ángulo interno para calcular la posición de los vértices
    internal_angle = 360 / num_sides
    # Coordenadas del pentágono antes de la rotación, centradas en el origen
    coords = [(math.cos(math.radians(internal_angle * i + angle)) * radius + center[0], math.sin(math.radians(internal_angle * i + angle)) * radius + center[1]) for i in range(num_sides)]    
    draw.polygon(coords, outline="black", fill=fill_color)
    
#-------------------------------------------------------------------------------
def create_rotated_square(draw, center, size, angle, fill_color):
    # Número de lados
    num_sides = 4
    # Calcular el radio del círculo circunscrito alrededor del pentágono
    radius = size / (2 * math.sin(math.pi / num_sides))
    # Ángulo interno para calcular la posición de los vértices
    internal_angle = 360 / num_sides
    # Coordenadas del pentágono antes de la rotación, centradas en el origen
    coords = [(math.cos(math.radians(internal_angle * i + angle)) * radius + center[0], math.sin(math.radians(internal_angle * i + angle)) * radius + center[1]) for i in range(num_sides)]
    draw.polygon(coords, outline="black", fill=fill_color)

#-------------------------------------------------------------------------------
def create_rotated_triangle(draw, center, size, angle, fill_color):
    # Número de lados
    num_sides = 3
    # Calcular el radio del círculo circunscrito alrededor del pentágono
    radius = size / (2 * math.sin(math.pi / num_sides))
    # Ángulo interno para calcular la posición de los vértices
    internal_angle = 360 / num_sides
    # Coordenadas del pentágono antes de la rotación, centradas en el origen
    coords = [(math.cos(math.radians(internal_angle * i + angle)) * radius + center[0], math.sin(math.radians(internal_angle * i + angle)) * radius + center[1]) for i in range(num_sides)]
    draw.polygon(coords, outline="black", fill=fill_color)

#-------------------------------------------------------------------------------
def create_circle(draw, center, diameter, fill_color):
    draw.ellipse([center[0]-diameter/2, center[1]-diameter/2, center[0]+diameter/2, center[1]+diameter/2], outline="black", fill=fill_color)

#-------------------------------------------------------------------------------
def is_valid_position(center, size, existing_squares):
    for existing_center, existing_size in existing_squares:
        distance = math.sqrt((existing_center[0] - center[0])**2 + (existing_center[1] - center[1])**2)
        if distance < (size + existing_size)/2:
           return False
    return True

#-------------------------------------------------------------------------------
def generate_random_rgb_color():
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255));
    return color;

#-------------------------------------------------------------------------------
def generate_biased_random_rgb_color():

    def biased_random_component():
        number = random.randint(0, 256);
        return 255 if number >128 else number;
    
    r = biased_random_component();
    g = biased_random_component();
    b = biased_random_component();
    
    return (r, g, b);

#-------------------------------------------------------------------------------
def create_image_with_shapes(image_size, n_shapes, boxing=False):

    image = Image.new('RGB', (image_size, image_size), 'white')

    draw = ImageDraw.Draw(image)
    
    create_noise_on_image(image, draw, 300, 120);
    
    existing_squares = []
    rt=[];

    for _ in range(n_shapes):
        attempts = 100
        while attempts > 0:
            attempts -= 1
            size = random.randint(40, 200)  # Tamaño del cuadrado delimitador
            center = (random.randint(size//2, image_size-size//2), random.randint(size//2, image_size-size//2))

            if is_valid_position(center, size, existing_squares):
                existing_squares.append((center, size))
                shape_type = random.choice(["hexagon", "pentagon", "square", "circle", "triangle"])
                angle = random.randint(0, 360)
                fill_color = generate_biased_random_rgb_color(); #random.choice([None, (255, 182, 193), (152, 251, 152), (173, 216, 230)])

                g=None;
                if   shape_type == 'hexagon':
                     create_rotated_hexagon(draw, center, size*0.5, angle, fill_color)
                     g=4;
                elif shape_type == 'pentagon':
                     create_rotated_pentagon(draw, center, size*0.6, angle, fill_color)
                     g=3;
                elif shape_type == 'square':
                     create_rotated_square(draw, center, size*0.75, angle, fill_color)
                     g=2;
                elif shape_type == 'triangle':
                     create_rotated_triangle(draw, center, size*0.85, angle, fill_color)
                     g=1;
                elif shape_type == 'circle':
                     create_circle(draw, center, size*0.9, fill_color)
                     g=0;

                x1 = center[0]-size/2
                y1 = center[1]-size/2
                x2 = center[0]+size/2
                y2 = center[1]+size/2
                
                rt.append( [g, (x1+(x2-x1)/2)/image_size, (y1+(y2-y1)/2)/image_size, (x2-x1)/image_size, (y2-y1)/image_size ] );
                
                if boxing:
                   # Dibujar el cuadrado delimitador                
                   draw.rectangle([x1, y1, x2, y2], outline="silver")
                
                break

    return image, rt

#-------------------------------------------------------------------------------
def generate_biased_random(thr=95):
    number = random.randint(0, 99);
    return 1 if number < thr else 0;

################################################################################
if __name__=="__main__":

   import os;
   
   TARGET="../data"
   
   for i in range(1000):
       
       n_shapes=generate_biased_random(95) * 15;
       
       image, coords = create_image_with_shapes(640, n_shapes, False);
       
       fnbase=os.path.join(TARGET,f"img-{i}");
       
       print(fnbase, flush=True);
       
       image.save(f"{fnbase}.png");
       
       with open(f"{fnbase}.txt","wt") as fd:
            for g,x,y,w,h in coords:
                print(f"{g} {x} {y} {w} {h}", end='\n', file=fd);
                
            
       