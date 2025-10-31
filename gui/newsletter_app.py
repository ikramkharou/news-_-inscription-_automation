import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading
import logging
from factory.scraper_factory import ScraperFactory
from services.email_processor import EmailProcessor
from utils.email_validator import parse_emails

logger = logging.getLogger(__name__)


class NewsletterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Newsletter Subscription Tool")
        self.root.geometry("700x600")
        
        self.scraper_factory = ScraperFactory()
        self.email_processor = EmailProcessor()
        
        self.setup_ui()
    
    def setup_ui(self):
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        url_label = tk.Label(main_frame, text="Website URL:", font=("Arial", 10))
        url_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.url_entry = tk.Entry(main_frame, font=("Arial", 10), width=70)
        self.url_entry.pack(fill=tk.X, pady=(0, 15))
        
        emails_label = tk.Label(main_frame, text="Email List (one per line):", font=("Arial", 10))
        emails_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.emails_text = scrolledtext.ScrolledText(main_frame, height=15, font=("Arial", 10))
        self.emails_text.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        self.start_button = tk.Button(
            button_frame,
            text="Start Subscription",
            command=self.start_subscription,
            font=("Arial", 11),
            bg="#4CAF50",
            fg="white",
            padx=20,
            pady=10
        )
        self.start_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.clear_button = tk.Button(
            button_frame,
            text="Clear",
            command=self.clear_fields,
            font=("Arial", 11),
            bg="#f44336",
            fg="white",
            padx=20,
            pady=10
        )
        self.clear_button.pack(side=tk.LEFT)
    
    def validate_inputs(self) -> tuple:
        url = self.url_entry.get().strip()
        emails_text = self.emails_text.get("1.0", tk.END).strip()
        emails = parse_emails(emails_text)
        
        if not url:
            messagebox.showerror("Error", "Please enter a website URL")
            return None, None
        
        if not emails:
            messagebox.showerror("Error", "Please enter at least one valid email address")
            return None, None
        
        if not self.scraper_factory.is_supported_url(url):
            supported = self.scraper_factory.get_supported_sites_list()
            messagebox.showerror(
                "Error",
                f"Unsupported website URL: {url}\n\nSupported sites: {supported}"
            )
            return None, None
        
        return url, emails
    
    def clear_fields(self):
        self.url_entry.delete(0, tk.END)
        self.emails_text.delete("1.0", tk.END)
    
    def start_subscription(self):
        url, emails = self.validate_inputs()
        
        if not url or not emails:
            return
        
        self.start_button.config(state=tk.DISABLED)
        
        thread = threading.Thread(target=self.run_async_processing, args=(url, emails))
        thread.daemon = True
        thread.start()
    
    def run_async_processing(self, url: str, emails: list):
        import asyncio
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            results = loop.run_until_complete(self.email_processor.process_emails(url, emails))
            self.root.after(0, lambda: self.show_results(results))
        except Exception as e:
            logger.error(f"Error in async processing: {e}")
            self.root.after(0, lambda: messagebox.showerror("Error", f"An error occurred: {str(e)}"))
        finally:
            self.root.after(0, lambda: self.start_button.config(state=tk.NORMAL))
            loop.close()
    
    def show_results(self, results: dict):
        success = results.get("success", 0)
        failed = results.get("failed", 0)
        total = results.get("total", 0)
        
        message = f"Processing complete!\n\nSuccess: {success}\nFailed: {failed}\nTotal: {total}"
        
        if results.get("errors"):
            error_details = "\n".join(results["errors"][:5])
            if len(results["errors"]) > 5:
                error_details += f"\n... and {len(results['errors']) - 5} more"
            message += f"\n\nErrors:\n{error_details}"
        
        if failed == 0:
            messagebox.showinfo("Success", message)
        else:
            messagebox.showwarning("Completed with Errors", message)

