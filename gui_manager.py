"""Telegram Bot Agent - GUI Manager"""

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import threading
import os
import sys
import time
import psutil
from pathlib import Path
from datetime import datetime


class BotManagerGUI:
    """GUI Manager for Telegram Bot Agent."""

    def __init__(self, root):
        self.root = root
        self.root.title("Telegram Bot Agent - 管理面板")
        self.root.geometry("700x500")
        self.root.minsize(600, 400)

        # Bot process
        self.bot_process = None
        self.is_running = False
        self.log_file = Path(__file__).parent / "log" / "bot.log"

        # Style
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Create UI
        self._create_status_bar()
        self._create_notebook()
        self._create_dashboard_tab()
        self._create_config_tab()
        self._create_log_tab()

        # Load config
        self._load_env_config()

        # Start monitoring
        self._start_monitoring()

        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    # ==================== UI Creation ====================

    def _create_status_bar(self):
        """Create bottom status bar."""
        self.status_frame = ttk.Frame(self.root)
        self.status_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=2)

        self.status_label = ttk.Label(self.status_frame, text="就绪")
        self.status_label.pack(side=tk.LEFT)

        self.instance_label = ttk.Label(self.status_frame, text="实例: 0", foreground="gray")
        self.instance_label.pack(side=tk.RIGHT, padx=10)

    def _create_notebook(self):
        """Create tab notebook."""
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def _create_dashboard_tab(self):
        """Create dashboard tab."""
        self.dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.dashboard_frame, text="📊 控制台")

        # Bot control section
        control_frame = ttk.LabelFrame(self.dashboard_frame, text="Bot 控制", padding=10)
        control_frame.pack(fill=tk.X, padx=10, pady=5)

        # Start/Stop buttons
        btn_frame = ttk.Frame(control_frame)
        btn_frame.pack(fill=tk.X)

        self.start_btn = ttk.Button(btn_frame, text="▶ 启动 Bot", command=self._start_bot)
        self.start_btn.pack(side=tk.LEFT, padx=5)

        self.stop_btn = ttk.Button(btn_frame, text="⏹ 停止 Bot", command=self._stop_bot, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5)

        self.restart_btn = ttk.Button(btn_frame, text="🔄 重启 Bot", command=self._restart_bot)
        self.restart_btn.pack(side=tk.LEFT, padx=5)

        # Status indicators
        status_frame = ttk.LabelFrame(self.dashboard_frame, text="运行状态", padding=10)
        status_frame.pack(fill=tk.X, padx=10, pady=5)

        # Bot status
        row1 = ttk.Frame(status_frame)
        row1.pack(fill=tk.X, pady=2)
        ttk.Label(row1, text="Bot 状态:").pack(side=tk.LEFT, padx=5)
        self.bot_status_label = ttk.Label(row1, text="⚫ 未运行", foreground="gray")
        self.bot_status_label.pack(side=tk.LEFT, padx=5)

        # Instance count
        row2 = ttk.Frame(status_frame)
        row2.pack(fill=tk.X, pady=2)
        ttk.Label(row2, text="运行实例:").pack(side=tk.LEFT, padx=5)
        self.instance_count_label = ttk.Label(row2, text="0", foreground="gray")
        self.instance_count_label.pack(side=tk.LEFT, padx=5)

        # Proxy status
        row3 = ttk.Frame(status_frame)
        row3.pack(fill=tk.X, pady=2)
        ttk.Label(row3, text="代理状态:").pack(side=tk.LEFT, padx=5)
        self.proxy_status_label = ttk.Label(row3, text="⚫ 未知", foreground="gray")
        self.proxy_status_label.pack(side=tk.LEFT, padx=5)

        # Recent log section
        log_frame = ttk.LabelFrame(self.dashboard_frame, text="最近日志", padding=10)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.recent_log_text = tk.Text(log_frame, height=8, font=("Consolas", 9), state=tk.DISABLED)
        scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.recent_log_text.yview)
        self.recent_log_text.configure(yscrollcommand=scrollbar.set)
        self.recent_log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def _create_config_tab(self):
        """Create configuration tab with form inputs."""
        self.config_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.config_frame, text="⚙️ 配置")

        # Create canvas with scrollbar for config
        canvas = tk.Canvas(self.config_frame)
        scrollbar = ttk.Scrollbar(self.config_frame, orient=tk.VERTICAL, command=canvas.yview)
        self.config_form = ttk.Frame(canvas)

        self.config_form.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.config_form, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Bind mousewheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Config fields
        self.config_vars = {}

        # Telegram section
        ttk.Label(self.config_form, text="Telegram 配置", font=("", 10, "bold")).pack(anchor="w", padx=10, pady=(10, 5))

        self._add_config_field("TELEGRAM_BOT_TOKEN", "Bot Token", "", show="*")
        self._add_config_field("ALLOWED_USER_IDS", "允许的用户 ID", "多个用逗号分隔")

        # Proxy section
        ttk.Label(self.config_form, text="代理配置", font=("", 10, "bold")).pack(anchor="w", padx=10, pady=(10, 5))

        self._add_config_field("PROXY_URL", "代理地址", "例如: http://127.0.0.1:7897")

        # MiMo API section
        ttk.Label(self.config_form, text="MiMo API 配置", font=("", 10, "bold")).pack(anchor="w", padx=10, pady=(10, 5))

        self._add_config_field("MIMO_API_KEY", "API Key", "", show="*")
        self._add_config_field("MIMO_API_BASE_URL", "API 地址", "https://token-plan-cn.xiaomimimo.com/v1")

        # Claude CLI section
        ttk.Label(self.config_form, text="Claude CLI 配置", font=("", 10, "bold")).pack(anchor="w", padx=10, pady=(10, 5))

        self._add_config_field("CLAUDE_CLI_PATH", "CLI 路径", "例如: C:/Users/xxx/.openclaw/claude")
        self._add_config_field("CLAUDE_WORKING_DIR", "工作目录", "例如: E:/Project")

        # Buttons
        btn_frame = ttk.Frame(self.config_form)
        btn_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Button(btn_frame, text="💾 保存配置", command=self._save_env_config).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="🔄 重新加载", command=self._load_env_config).pack(side=tk.LEFT, padx=5)

    def _add_config_field(self, key, label, placeholder, show=None):
        """Add a config field to the form."""
        frame = ttk.Frame(self.config_form)
        frame.pack(fill=tk.X, padx=10, pady=2)

        ttk.Label(frame, text=label + ":", width=15, anchor="e").pack(side=tk.LEFT, padx=(0, 5))

        var = tk.StringVar()
        entry = ttk.Entry(frame, textvariable=var, show=show, width=50)
        entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Placeholder text
        if placeholder:
            entry.insert(0, placeholder)
            entry.config(foreground="gray")
            entry.bind("<FocusIn>", lambda e, p=placeholder: self._on_entry_focus_in(e, p))
            entry.bind("<FocusOut>", lambda e, p=placeholder: self._on_entry_focus_out(e, p))

        self.config_vars[key] = var

    def _on_entry_focus_in(self, event, placeholder):
        """Handle entry focus in - remove placeholder."""
        if event.widget.get() == placeholder:
            event.widget.delete(0, tk.END)
            event.widget.config(foreground="black")

    def _on_entry_focus_out(self, event, placeholder):
        """Handle entry focus out - add placeholder if empty."""
        if not event.widget.get():
            event.widget.insert(0, placeholder)
            event.widget.config(foreground="gray")

    def _create_log_tab(self):
        """Create log tab."""
        self.log_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.log_frame, text="📝 日志")

        # Log viewer
        self.log_text = tk.Text(self.log_frame, font=("Consolas", 9))
        scrollbar = ttk.Scrollbar(self.log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Buttons
        btn_frame = ttk.Frame(self.log_frame)
        btn_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(btn_frame, text="🔄 刷新", command=self._refresh_log).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="🗑️ 清空", command=self._clear_log_display).pack(side=tk.LEFT, padx=5)

        self.auto_refresh_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(btn_frame, text="自动刷新", variable=self.auto_refresh_var).pack(side=tk.RIGHT, padx=5)

    # ==================== Bot Control ====================

    def _start_bot(self):
        """Start the bot process."""
        if self.is_running:
            messagebox.showwarning("警告", "Bot 已在运行中！")
            return

        # Kill existing bot instances first
        existing = self._count_bot_instances()
        if existing > 0:
            self._log_to_display(f"[{datetime.now().strftime('%H:%M:%S')}] 检测到 {existing} 个旧实例，正在清理...")
            self._kill_all_bot_instances()
            time.sleep(1)

        try:
            project_dir = Path(__file__).parent
            self.bot_process = subprocess.Popen(
                [sys.executable, "run.py"],
                cwd=str(project_dir),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0,
            )

            self.is_running = True
            self._update_bot_status(True)
            self._log_to_display(f"[{datetime.now().strftime('%H:%M:%S')}] Bot 已启动 (PID: {self.bot_process.pid})")
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)

        except Exception as e:
            messagebox.showerror("错误", f"启动 Bot 失败: {e}")

    def _stop_bot(self):
        """Stop the bot process."""
        if self.bot_process:
            try:
                self.bot_process.terminate()
                self.bot_process.wait(timeout=5)
            except:
                try:
                    self.bot_process.kill()
                except:
                    pass
            self.bot_process = None

        # Also kill any other bot instances
        self._kill_all_bot_instances()

        self.is_running = False
        self._update_bot_status(False)
        self._log_to_display(f"[{datetime.now().strftime('%H:%M:%S')}] Bot 已停止")
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)

    def _restart_bot(self):
        """Restart the bot."""
        self._stop_bot()
        time.sleep(1)
        self._start_bot()

    def _kill_all_bot_instances(self):
        """Kill all existing bot instances."""
        for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'cwd']):
            try:
                cmdline = proc.info.get('cmdline', [])
                cwd = proc.info.get('cwd', '')
                if cmdline and len(cmdline) >= 2:
                    # Check if this is a python run.py process
                    exe_name = cmdline[0].lower()
                    script_name = cmdline[1].lower()

                    if ('python' in exe_name or 'pythonw' in exe_name) and script_name == 'run.py':
                        # Check if it's in our project directory
                        if cwd and 'telegram-bot' in cwd.lower():
                            pid = proc.info['pid']
                            if self.bot_process and pid == self.bot_process.pid:
                                continue
                            p = psutil.Process(pid)
                            p.terminate()
                            self._log_to_display(f"[{datetime.now().strftime('%H:%M:%S')}] 已停止旧实例 (PID: {pid})")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

    # ==================== Monitoring ====================

    def _start_monitoring(self):
        """Start background monitoring thread."""
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()

    def _monitor_loop(self):
        """Background monitoring loop."""
        while True:
            try:
                # Update instance count
                count = self._count_bot_instances()
                self.root.after(0, self._update_instance_count, count)

                # Check if our process is still running
                if self.is_running and self.bot_process:
                    poll = self.bot_process.poll()
                    if poll is not None:
                        self.root.after(0, self._on_bot_exited, poll)

                # Auto-refresh log
                if self.auto_refresh_var.get():
                    self.root.after(0, self._refresh_log)
                    self.root.after(0, self._refresh_recent_log)

                # Check proxy
                self.root.after(0, self._check_proxy)

            except Exception:
                pass

            time.sleep(3)

    def _count_bot_instances(self):
        """Count running bot instances."""
        count = 0
        for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'cwd']):
            try:
                cmdline = proc.info.get('cmdline', [])
                cwd = proc.info.get('cwd', '')
                if cmdline and len(cmdline) >= 2:
                    # Check if this is a python run.py process
                    # cmdline should be like ['python.exe', 'run.py'] or ['pythonw.exe', 'run.py']
                    exe_name = cmdline[0].lower()
                    script_name = cmdline[1].lower()

                    if ('python' in exe_name or 'pythonw' in exe_name) and script_name == 'run.py':
                        # Check if it's in our project directory
                        if cwd and 'telegram-bot' in cwd.lower():
                            count += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return count

    def _update_instance_count(self, count):
        """Update instance count display."""
        self.instance_count_label.config(text=str(count))
        self.instance_label.config(text=f"实例: {count}")

        if count == 0:
            self.instance_count_label.config(foreground="gray")
            self.instance_label.config(foreground="gray")
        elif count == 1:
            self.instance_count_label.config(foreground="green")
            self.instance_label.config(foreground="green")
        else:
            self.instance_count_label.config(foreground="red")
            self.instance_label.config(foreground="red")

    def _update_bot_status(self, running):
        """Update bot status display."""
        if running:
            self.bot_status_label.config(text="🟢 运行中", foreground="green")
            self.status_label.config(text="Bot 运行中")
        else:
            self.bot_status_label.config(text="⚫ 未运行", foreground="gray")
            self.status_label.config(text="Bot 已停止")

    def _on_bot_exited(self, return_code):
        """Handle bot process exit."""
        self.is_running = False
        self.bot_process = None
        self._update_bot_status(False)
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self._log_to_display(f"[{datetime.now().strftime('%H:%M:%S')}] Bot 已退出 (返回码: {return_code})")

    def _check_proxy(self):
        """Check proxy connection status."""
        import socket
        try:
            proxy_url = self._get_config_value("PROXY_URL")
            if proxy_url and proxy_url not in ["", "例如: http://127.0.0.1:7897"]:
                proxy_addr = proxy_url.split("://")[-1]
                host, port = proxy_addr.split(":")
                port = int(port)

                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                result = sock.connect_ex((host, port))
                sock.close()

                if result == 0:
                    self.root.after(0, lambda: self.proxy_status_label.config(text="🟢 已连接", foreground="green"))
                else:
                    self.root.after(0, lambda: self.proxy_status_label.config(text="🔴 端口未开放", foreground="red"))
            else:
                self.root.after(0, lambda: self.proxy_status_label.config(text="⚪ 未配置", foreground="gray"))
        except Exception:
            self.root.after(0, lambda: self.proxy_status_label.config(text="🔴 检测失败", foreground="red"))

    # ==================== Config Management ====================

    def _load_env_config(self):
        """Load .env configuration into form fields."""
        env_path = Path(__file__).parent / ".env"
        if not env_path.exists():
            return

        try:
            with open(env_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()
                        if key in self.config_vars:
                            self.config_vars[key].set(value)
        except Exception as e:
            messagebox.showerror("错误", f"加载配置失败: {e}")

    def _save_env_config(self):
        """Save form fields to .env file."""
        env_path = Path(__file__).parent / ".env"

        try:
            lines = []
            lines.append("# Telegram Bot 配置")
            lines.append(f"TELEGRAM_BOT_TOKEN={self.config_vars['TELEGRAM_BOT_TOKEN'].get()}")
            lines.append("")
            lines.append("# MiMo API 配置")
            lines.append(f"MIMO_API_KEY={self.config_vars['MIMO_API_KEY'].get()}")
            lines.append(f"MIMO_API_BASE_URL={self.config_vars['MIMO_API_BASE_URL'].get()}")
            lines.append("")
            lines.append("# 代理配置（Clash Verge）")
            lines.append(f"PROXY_URL={self.config_vars['PROXY_URL'].get()}")
            lines.append("")
            lines.append("# Claude Code CLI 配置")
            lines.append(f"CLAUDE_CLI_PATH={self.config_vars['CLAUDE_CLI_PATH'].get()}")
            lines.append(f"CLAUDE_WORKING_DIR={self.config_vars['CLAUDE_WORKING_DIR'].get()}")
            lines.append("")
            lines.append("# 安全配置")
            lines.append(f"ALLOWED_USER_IDS={self.config_vars['ALLOWED_USER_IDS'].get()}")

            with open(env_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(lines) + '\n')

            messagebox.showinfo("成功", "配置已保存！\n请重启 Bot 使配置生效。")

        except Exception as e:
            messagebox.showerror("错误", f"保存配置失败: {e}")

    def _get_config_value(self, key):
        """Get value from config vars."""
        if key in self.config_vars:
            value = self.config_vars[key].get()
            # Return None if it's a placeholder
            if value.startswith("例如:") or value == "":
                return None
            return value
        return None

    # ==================== Log Management ====================

    def _refresh_log(self):
        """Refresh log display."""
        if not self.log_file.exists():
            return

        try:
            with open(self.log_file, 'r', encoding='utf-8', errors='replace') as f:
                lines = f.readlines()

            recent = lines[-100:] if len(lines) > 100 else lines
            content = ''.join(recent)

            current = self.log_text.get(1.0, tk.END)
            if current.strip() != content.strip():
                self.log_text.delete(1.0, tk.END)
                self.log_text.insert(tk.END, content)
                self.log_text.see(tk.END)

        except Exception:
            pass

    def _refresh_recent_log(self):
        """Refresh recent log in dashboard."""
        if not self.log_file.exists():
            return

        try:
            with open(self.log_file, 'r', encoding='utf-8', errors='replace') as f:
                lines = f.readlines()

            recent = lines[-10:] if len(lines) > 10 else lines
            content = ''.join(recent)

            self.recent_log_text.config(state=tk.NORMAL)
            current = self.recent_log_text.get(1.0, tk.END)
            if current.strip() != content.strip():
                self.recent_log_text.delete(1.0, tk.END)
                self.recent_log_text.insert(tk.END, content)
                self.recent_log_text.see(tk.END)
            self.recent_log_text.config(state=tk.DISABLED)

        except Exception:
            pass

    def _clear_log_display(self):
        """Clear log display."""
        self.log_text.delete(1.0, tk.END)

    def _log_to_display(self, message):
        """Add message to recent log display."""
        self.recent_log_text.config(state=tk.NORMAL)
        self.recent_log_text.insert(tk.END, message + "\n")
        self.recent_log_text.see(tk.END)
        self.recent_log_text.config(state=tk.DISABLED)

    # ==================== Utility ====================

    def _on_close(self):
        """Handle window close."""
        if self.is_running:
            if messagebox.askyesno("确认", "Bot 正在运行中，是否停止并退出？"):
                self._stop_bot()
                self.root.destroy()
            else:
                return
        else:
            self.root.destroy()


def main():
    """Main entry point."""
    root = tk.Tk()
    app = BotManagerGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()