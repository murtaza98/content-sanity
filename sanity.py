import time
import argparse
import json
from playwright.sync_api import sync_playwright
from ide_checker import IDEChecker
from preview_checker import PreviewChecker

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
                
                # Initialize checkers
                ide_checker = IDEChecker(page)
                preview_checker = PreviewChecker(page)
                
                # Run checks
                ide_results = ide_checker.check_ide_status()
                preview_results = preview_checker.check_preview_status()
                
                # Combine results
                self.test_results = {
                    "ide_checks": ide_results,
                    "preview_checks": preview_results
                }
                
                # Save results to file
                with open('test_results.json', 'w') as f:
                    json.dump(self.test_results, f, indent=2)
                
                print("Results saved to test_results.json")
                
            except Exception as e:
                print(f"Error during test: {str(e)}")
                self.test_results = {
                    "ide_checks": {
                        "test_files_and_folders": "fail",
                        "test_search_bar": "fail",
                        "screenshots": "ide.png"
                    },
                    "preview_checks": {
                        "preview_iframe": "fail",
                        "application_state": "unknown",
                        "screenshots": "preview.png",
                        "test_compilation": "fail"
                    }
                }
            
            finally:
                self.print_summary()

    def print_summary(self):
        print(json.dumps(self.test_results, indent=2))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run IDE tests in sequence.")
    parser.add_argument('ide_url', type=str, help="The IDE URL to test.")
    args = parser.parse_args()
    
    ide_test = IDETest(args.ide_url)
    ide_test.run()


# https://vm-6a4d2dce-d20f-4d1d-93b8-8627694ba6a5.in-vmprovider.projects.hrcdn.net