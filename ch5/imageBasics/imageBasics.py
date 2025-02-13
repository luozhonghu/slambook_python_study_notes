import cv2
import numpy as np
import time

def main():
    # 读取命令行参数指定的图像
    import sys
    if len(sys.argv) < 2:
        print("请提供图像文件路径作为参数")
        return
    
    image_path = sys.argv[1]
    image = cv2.imread(image_path)

    # 判断图像文件是否正确读取
    if image is None:
        print(f"文件 {image_path} 不存在.")
        return

    # 输出基本信息
    print(f"图像宽为 {image.shape[1]}, 高为 {image.shape[0]}, 通道数为 {image.shape[2]}")
    cv2.imshow("image", image)
    cv2.waitKey(0)

    # 判断image的类型
    if image.dtype != np.uint8 or (image.ndim != 2 and image.ndim != 3):
        print("请输入一张彩色图或灰度图.")
        return

    # 遍历图像
    start_time = time.time()
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            pixel = image[y, x]
            # 这里可以对像素进行操作，比如:
            # for c in range(image.shape[2]):
            #     data = pixel[c]

    end_time = time.time()
    print(f"遍历图像用时：{end_time - start_time:.6f} 秒。")

    # 关于图像的拷贝
    image_another = image.copy()
    image_another[0:100, 0:100] = 0  # 将左上角100*100的块置零
    cv2.imshow("image", image)
    cv2.waitKey(0)

    # 使用copy()函数来拷贝数据
    image_clone = image.copy()
    image_clone[0:100, 0:100] = 255
    cv2.imshow("image", image)
    cv2.imshow("image_clone", image_clone)
    cv2.waitKey(0)

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()