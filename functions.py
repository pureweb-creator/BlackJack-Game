from PIL import Image

def render_image(img_path, img_count, image_name):
    img_list = []

    # create image list
    for i in range(img_count):
        current_image = Image.open(img_path[i], 'r')
        current_image = current_image.resize((70,103),Image.ANTIALIAS)
        img_list.append(current_image)
    
    img_size     = Image.open("static/images/2_of_clubs.png", "r")
    img_size     = img_size.resize((70,103), Image.ANTIALIAS)
    img_w, img_h = img_size.size

    background  = Image.open('static/images/bg.png') # create bg
    bg_w, bg_h  = background.size
    offset_list = []
    offset_left = 1

    # create offsets
    for i in range(1,img_count+1):
        if (i==1): offset_list.append((15, (bg_h - img_h) // 2))
        if (i>=2): offset_list.append(((offset_left*i + img_w//4*(i-1)+10 ), (bg_h - img_h) // 2))

    # create image with offsets 
    for i in range(len(offset_list)):
        background.paste(img_list[i], offset_list[i])

    background.save(f'static/images/{image_name}', format='webp')