import os
import sys
import subprocess

# Auto-install Pillow if not present
try:
    from PIL import Image
except ImportError:
    print("正在安装必要的图片处理库 Pillow，请稍候...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
        from PIL import Image
        print("Pillow 安装成功！")
    except Exception as e:
        print(f"安装 Pillow 失败，请检查网络连接。错误信息: {e}")
        input("按任意键退出...")
        sys.exit(1)

def convert_single_file(file_path):
    lower_path = file_path.lower()
    if not (lower_path.endswith('.png') or lower_path.endswith('.webp')):
        return False
        
    try:
        img = Image.open(file_path)
        
        # Determine output path
        base, _ = os.path.splitext(file_path)
        output_path = base + '.jpg'
        
        # If image has alpha/transparency, paste on white background
        if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
            background = Image.new('RGB', img.size, (255, 255, 255))
            # Handle alpha band
            alpha = img.convert('RGBA').split()[-1]
            background.paste(img, mask=alpha)
            background.save(output_path, 'JPEG', quality=92)
        else:
            img.convert('RGB').save(output_path, 'JPEG', quality=92)
            
        # Close image file
        img.close()
        
        # Delete original file
        os.remove(file_path)
        print(f"[OK] 转换成功: {os.path.basename(file_path)} -> JPG")
        return True
    except Exception as e:
        print(f"[FAIL] 转换失败: {os.path.basename(file_path)}，错误: {e}")
        return False

def process_path(path):
    if not os.path.exists(path):
        return
        
    if os.path.isdir(path):
        print(f"[DIR] 正在处理文件夹: {path}")
        success_count = 0
        for root, dirs, files in os.walk(path):
            for file in files:
                full_path = os.path.join(root, file)
                if convert_single_file(full_path):
                    success_count += 1
        print(f"[DONE] 文件夹处理完毕！共转换并替换了 {success_count} 张图片。")
    else:
        convert_single_file(path)

if __name__ == '__main__':
    args = sys.argv[1:]
    if not args:
        print("提示: 请直接将图片或文件夹拖放到此脚本（或关联的 .bat 文件）上进行转换。")
        input("按任意键退出...")
        sys.exit(0)
        
    print("=" * 50)
    print("[RUN] 正在就地将图片转换为 JPG 并删除原图...")
    print("=" * 50)
    
    for arg in args:
        process_path(arg)
        
    print("\n[DONE] 所有任务处理完成！")
    # Auto close after 2 seconds instead of waiting for input, so it's very fast!
    import time
    time.sleep(2)
