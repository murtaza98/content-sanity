import time
import argparse
import json
from playwright.sync_api import sync_playwright

class IDETest:
    def __init__(self, ide_url):
        self.ide_url = ide_url
        self.p = sync_playwright().start()
        self.test_results = {}

    def run(self):
        with self.p.chromium.launch(headless=False) as browser:
            context = browser.new_context(viewport={'width': 1920, 'height': 1080})
            page = context.new_page()
            
            try:
                page.goto(self.ide_url)
                page.wait_for_load_state('networkidle')
                page.wait_for_load_state('domcontentloaded')
                time.sleep(2)
                
                # Run all the test modules sequentially and store results
                self.test_files_and_folders(page)
                time.sleep(5) 
                self.test_preview(page)
                
            except Exception as e:
                print(f"❌ An error occurred: {str(e)}")
            
            finally:
                # Output the summary of test results as JSON which can be used for reporting
                self.print_summary()

    def test_files_and_folders(self, page):
        # Get files and folders (using new selector)
        files_and_folders = page.evaluate('''() => {
            const items = Array.from(document.querySelectorAll(".monaco-highlighted-label"));
            return items
                .map(item => item.textContent.trim())
                .filter(text => text === "challenge");  // Look for "challenge"
        }''')

        # Check if the files and folders section has the correct content
        if files_and_folders:
            self.test_results["test_files_and_folders"] = "pass"
        else:
            self.test_results["test_files_and_folders"] = "fail"

    def test_preview(self, page):
        # Look for Preview element (checking for iframe presence)
        preview_element = page.query_selector('#hr-realtime-preview-iframe')

        # Check if the preview iframe is present
        if preview_element:
            self.test_results["test_preview"] = "pass"
        else:
            self.test_results["test_preview"] = "fail"

    # Add more test modules as needed, for example:
    def test_search_functionality(self, page):
        print("\n🔍 Testing Search Functionality...")
        search_box = page.query_selector('input[type="search"]')
        if search_box:
            print("  ✅ Search box found!")
        else:
            print("  ❌ Search box not found.")

    def print_summary(self):
        # Output the test results in JSON format
        print(json.dumps(self.test_results, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run IDE tests in sequence.")
    parser.add_argument('ide_url', type=str, help="The IDE URL to test.")
    args = parser.parse_args()
    
    ide_test = IDETest(args.ide_url)
    ide_test.run()
