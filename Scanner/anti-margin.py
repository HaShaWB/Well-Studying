from PIL import Image

def remove_margin(image_path):
    # 이미지 로드
    img = Image.open(image_path)
    
    # 이진 이미지로 변환 (필요한 경우)
    img = img.convert("L")  

    # 픽셀 데이터 가져오기
    pixels = img.load()

    # 이미지 크기 가져오기
    width, height = img.size

    # 왼쪽, 오른쪽, 위, 아래 마진 찾기
    background_color = min(pixels[0, 0], pixels[0, height-1], pixels[width-1, 0], pixels[width-1, height-1])

# 배경색이 아닌 픽셀 찾기
    non_background_pixels = [(x, y) for x in range(width) for y in range(height) if pixels[x, y] != background_color]

    # 배경색이 아닌 픽셀이 없는 경우, 전체 이미지가 배경색인 것으로 간주하고 원본 이미지 반환
    if not non_background_pixels:
        cropped_img = img
    else:
        # 좌표 리스트에서 x와 y의 최소/최대 값을 가져와 이미지를 자름
        x_coords, y_coords = zip(*non_background_pixels)
        left_margin = min(x_coords)-1
        right_margin = max(x_coords)+1
        top_margin = min(y_coords)-1
        bottom_margin = max(y_coords)+1

    # 이미지 자르기
    cropped_img = img.crop((left_margin, top_margin, right_margin + 1, bottom_margin + 1))

    return cropped_img