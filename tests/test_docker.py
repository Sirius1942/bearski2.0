from core.docker_builder import DockerBuilder

def test_docker_generation():
    files = DockerBuilder.save_all(".")
    print(f"✅ 生成文件: {files}")
    
    # 验证文件存在
    import os
    for f in files:
        assert os.path.exists(f), f"文件不存在: {f}"
    
    print("✅ Docker 配置生成成功")

if __name__ == "__main__":
    test_docker_generation()
