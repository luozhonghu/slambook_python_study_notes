import numpy as np
import cv2
import open3d as o3d
from scipy.spatial.transform import Rotation as R

def read_pose_file(filename):
    poses = []
    with open(filename, 'r') as f:
        for line in f:
            data = list(map(float, line.strip().split()))
            q = data[3:]  # 四元数部分
            t = data[:3]  # 平移向量部分
            
            # 创建变换矩阵
            T = np.eye(4)
            T[:3, :3] = R.from_quat(q).as_matrix()
            T[:3, 3] = t
            
            poses.append(T)
    return poses

def main():
    color_imgs = []
    depth_imgs = []
    poses = read_pose_file("/Users/bytedance/Desktop/test/slambook_python/ch5/joinMap/pose.txt")

    # 读取图像
    for i in range(5):
        color_img = cv2.imread(f"/Users/bytedance/Desktop/test/slambook_python/ch5/joinMap/color/{i+1}.png")
        depth_img = cv2.imread(f"/Users/bytedance/Desktop/test/slambook_python/ch5/joinMap/depth/{i+1}.pgm", -1)
        color_imgs.append(color_img)
        depth_imgs.append(depth_img)

    # 相机内参
    cx, cy = 325.5, 253.5
    fx, fy = 518.0, 519.0
    depth_scale = 1000.0

    print("正在将图像转换为点云...")

    # 新建一个点云
    pcd = o3d.geometry.PointCloud()

    for i in range(5):
        print(f"转换图像中: {i+1}")
        color = color_imgs[i]
        depth = depth_imgs[i]
        T = poses[i]

        for v in range(color.shape[0]):
            for u in range(color.shape[1]):
                d = depth[v, u]
                if d == 0:
                    continue

                z = d / depth_scale
                x = (u - cx) * z / fx
                y = (v - cy) * z / fy

                point = np.dot(T, np.array([x, y, z, 1]))[:3]

                pcd.points.append(point)
                pcd.colors.append(color[v, u, ::-1] / 255.0)  # BGR to RGB

    pcd.points = o3d.utility.Vector3dVector(np.asarray(pcd.points))
    pcd.colors = o3d.utility.Vector3dVector(np.asarray(pcd.colors))

    print(f"点云共有 {len(pcd.points)} 个点.")

    # 保存点云
    o3d.io.write_point_cloud("/Users/bytedance/Desktop/test/slambook_python/ch5/joinMap/map.pcd", pcd)

    # 可视化点云
    o3d.visualization.draw_geometries([pcd])

if __name__ == "__main__":
    main()

# poses = read_pose_file("/Users/bytedance/Desktop/test/slambook_python/ch5/joinMap/pose.txt")
# print(poses)