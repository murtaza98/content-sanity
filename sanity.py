from playwright.sync_api import sync_playwright
import time

def explore_vm_contents():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = context.new_page()
        
        try:
            # Navigate to the VM URL
            page.goto('https://vm-6a25ef3f-8ed0-4b68-af1b-9b0d5bc3b352-ide.in-vmprovider.projects.hrcdn.net/')
            
            # Wait for the IDE to load completely
            page.wait_for_load_state('networkidle')
            page.wait_for_load_state('domcontentloaded')
            time.sleep(2)
            
            # Get files and folders
            files_and_folders = page.evaluate('''() => {
                const items = Array.from(document.querySelectorAll('.monaco-list-row'));
                return items
                    .map(item => item.textContent.trim())
                    .filter(text => text.length > 0);
            }''')
            
            # Look for Preview text
            preview_elements = page.evaluate('''() => {
                return Array.from(document.querySelectorAll('*'))
                    .filter(el => el.textContent.includes('Preview'))
                    .map(el => el.textContent.trim())
                    .filter(text => text === 'Preview');  // Exact match only
            }''')
            
            print("\n📂 Files and Folders:")
            for item in files_and_folders:
                print(f"  - {item}")
                
            print("\n🔍 Preview Elements:")
            if preview_elements:
                for elem in preview_elements:
                    print(f"  Found: {elem}")
            else:
                print("  No Preview text found")
            
        except Exception as e:
            print(f"❌ An error occurred: {str(e)}")
        
        finally:
            time.sleep(3)
            browser.close()

if __name__ == "__main__":
    explore_vm_contents()