import sys
import time
import threading
import warnings
from pathlib import Path
from tkinter import Tk, filedialog, messagebox

# 忽略 ffmpeg / avconv 的警告
warnings.filterwarnings("ignore", message="Couldn't find ffmpeg or avconv.*", category=RuntimeWarning)

sys.path.insert(0, r"D:\MarkItDown")
from markitdown import MarkItDown


def heartbeat(stop_event):
    seconds = 0
    while not stop_event.is_set():
        time.sleep(5)
        seconds += 5
        print(f"仍在使用 MarkItDown 转换中... 已耗时 {seconds} 秒")


def convert_pdf_markitdown(pdf_file: Path, output_file: Path):
    stop_event = threading.Event()
    t = threading.Thread(target=heartbeat, args=(stop_event,), daemon=True)

    try:
        print("正在初始化 MarkItDown...")
        md = MarkItDown()

        print("正在转换，请等待。MarkItDown 不支持逐页实时进度。")
        t.start()

        result = md.convert(str(pdf_file))

        stop_event.set()
        output_file.write_text(result.text_content, encoding="utf-8")

        print(f"\n转换完成：{output_file}")
        messagebox.showinfo("转换完成", f"Markdown 文件已生成：\n{output_file}")

    except Exception as e:
        stop_event.set()
        print("\n转换失败：", e)
        messagebox.showerror("转换失败", str(e))


def main():
    print("PDF 转 Markdown 工具启动")
    print("请选择 PDF 文件...")

    root = Tk()
    root.withdraw()
    root.attributes("-topmost", True)

    pdf_path = filedialog.askopenfilename(
        title="请选择要转换的 PDF 文件",
        filetypes=[("PDF 文件", "*.pdf")]
    )

    if not pdf_path:
        print("未选择文件，程序结束。")
        input("按回车键退出...")
        return

    pdf_file = Path(pdf_path)
    output_file = pdf_file.with_suffix(".md")

    print(f"已选择：{pdf_file}")
    print(f"输出文件：{output_file}\n")

    convert_pdf_markitdown(pdf_file, output_file)

    input("按回车键退出...")


if __name__ == "__main__":
    main()