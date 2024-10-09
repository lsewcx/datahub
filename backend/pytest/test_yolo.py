import os
import shutil
import pytest
import sys
import math
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.yolo import YOLO

@pytest.fixture
def setup_test_environment(tmp_path):
    # 创建临时数据集目录
    dataset_path = tmp_path / "data"
    dataset_path.mkdir()

    # 创建一些示例图像和标签文件
    for i in range(10):
        (dataset_path / f"image_{i}.jpg").write_text("image content")
        (dataset_path / f"image_{i}.txt").write_text(f"{i % 3} 0.5 0.5 0.5 0.5")

    return dataset_path

def test_export_to_yolo_format(setup_test_environment, tmp_path):
    dataset_path = setup_test_environment
    output_path = tmp_path / "yolo"

    result = YOLO.export_to_yolo_format(
        dataset_path=str(dataset_path),
        train_ratio=0.7,
        val_ratio=0.2,
        test_ratio=0.1,
        output_path=str(output_path),
    )

    # 检查输出目录是否存在
    assert (output_path / "train" / "images").exists()
    assert (output_path / "train" / "labels").exists()
    assert (output_path / "val" / "images").exists()
    assert (output_path / "val" / "labels").exists()
    assert (output_path / "test" / "images").exists()
    assert (output_path / "test" / "labels").exists()

    # 检查数据集分割比例
    total_files = len([f for f in os.listdir(dataset_path) if f.endswith('.jpg')])
    train_files = len(os.listdir(output_path / "train" / "images"))
    val_files = len(os.listdir(output_path / "val" / "images"))
    test_files = len(os.listdir(output_path / "test" / "images"))

    expected_train_files = math.ceil(0.7 * total_files)
    expected_val_files = math.ceil(0.2 * total_files)
    expected_test_files = math.ceil(0.1 * total_files)

    print(f"Total files: {total_files}")
    print(f"Train files: {train_files}, Expected: {expected_train_files}")
    print(f"Val files: {val_files}, Expected: {expected_val_files}")
    print(f"Test files: {test_files}, Expected: {expected_test_files}")

    assert train_files == expected_train_files
    assert val_files == expected_val_files
    assert test_files == expected_test_files

    # 检查 data.yaml 文件是否正确生成
    data_yaml_path = output_path / "data.yaml"
    assert data_yaml_path.exists()
    with open(data_yaml_path, 'r') as f:
        data_yaml_content = f.read()
        assert "train: ../train/images" in data_yaml_content
        assert "val: ../val/images" in data_yaml_content
        assert "test: ../test/images" in data_yaml_content

    # 检查返回结果
    assert result['totals'] == total_files
    assert len(result['labels']) > 0

def test_export_to_yolo_format_no_test(setup_test_environment, tmp_path):
    dataset_path = setup_test_environment
    output_path = tmp_path / "yolo"

    result = YOLO.export_to_yolo_format(
        dataset_path=str(dataset_path),
        train_ratio=0.8,
        val_ratio=0.2,
        test_ratio=0.0,
        output_path=str(output_path),
    )

    # 检查输出目录是否存在
    assert (output_path / "train" / "images").exists()
    assert (output_path / "train" / "labels").exists()
    assert (output_path / "val" / "images").exists()
    assert (output_path / "val" / "labels").exists()
    assert not (output_path / "test").exists()

    # 检查数据集分割比例
    total_files = len([f for f in os.listdir(dataset_path) if f.endswith('.jpg')])
    train_files = len(os.listdir(output_path / "train" / "images"))
    val_files = len(os.listdir(output_path / "val" / "images"))

    expected_train_files = math.ceil(0.8 * total_files)
    expected_val_files = math.ceil(0.2 * total_files)

    print(f"Total files: {total_files}")
    print(f"Train files: {train_files}, Expected: {expected_train_files}")
    print(f"Val files: {val_files}, Expected: {expected_val_files}")

    assert train_files == expected_train_files
    assert val_files == expected_val_files

    # 检查 data.yaml 文件是否正确生成
    data_yaml_path = output_path / "data.yaml"
    assert data_yaml_path.exists()
    with open(data_yaml_path, 'r') as f:
        data_yaml_content = f.read()
        assert "train: ../train/images" in data_yaml_content
        assert "val: ../val/images" in data_yaml_content
        assert "test: ../test/images" not in data_yaml_content

    # 检查返回结果
    assert result['totals'] == total_files
    assert len(result['labels']) > 0

def test_export_to_yolo_format_no_val_no_test(setup_test_environment, tmp_path):
    dataset_path = setup_test_environment
    output_path = tmp_path / "yolo"

    result = YOLO.export_to_yolo_format(
        dataset_path=str(dataset_path),
        train_ratio=1.0,
        val_ratio=0.0,
        test_ratio=0.0,
        output_path=str(output_path),
    )

    # 检查输出目录是否存在
    assert (output_path / "train" / "images").exists()
    assert (output_path / "train" / "labels").exists()
    assert not (output_path / "val").exists()
    assert not (output_path / "test").exists()

    # 检查数据集分割比例
    total_files = len([f for f in os.listdir(dataset_path) if f.endswith('.jpg')])
    train_files = len(os.listdir(output_path / "train" / "images"))

    expected_train_files = total_files

    print(f"Total files: {total_files}")
    print(f"Train files: {train_files}, Expected: {expected_train_files}")

    assert train_files == expected_train_files

    # 检查 data.yaml 文件是否正确生成
    data_yaml_path = output_path / "data.yaml"
    assert data_yaml_path.exists()
    with open(data_yaml_path, 'r') as f:
        data_yaml_content = f.read()
        assert "train: ../train/images" in data_yaml_content
        assert "val: ../val/images" not in data_yaml_content
        assert "test: ../test/images" not in data_yaml_content

    # 检查返回结果
    assert result['totals'] == total_files
    assert len(result['labels']) > 0

def test_export_to_yolo_format_no_labels(setup_test_environment, tmp_path):
    dataset_path = setup_test_environment
    output_path = tmp_path / "yolo"

    # 删除所有标签文件，模拟无标签情况
    for label_file in dataset_path.glob("*.txt"):
        label_file.unlink()

    result = YOLO.export_to_yolo_format(
        dataset_path=str(dataset_path),
        train_ratio=1.0,
        val_ratio=0.0,
        test_ratio=0.0,
        output_path=str(output_path),
    )

    # 检查输出目录是否存在
    assert (output_path / "train" / "images").exists()
    assert (output_path / "train" / "labels").exists()
    assert not (output_path / "val").exists()
    assert not (output_path / "test").exists()

    # 检查 data.yaml 文件是否不存在
    data_yaml_path = output_path / "data.yaml"
    assert not data_yaml_path.exists()  # 确保 data.yaml 文件不存在

    # 检查返回结果
    assert result['totals'] == 0  # 无标签情况下，totals 应为 0
    assert len(result['labels']) == 0  # 无标签情况下，labels 列表应为空