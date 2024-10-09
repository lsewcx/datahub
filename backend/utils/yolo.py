import os
import shutil
from loguru import logger
from sklearn.model_selection import train_test_split

'''
用于导出YOLO格式数据集
暂时只支持yolo格式的txt文件的标签
后续尝试支持voc或者是coco格式的标签
'''
class YOLO:
    @staticmethod
    def export_to_yolo_format(
        dataset_path: str,
        train_ratio: float,
        val_ratio: float,
        test_ratio: float,
        output_path: str,
    ) -> dict:
        """
        导出YOLO格式数据集

        Args:
            dataset_path (str): 数据集路径
            train_ratio (float): 训练集比例
            val_ratio (float): 验证集比例
            test_ratio (float): 测试集比例
            output_path (str): 输出路径
        Returns:
            dict: 导出结果
        """
        os.makedirs(output_path, exist_ok=True)
        tmp_path = os.path.join(output_path, 'tmp')
        os.makedirs(tmp_path, exist_ok=True)

        # 递归搜索文件夹中的所有文件并复制到 tmp 文件夹
        for root, _, files in os.walk(dataset_path):
            for file in files:
                file_path = os.path.join(root, file)
                shutil.copy(file_path, os.path.join(tmp_path, file))

        # 创建输出目录
        if train_ratio:
            train_images_path = os.path.join(output_path, 'train', 'images')
            train_labels_path = os.path.join(output_path, 'train', 'labels')
            os.makedirs(train_images_path, exist_ok=True)
            os.makedirs(train_labels_path, exist_ok=True)
        if val_ratio:
            val_images_path = os.path.join(output_path, 'val', 'images')
            val_labels_path = os.path.join(output_path, 'val', 'labels')
            os.makedirs(val_images_path, exist_ok=True)
            os.makedirs(val_labels_path, exist_ok=True)
        if test_ratio:
            test_images_path = os.path.join(output_path, 'test', 'images')
            test_labels_path = os.path.join(output_path, 'test', 'labels')
            os.makedirs(test_images_path, exist_ok=True)
            os.makedirs(test_labels_path, exist_ok=True)
        
        # 读取 tmp 文件夹中的所有文件
        images = [f for f in os.listdir(tmp_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        labels = [f for f in os.listdir(tmp_path) if f.lower().endswith('.txt')]
        try:
            # 确保每个 image 文件都有对应的 label 文件
            image_label_pairs = []
            for image in images:
                label = os.path.splitext(image)[0] + '.txt'
                if label in labels:
                    image_label_pairs.append((image, label))

            images, labels = zip(*image_label_pairs)
        except Exception as e:
            logger.error(f"Failed to match image and label files: {e}")
            return {
                'message': 'Failed to match image and label files',
                'totals': 0,
                'labels': [],
                'output_path': output_path
            }

        # 分割数据集
        if val_ratio + test_ratio > 0:
            train_images, temp_images, train_labels, temp_labels = train_test_split(images, labels, train_size=train_ratio)
            if test_ratio > 0:
                val_images, test_images, val_labels, test_labels = train_test_split(temp_images, temp_labels, test_size=test_ratio/(val_ratio + test_ratio))
            else:
                val_images, val_labels = temp_images, temp_labels
                test_images, test_labels = [], []
        else:
            train_images, train_labels = images, labels
            val_images, val_labels = [], []
            test_images, test_labels = [], []

        # 复制文件
        for image, label in zip(train_images, train_labels):
            shutil.copy(os.path.join(tmp_path, image), os.path.join(train_images_path, image))
            shutil.copy(os.path.join(tmp_path, label), os.path.join(train_labels_path, label))

        for image, label in zip(val_images, val_labels):
            shutil.copy(os.path.join(tmp_path, image), os.path.join(val_images_path, image))
            shutil.copy(os.path.join(tmp_path, label), os.path.join(val_labels_path, label))

        for image, label in zip(test_images, test_labels):
            shutil.copy(os.path.join(tmp_path, image), os.path.join(test_images_path, image))
            shutil.copy(os.path.join(tmp_path, label), os.path.join(test_labels_path, label))

        # 删除 tmp 文件夹
        shutil.rmtree(tmp_path)
        try:
            # 读取所有标签文件中的内容来生成 names 列表
            class_names = set()
            for label_file in os.listdir(train_labels_path):
                label_file_path = os.path.join(train_labels_path, label_file)
                with open(label_file_path, 'r') as f:
                    for line in f:
                        class_id = int(line.split()[0])
                        class_names.add(class_id)

            class_names = sorted(list(class_names))
            nc = len(class_names)
            names = [f'{i}' for i in class_names]
        except Exception as e:
            logger.error(f"Failed to read label files: {e}")
            return {
                'message': 'Failed to read label files',
                'totals': 0,
                'labels': [],
                'output_path': output_path
            }  

        # 生成 data.yaml 文件
        data_yaml_content = f"""
    train: ../train/images
    """
        if val_ratio > 0:
            data_yaml_content += "val: ../val/images\n"
        if test_ratio > 0:
            data_yaml_content += "test: ../test/images\n"

        data_yaml_content += f"""
    nc: {nc}
    names: {names}
    """
        with open(os.path.join(output_path, 'data.yaml'), 'w') as f:
            f.write(data_yaml_content)
        logger.info(f"Exported dataset to YOLO format: {output_path}")
        return {
            'message': 'Exported dataset to YOLO format',
            'totals': len(images),
            'labels': names,
            'output_path': output_path
        }
