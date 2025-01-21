class IDEChecker:
    def __init__(self, page):
        self.page = page
        
    def check_ide_status(self):
        # Check if IDE is loaded by verifying search icon and file structure
        search_icon = self.page.query_selector('.monaco-toolbar .codicon-search')
        files_and_folders = self.page.evaluate('''() => {
            const items = Array.from(document.querySelectorAll(".monaco-highlighted-label"));
            return items.map(item => item.textContent.trim());
        }''')
        
        # Take IDE screenshot
        self.page.screenshot(path="ide.png", full_page=True)
        print("Captured IDE screenshot")
        
        return {
            "test_files_and_folders": "pass" if "challenge" in files_and_folders else "fail",
            "test_search_bar": "pass" if search_icon else "fail",
            "screenshots": "ide.png"
        } 