#!/bin/env python3

from PIL import Image, ImageDraw
import random
import math

def create_rotated_square(draw, center, size, angle, fill_color):
    # Calcular las coordenadas del cuadrado antes de la rotación
    coords = [(-size/2, -size/2), (-size/2, size/2), (size/2, size/2), (size/2, -size/2)]
    # Rotar cada punto alrededor del centro
    rotated_coords = [(x*math.cos(math.radians(angle)) - y*math.sin(math.radians(angle)) + center[0], x*math.sin(math.radians(angle)) + y*math.cos(math.radians(angle)) + center[1]) for x, y in coords]
    draw.polygon(rotated_coords, outline=None, fill=fill_color)

def create_rotated_triangle(draw, center, size, angle, fill_color):
    # Altura del triángulo equilátero
    height = size * math.sqrt(3) / 2
    # Coordenadas del triángulo antes de la rotación
    coords = [(0, -height/2), (-size/2, height/2), (size/2, height/2)]
    # Rotar cada punto alrededor del centro
    rotated_coords = [(x*math.cos(math.radians(angle)) - y*math.sin(math.radians(angle)) + center[0], x*math.sin(math.radians(angle)) + y*math.cos(math.radians(angle)) + center[1]) for x, y in coords]
    draw.polygon(rotated_coords, outline=None, fill=fill_color)

def create_circle(draw, center, diameter, fill_color):
    draw.ellipse([center[0]-diameter/2, center[1]-diameter/2, center[0]+diameter/2, center[1]+diameter/2], outline=None, fill=fill_color)

def is_valid_position(center, size, existing_squares):
    for existing_center, existing_size in existing_squares:
        distance = math.sqrt((existing_center[0] - center[0])**2 + (existing_center[1] - center[1])**2)
        if distance < (size + existing_size)/2:
           return False
    return True

def create_image_with_shapes(image_size, n_shapes, boxing=False):
    image = Image.new('RGB', (image_size, image_size), 'white')
    draw = ImageDraw.Draw(image)
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
                shape_type = random.choice(['square', 'circle', 'triangle'])
                angle = random.randint(0, 360)  # Ángulo de rotación
                fill_color = random.choice([(255, 182, 193), (152, 251, 152), (173, 216, 230)])  # Colores pastel

                g=None;
                if shape_type == 'square':
                    create_rotated_square(draw, center, size*0.7, angle, fill_color)
                    g=2;
                elif shape_type == 'triangle':
                    create_rotated_triangle(draw, center, size*0.8, angle, fill_color)
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

if __name__=="__main__":

   import os;
   
   TARGET="../data"
   
   for i in range(1000):
       
       image, coords = create_image_with_shapes(640, 20, False);
       
       fnbase=os.path.join(TARGET,f"img-{i}");
       
       print(fnbase, flush=True);
       
       image.save(f"{fnbase}.png");
       
       with open(f"{fnbase}.txt","wt") as fd:
            for g,x,y,w,h in coords:
                print(f"{g} {x} {y} {w} {h}", end='\n', file=fd);
                
            
       