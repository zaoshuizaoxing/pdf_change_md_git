import sys
from pathlib import Path
from tkinter import Tk, filedialog, messagebox
import fitz  # PyMuPDF
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn

def convert_pdf_pymupdf(pdf_file: Path, output_file: Path):
    try:
        doc = fitz.open(str(pdf_file))
        total_pages = doc.page_count

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(f"# {pdf_file.stem}\n\n")

            # 创建 Rich 进度条
            with Progress(
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                TimeRemainingColumn(),
            ) as progress:
                task = progress.add_task(f"转换中...", total=total_pages)

                for i, page in enumerate(doc, start=1):
                    text = page.get_text()
                    f.write(f"\n\n## 第 {i} 页\n\n")
                    if text.strip():
                        f.write(text)
                    else:
                        f.write("[本页未提取到文字，可能是扫描版图片 PDF]")
                    f.write("\n\n")

                    progress.update(task, advance=1)

        print(f"\n转换完成！Markdown 文件已生成：{output_file}")
        messagebox.showinfo("转换完成", f"Markdown 文件已生成：\n{output_file}")

    except Exception as e:
        print("\n转换失败：", e)
        messagebox.showerror("转换失败", str(e))


def main():
    print("快速 PDF → Markdown 工具（PyMuPDF 版）启动")
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

    convert_pdf_pymupdf(pdf_file, output_file)

    input("按回车键退出...")


if __name__ == "__main__":
    main()