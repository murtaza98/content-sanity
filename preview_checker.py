import time

class PreviewChecker:
    def __init__(self, page):
        self.page = page
        
    def check_preview_status(self):
        # Check if preview iframe exists and is accessible
        preview_iframe = self.page.frame_locator('#hr-realtime-preview-iframe')
        iframe_element = self.page.query_selector('#hr-realtime-preview-iframe')
        
        # Take preview screenshot
        self.page.screenshot(path="preview.png", full_page=True)
        print("Captured preview screenshot")
        
        if not iframe_element:
            print("Preview iframe not found")
            return self._get_preview_results("not running", False)
            
        # Check for "Application is not running" message
        preview_message = preview_iframe.locator('text="Application is not running."').count()
        initial_state = "not running" if preview_message > 0 else "running"
        
        # If iframe exists but is empty or not loaded properly, mark as not running
        iframe_content = preview_iframe.locator('body').count()
        if iframe_content == 0:
            print("Preview iframe is empty or not loaded")
            return self._get_preview_results("not running", False)
            
        print(f"Initial application state: {initial_state}")
        
        # Check preview state every second for up to 60 seconds
        start_time = time.time()
        max_wait_time = 60
        application_started = False
        
        print("Checking application state...")
        while time.time() - start_time < max_wait_time:
            preview_message = preview_iframe.locator('text="Application is not running."').count()
            if preview_message == 0:
                application_started = True
                end_time = time.time()
                startup_time = end_time - start_time
                print(f"Application started in {startup_time:.2f} seconds")
                break
            time.sleep(1)
        
        if not application_started:
            print("Application did not start within 60 seconds")
            
        # Record final state
        preview_message = preview_iframe.locator('text="Application is not running."').count()
        final_state = "not running" if preview_message > 0 else "running"
        print(f"Final application state: {final_state}")
        
        return self._get_preview_results(final_state, iframe_element is not None)
        
    def _get_preview_results(self, state, iframe_exists):
        return {
            "preview_iframe": "pass" if iframe_exists else "fail",
            "application_state": state,
            "screenshots": "preview.png",
            "test_compilation": "pass" if state == "running" else "fail"
        } 