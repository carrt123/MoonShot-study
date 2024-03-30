from image.img_generator import get_requirement, generate_img

if __name__ == '__main__':
    while True:
        requirement = get_requirement()
        if not requirement:
            break

        generate_img(requirement)
