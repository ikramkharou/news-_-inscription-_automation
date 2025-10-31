import tkinter as tk
import logging
from gui.newsletter_app import NewsletterApp
from config import logger

logger.info("Starting Newsletter Subscription Tool")


def main():
    root = tk.Tk()
    app = NewsletterApp(root)
    root.mainloop()
    

if __name__ == "__main__":
    main()

