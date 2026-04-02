import sublime
import sublime_plugin

class HexToDecCommand(sublime_plugin.TextCommand):
    MAX_STR_LEN = 20

    def run(self, edit):
        v = self.view
        
        # Process selections in reverse order to prevent offset shifting
        for region in reversed(list(v.sel())):
            hx = v.substr(region).strip()
            
            # Skip completely empty selections
            if not hx:
                continue

            # Strip the 'h' or 'H' suffix if it exists
            clean_hx = hx
            if clean_hx.lower().endswith('h'):
                clean_hx = clean_hx[:-1]

            try:
                # Python's int() with base 16 inherently handles '0x' prefixes
                dec_val = str(int(clean_hx, 16))
                v.replace(edit, region, dec_val)
                
            except ValueError:
                # If int() fails, it's not a valid hex number
                if len(hx) > self.MAX_STR_LEN:
                    logMsg = hx[0:self.MAX_STR_LEN] + "..."
                else:
                    logMsg = hx
                    
                sublime.status_message("\"%s\" isn't a hexadecimal number!" % logMsg)
                sublime.error_message("\"%s\" isn't a hexadecimal number!" % logMsg)
