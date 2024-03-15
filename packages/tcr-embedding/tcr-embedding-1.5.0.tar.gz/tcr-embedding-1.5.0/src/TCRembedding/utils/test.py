from env_manager import VirtualEnvManager 

# 假定嵌入方法存放的基本路径
base_dir = f"D:\TCR\project\src\TCRembedding"

manager = VirtualEnvManager(base_dir)
manager.setup_virtualenv("GIANA", mirror_url="https://pypi.tuna.tsinghua.edu.cn/simple")
