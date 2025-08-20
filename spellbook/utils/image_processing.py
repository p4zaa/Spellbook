from PIL import Image

def remove_white_background(input_path, output_path, threshold=240, output_format="GIF", exact_white=False):
    """
    Remove white (or near-white) background from an image and save to desired format.
    
    Args:
        input_path (str): Path to input image (GIF/PNG/etc.)
        output_path (str): Base path for output file (extension added automatically)
        threshold (int): RGB threshold above which a pixel is considered white (ignored if exact_white=True)
        output_format (str): Output format, e.g. "GIF", "WEBP", "PNG"
        exact_white (bool): If True, remove only pure white (255,255,255).
                            If False, remove near-white using threshold.
    """
    img = Image.open(input_path)
    frames = []
    output_path = f"{output_path}.{output_format.lower()}"

    for frame in range(getattr(img, "n_frames", 1)):
        img.seek(frame)
        frame_img = img.convert("RGBA")

        new_data = []
        for r, g, b, a in frame_img.getdata():
            if exact_white:
                if (r, g, b) == (255, 255, 255):
                    new_data.append((255, 255, 255, 0))  # pure white → transparent
                else:
                    new_data.append((r, g, b, a))
            else:
                if r > threshold and g > threshold and b > threshold:
                    new_data.append((255, 255, 255, 0))  # near-white → transparent
                else:
                    new_data.append((r, g, b, a))
        frame_img.putdata(new_data)
        frames.append(frame_img)

    if output_format.upper() == "GIF":
        frames[0].save(
            output_path,
            save_all=True,
            append_images=frames[1:],
            loop=0,
            disposal=2,
            transparency=0,
        )
    elif output_format.upper() in ["WEBP", "PNG"]:
        if len(frames) > 1:
            frames[0].save(
                output_path,
                save_all=True,
                append_images=frames[1:],
                loop=0,
                format=output_format.upper()
            )
        else:
            frames[0].save(output_path, format=output_format.upper())
    else:
        raise ValueError(f"Unsupported format: {output_format}")

    return output_path
