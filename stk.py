from PIL import Image


def stk_convert(input_path, output_path):
    try:
        # Открываем изображение
        image = Image.open(input_path)

        # Обрезаем или изменяем размер изображения до 512x512 пикселей
        width, height = image.size
        if width != height or width != 512:
            # Определяем координаты обрезки
            left = 0
            top = 0
            right = width
            bottom = height
            if width > height:
                # Обрезаем по горизонтали
                left = (width - height) // 2
                right = left + height
            elif height > width:
                # Обрезаем по вертикали
                top = (height - width) // 2
                bottom = top + width
            # Обрезаем или изменяем размер
            cropped_image = image.crop((left, top, right, bottom)).resize((512, 512), Image.BICUBIC)
        else:
            # Изменяем размер
            cropped_image = image.resize((512, 512), Image.BICUBIC)

        # Сохраняем обработанное изображение
        cropped_image.save(output_path, "PNG")

    except Exception as e:
        print(f"Произошла ошибка: {e}")
