import math
import sys

class CalculatorAgent:
    def __init__(self):
        self.name = "计算器智能体"
        self.math_functions = {
            "abs": abs, "pow": pow, "sqrt": math.sqrt,
            "sin": math.sin, "cos": math.cos, "tan": math.tan,
            "asin": math.asin, "acos": math.acos, "atan": math.atan,
            "sinh": math.sinh, "cosh": math.cosh, "tanh": math.tanh,
            "log": math.log, "log10": math.log10, "log2": math.log2,
            "exp": math.exp, "floor": math.floor, "ceil": math.ceil,
            "round": round, "fabs": math.fabs, "factorial": math.factorial,
            "pi": math.pi, "e": math.e
        }
    
    def calculate(self, expression):
        if expression.lower() == "help":
            return self.show_help()
        
        try:
            result = eval(expression, {"__builtins__": None}, self.math_functions)
            return f"计算结果：{result}"
        except ZeroDivisionError:
            return "错误：不能除以零"
        except SyntaxError:
            return "错误：表达式语法不正确"
        except ValueError as e:
            return f"错误：{str(e)}"
        except Exception as e:
            return f"错误：{str(e)}"
    
    def show_help(self):
        help_text = "\n支持的数学函数：\n"
        help_text += "【基本运算】\n"
        help_text += "  + - * /  (加减乘除)\n"
        help_text += "  pow(x, y)  (x的y次方)\n"
        help_text += "\n【三角函数】\n"
        help_text += "  sin(x) cos(x) tan(x)  (正弦、余弦、正切)\n"
        help_text += "  asin(x) acos(x) atan(x)  (反正弦、反余弦、反正切)\n"
        help_text += "\n【双曲函数】\n"
        help_text += "  sinh(x) cosh(x) tanh(x)  (双曲正弦、余弦、正切)\n"
        help_text += "\n【对数函数】\n"
        help_text += "  log(x)  (自然对数)  log10(x)  (常用对数)  log2(x)  (以2为底)\n"
        help_text += "\n【其他函数】\n"
        help_text += "  sqrt(x)  (平方根)  exp(x)  (e的x次方)\n"
        help_text += "  abs(x)  (绝对值)  floor(x)  (向下取整)\n"
        help_text += "  ceil(x)  (向上取整)  round(x)  (四舍五入)\n"
        help_text += "  factorial(x)  (阶乘)\n"
        help_text += "\n【常数】\n"
        help_text += "  pi  (圆周率)  e  (自然常数)\n"
        help_text += "\n示例：2 + 3 * 4, sqrt(16), sin(pi/2), factorial(5)"
        return help_text
    
    def run_cli(self):
        print(f"欢迎使用 {self.name}！")
        print("支持的运算：+ - * / 以及多种数学函数")
        print("输入 'help' 查看所有支持的函数")
        print("输入 'exit' 退出\n")
        
        while True:
            user_input = input("你: ")
            if user_input.lower() == "exit":
                print(f"{self.name}: 再见！")
                break
            
            response = self.calculate(user_input)
            print(f"{self.name}: {response}\n")

def run_gui():
    import tkinter as tk
    from tkinter import ttk, messagebox
    
    class CalculatorAgentGUI:
        def __init__(self, root):
            self.root = root
            self.root.title("智能计算器")
            self.root.geometry("500x600")
            self.root.resizable(False, False)
            
            self.math_functions = {
                "abs": abs, "pow": pow, "sqrt": math.sqrt,
                "sin": math.sin, "cos": math.cos, "tan": math.tan,
                "asin": math.asin, "acos": math.acos, "atan": math.atan,
                "sinh": math.sinh, "cosh": math.cosh, "tanh": math.tanh,
                "log": math.log, "log10": math.log10, "log2": math.log2,
                "exp": math.exp, "floor": math.floor, "ceil": math.ceil,
                "round": round, "fabs": math.fabs, "factorial": math.factorial,
                "pi": math.pi, "e": math.e
            }
            
            self.setup_gui()
        
        def setup_gui(self):
            style = ttk.Style()
            style.theme_use('clam')
            
            style.configure('Title.TLabel', font=('微软雅黑', 18, 'bold'), foreground='#ffffff')
            style.configure('Result.TLabel', font=('微软雅黑', 16), foreground='#000000')
            style.configure('Input.TEntry', font=('微软雅黑', 14))
            style.configure('Calc.TButton', font=('微软雅黑', 12, 'bold'), padding=10)
            style.configure('Func.TButton', font=('微软雅黑', 10), padding=5)
            
            gradient_frame = tk.Frame(self.root, bg='#1a1a2e')
            gradient_frame.pack(fill=tk.BOTH, expand=True)
            
            title_label = ttk.Label(gradient_frame, text="🧮 智能计算器", style='Title.TLabel', background='#1a1a2e')
            title_label.pack(pady=20)
            
            input_frame = ttk.Frame(gradient_frame, padding=15)
            input_frame.pack(padx=20, pady=10, fill=tk.X)
            
            self.input_entry = ttk.Entry(input_frame, style='Input.TEntry', width=40)
            self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            calc_button = ttk.Button(input_frame, text="计算", style='Calc.TButton', 
                                     command=self.calculate, width=10)
            calc_button.pack(side=tk.RIGHT, padx=10)
            
            result_frame = ttk.Frame(gradient_frame, padding=15)
            result_frame.pack(padx=20, pady=10, fill=tk.X)
            
            result_label = ttk.Label(result_frame, text="计算结果：", font=('微软雅黑', 12), 
                                     background='#1a1a2e', foreground='#a0a0a0')
            result_label.pack(anchor=tk.W)
            
            self.result_text = tk.Text(result_frame, height=3, width=50, font=('微软雅黑', 14),
                                       bg='#ffffff', fg='#000000', bd=2, relief=tk.SOLID)
            self.result_text.pack(fill=tk.X)
            self.result_text.insert(tk.END, "等待输入...")
            self.result_text.config(state=tk.DISABLED)
            
            func_frame = ttk.Frame(gradient_frame, padding=10)
            func_frame.pack(padx=20, pady=10, fill=tk.X)
            
            func_label = ttk.Label(func_frame, text="常用函数：", font=('微软雅黑', 12),
                                   background='#1a1a2e', foreground='#a0a0a0')
            func_label.grid(row=0, column=0, columnspan=4, sticky='w', pady=5)
            
            functions = [
                ('sqrt', '平方根'), ('sin', '正弦'), ('cos', '余弦'), ('tan', '正切'),
                ('log', '自然对数'), ('log10', '常用对数'), ('pow', '幂运算'), ('abs', '绝对值'),
                ('pi', 'π'), ('e', 'e'), ('floor', '向下取整'), ('ceil', '向上取整'),
                ('factorial', '阶乘'), ('exp', '指数'), ('log2', 'log2'), ('round', '四舍五入')
            ]
            
            row = 1
            col = 0
            for func_name, func_desc in functions:
                btn = ttk.Button(func_frame, text=f"{func_name}", style='Func.TButton',
                                 command=lambda fn=func_name: self.insert_function(fn))
                btn.grid(row=row, column=col, padx=5, pady=5, sticky='nsew')
                col += 1
                if col == 4:
                    col = 0
                    row += 1
            
            func_frame.grid_columnconfigure((0,1,2,3), weight=1)
            
            help_frame = ttk.Frame(gradient_frame, padding=10)
            help_frame.pack(padx=20, pady=10, fill=tk.X)
            
            help_button = ttk.Button(help_frame, text="📖 查看帮助", command=self.show_help)
            help_button.pack()
            
            self.input_entry.bind('<Return>', lambda event: self.calculate())
        
        def insert_function(self, func_name):
            current = self.input_entry.get()
            if func_name in ['pi', 'e']:
                self.input_entry.delete(0, tk.END)
                self.input_entry.insert(tk.END, current + func_name)
            else:
                self.input_entry.delete(0, tk.END)
                self.input_entry.insert(tk.END, current + f"{func_name}(")
        
        def calculate(self):
            expression = self.input_entry.get().strip()
            if not expression:
                self.update_result("请输入数学表达式")
                return
            
            try:
                result = eval(expression, {"__builtins__": None}, self.math_functions)
                self.update_result(f"计算结果：{result}")
            except ZeroDivisionError:
                self.update_result("❌ 错误：不能除以零")
            except SyntaxError:
                self.update_result("❌ 错误：表达式语法不正确")
            except ValueError as e:
                self.update_result(f"❌ 错误：{str(e)}")
            except Exception as e:
                self.update_result(f"❌ 错误：{str(e)}")
        
        def update_result(self, text):
            self.result_text.config(state=tk.NORMAL)
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, text)
            self.result_text.config(state=tk.DISABLED)
        
        def show_help(self):
            help_text = """支持的数学函数：

【基本运算】
+ - * /  (加减乘除)
pow(x, y)  (x的y次方)

【三角函数】
sin(x) cos(x) tan(x)  (正弦、余弦、正切)
asin(x) acos(x) atan(x)  (反正弦、反余弦、反正切)

【双曲函数】
sinh(x) cosh(x) tanh(x)  (双曲正弦、余弦、正切)

【对数函数】
log(x)  (自然对数)
log10(x)  (常用对数)
log2(x)  (以2为底)

【其他函数】
sqrt(x)  (平方根)
exp(x)  (e的x次方)
abs(x)  (绝对值)
floor(x)  (向下取整)
ceil(x)  (向上取整)
round(x)  (四舍五入)
factorial(x)  (阶乘)

【常数】
pi  (圆周率)
e  (自然常数)

示例：
2 + 3 * 4
sqrt(16)
sin(pi/2)
factorial(5)
pow(2, 10)"""
            messagebox.showinfo("帮助信息", help_text)
    
    root = tk.Tk()
    app = CalculatorAgentGUI(root)
    root.mainloop()

def main():
    print("🧮 智能计算器")
    print("请选择运行模式：")
    print("1. 命令行模式 (CLI)")
    print("2. 图形界面模式 (GUI)")
    
    while True:
        choice = input("请输入选择 (1/2)：")
        if choice == "1":
            agent = CalculatorAgent()
            agent.run_cli()
            break
        elif choice == "2":
            run_gui()
            break
        else:
            print("无效选择，请输入 1 或 2")

if __name__ == "__main__":
    main()